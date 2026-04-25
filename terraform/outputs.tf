output "api_invoke_url" {
  description = "Full URL to invoke the API"
  value       = "${aws_apigatewayv2_stage.dev.invoke_url}/invoke"
}

output "api_endpoint" {
  description = "API Gateway endpoint"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}
