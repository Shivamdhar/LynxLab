resource "aws_s3_bucket" "logs_bucket" {
  bucket = var.bucket_name
}
