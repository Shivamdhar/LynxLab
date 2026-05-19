## Steps to spin up the stack
1. terraform init
2. terraform apply -var="auth_secret_value=$(aws configure get aws_secret_access_key)" -var="bucket_name=<unique-bucket-name>"


## Steps to destroy up the stack
1. terraform destroy