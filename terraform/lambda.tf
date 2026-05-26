data "archive_file" "authorizer_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_src/authorizer/index.py"
  output_path = "${path.module}/.build/authorizer.zip"
}

data "archive_file" "main_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_src/main/index.py"
  output_path = "${path.module}/.build/main.zip"
}

resource "aws_lambda_function" "authorization_lambda" {
  function_name    = "AuthorizationLambdaFunction"
  description      = "Lambda Authorizer for API Gateway"
  role             = aws_iam_role.authorization_lambda_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.12"
  timeout          = 10
  memory_size      = 128
  filename         = data.archive_file.authorizer_lambda_zip.output_path
  source_code_hash = data.archive_file.authorizer_lambda_zip.output_base64sha256

  environment {
    variables = {
      AuthSecret = var.auth_secret_name
    }
  }
}

resource "aws_lambda_function" "main_lambda" {
  function_name    = "MainLambdaFunction"
  description      = "Make requests to Bedrock models"
  role             = aws_iam_role.main_lambda_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.12"
  timeout          = 30
  memory_size      = 512
  filename         = data.archive_file.main_lambda_zip.output_path
  source_code_hash = data.archive_file.main_lambda_zip.output_base64sha256

  environment {
    variables = {
      BEDROCK_MODEL_ID = var.bedrock_model_id
      BUCKET_NAME      = var.bucket_name
    }
  }
}
