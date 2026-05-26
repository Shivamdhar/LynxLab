import json
import boto3
import os
import logging
import time
from botocore.exceptions import ClientError

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the Bedrock Runtime client
bedrock_runtime = boto3.client('bedrock-runtime')


def lambda_handler(event, context):
    logger.info('Received event: %s', json.dumps(event))

    try:
        # Retrieve the model ID from environment variables
        model_id = os.environ['BEDROCK_MODEL_ID']
        print("In lambda handle !!")
        # Validate the input
        input_text = event.get("queryStringParameters", {}).get("inputText")
        input_task = event.get("queryStringParameters", {}).get("inputTask")
        if not input_text or not input_task:
            logger.error('Input text / Input task is missing in the request')
            raise ValueError("Input text / Input task is required in the request query parameters.")

        combined_prompt = f"Task: {input_task}\n\nContent to analyze: {input_text}"

        payload = [
            {
                "role": "user",
                "content": [{"text": combined_prompt}]
            }
        ]

        logger.info('Payload for Bedrock model: %s', payload)

        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=payload,
            inferenceConfig={
                "maxTokens": 600,
                "temperature": 0.3,
                "topP": 0.9
            },
        )

        logger.info('Response from Bedrock model: %s', response)

        # Check if the 'output' exists in the response and handle it correctly
        if 'output' not in response or not response['output']:
            logger.error('Response output is empty')
            raise ValueError("Response output is empty.")

        # Read and process the response
        response_body = response['output']
        print(type(response_body))
        logger.info('Processed response body: %s', response_body)
        response_message = response['output']['message']
        response_text = response_message['content'][0]['text']

        fileName = "request-" + str(int(time.time())) + ".txt"
        log_content = {
            "request_payload": payload,
            "response_output": response_text,
            "model_used": model_id
        }

        # Upload the file
        s3_client = boto3.client('s3')
        bucket_name = os.environ['BUCKET_NAME']
        try:
            resp = s3_client.put_object(Bucket=bucket_name, Key=fileName, Body=json.dumps(log_content).encode("utf-8"))
        except ClientError as e:
            logging.error(e)

        rawResponse = json.dumps({"analysis": response_text.strip()})
        rawResponse = rawResponse.replace('\n\n', '')
        return {
            'statusCode': 200,
            'body': rawResponse
        }

    except ClientError as e:
        logger.error('ClientError: %s', e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Error interacting with the Bedrock API"})
        }
    except ValueError as e:
        logger.error('ValueError: %s', e)
        return {
            'statusCode': 400,
            'body': json.dumps({"error": str(e)})
        }
    except Exception as e:
        logger.error('Exception: %s', e)
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Internal Server Error"})
        }
