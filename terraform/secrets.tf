resource "aws_secretsmanager_secret" "auth_secret" {
  name = var.auth_secret_name
}

resource "aws_secretsmanager_secret_version" "auth_secret_value" {
  secret_id     = aws_secretsmanager_secret.auth_secret.id
  secret_string = var.auth_secret_value
}
