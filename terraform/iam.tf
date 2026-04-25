###############################################################################
# IAM Role: Authorization Lambda
###############################################################################

resource "aws_iam_role" "authorization_lambda_role" {
  name = "AuthorizationLambdaExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "authorization_lambda_cloudwatch" {
  name = "CloudWatchLogPolicy"
  role = aws_iam_role.authorization_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "authorization_lambda_secrets" {
  name = "SecretReadPolicy"
  role = aws_iam_role.authorization_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = aws_secretsmanager_secret.auth_secret.arn
      }
    ]
  })
}

resource "aws_iam_role_policy" "authorization_lambda_apigw" {
  name = "ApiGatewayInvokePolicy"
  role = aws_iam_role.authorization_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["execute-api:Invoke"]
        Resource = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*/invoke"
      }
    ]
  })
}

###############################################################################
# IAM Role: Main Lambda
###############################################################################

resource "aws_iam_role" "main_lambda_role" {
  name = "MainLambdaExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "main_lambda_basic_execution" {
  role       = aws_iam_role.main_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "main_lambda_bedrock" {
  name = "BedrockAccessPolicy"
  role = aws_iam_role.main_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:ListFoundationModels"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "main_lambda_s3" {
  name = "BucketPutPolicy"
  role = aws_iam_role.main_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.logs_bucket.arn}/*"
      }
    ]
  })
}

###############################################################################
# IAM Role: API Gateway invoke Lambda
###############################################################################

resource "aws_iam_role" "apigw_invoke_lambda_role" {
  name = "ApiGatewayInvokeLambdaRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "apigw_invoke_policy" {
  name = "AuthorizerPermissionsPolicy"
  role = aws_iam_role.apigw_invoke_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction",
          "sts:AssumeRole"
        ]
        Resource = aws_lambda_function.authorization_lambda.arn
      },
      {
        Effect   = "Allow"
        Action   = ["execute-api:Invoke"]
        Resource = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*/invoke"
      }
    ]
  })
}
