# 1. Automatically grab the identity of whoever runs the command
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "logs_bucket" {
  # 2. Extract the IAM user/role name dynamically and use it as a prefix
  # (lower() and split() ensure compliance with S3's strict lowercase naming rules)
  bucket_prefix = "logs-${lower(element(split("/", data.aws_caller_identity.current.arn), 1))}-"
  
  force_destroy = true
}