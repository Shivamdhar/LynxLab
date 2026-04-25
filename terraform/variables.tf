variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "auth_secret_name" {
  description = "Name of the Secrets Manager secret for API Gateway authorization"
  type        = string
  default     = "AuthSecret"
}

variable "auth_secret_value" {
  description = "Value of the authorization secret"
  type        = string
  sensitive   = true
}

variable "bedrock_model_id" {
  description = "Bedrock model ID to use for inference"
  type        = string
  default     = "us.amazon.nova-micro-v1:0"
}

variable "bucket_name" {
  description = "S3 bucket name for storing request/response logs"
  type        = string
  default     = "logs-bucket-test-1"
}
