resource "aws_apigatewayv2_api" "http_api" {
  name          = "HttpApi4328"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_authorizer" "lambda_authorizer" {
  api_id                            = aws_apigatewayv2_api.http_api.id
  name                              = "HttpApiGatewayAuthorizer"
  authorizer_type                   = "REQUEST"
  enable_simple_responses           = true
  authorizer_uri                    = aws_lambda_function.authorization_lambda.invoke_arn
  authorizer_result_ttl_in_seconds  = 0
  authorizer_payload_format_version = "2.0"
  authorizer_credentials_arn        = aws_iam_role.apigw_invoke_lambda_role.arn
  identity_sources                  = ["$request.header.Authorization"]
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "dev"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "main_lambda" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"
  integration_uri        = aws_lambda_function.main_lambda.invoke_arn
}

resource "aws_apigatewayv2_route" "invoke" {
  api_id             = aws_apigatewayv2_api.http_api.id
  route_key          = "ANY /invoke"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.lambda_authorizer.id
  target             = "integrations/${aws_apigatewayv2_integration.main_lambda.id}"
}

resource "aws_lambda_permission" "apigw_invoke_main_lambda" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*/invoke"
}
