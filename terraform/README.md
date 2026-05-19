## Steps to spin up the stack
1. terraform init
2. terraform apply -var="auth_secret_value=<your-secret-access-key>" -var="bucket_name=<unique-bucket-name>"


## Steps to destroy up the stack
1. terraform destroy