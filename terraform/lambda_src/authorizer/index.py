import boto3
from botocore.exceptions import ClientError
import json
import os


def lambda_handler(event, context):
    secret_name = os.environ['AuthSecret']
    region_name = context.invoked_function_arn.split(":")[3]

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret_token = get_secret_value_response['SecretString']

        # Access the authorization token from identitySource
        authorization_header = event.get('identitySource', [None])[0]

        # Check if the authorization header is properly set
        if not authorization_header:
            return {"isAuthorized": False}

        # Extract the token from the Bearer scheme
        token_parts = authorization_header.split(' ')
        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return {"isAuthorized": False}

        token = token_parts[1]

        # Check if the provided token matches the secret token
        is_authorized = token == secret_token

        print("Request authenticated successfully")
        # Construct the response
        response = {
            "isAuthorized": is_authorized
        }
        return response
    except ClientError as e:
        print(f"Error retrieving parameter: {e}")
        return {
            "isAuthorized": False,
            "context": {
                "error": "Internal server error"
            }
        }
