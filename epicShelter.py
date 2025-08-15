import pyfiglet
import subprocess
import json
import sys
import time
import os
import threading


# Usage: python3 epicShelter.py [OPERATION] 
# [OPERATION] - create/destroy

CREATE_OPERATION = 'create'
DESTROY_OPERATION = 'destroy'
allowedOperations = [CREATE_OPERATION, DESTROY_OPERATION]
def printBanner(banner:str):
    print("printing banner")

    # Generate the ASCII art banner
    # You can specify a font using the 'font' argument, e.g., font="slant"
    ascii_banner = pyfiglet.figlet_format(banner, font="standard")

    # Print the generated banner
    print(ascii_banner)

def validateArgs(args):
    if len(args) == 0:
        print("Operation not specified")
        return
    else:
        if len(args) == 1 and args[0] in allowedOperations:
            return True
        else:
            print("Invalid operation: Valid operations are create and destroy")
    return False

def createSecret():
    #aws secretsmanager create-secret  --name AuthSecret --description SecretValue --secret-string file://secret.json
    createSecretResponse = subprocess.run(
        [
            "aws",
            "secretsmanager",
            "create-secret",
            "--name",
            "TestSecret2",
            "--description",
            "SecretValue",
            "--secret-string",
            "file://secret.json",
        ],
        capture_output=True,
    )
    createSecretResponseJson = json.loads(createSecretResponse.stdout.decode("utf-8"))
    print(createSecretResponseJson)

    getSecretResponse = subprocess.run(
        [
            "aws",
            "secretsmanager",
            "get-secret-value",
            "--secret-id",
            "TestSecret2"
        ],
        capture_output=True,
    )
    getSecretResponseJson = json.loads(getSecretResponse.stdout.decode("utf-8"))
    print(getSecretResponseJson)


def deleteSecret():
    deleteSecretResponse = subprocess.run(
        [
            "aws",
            "secretsmanager",
            "delete-secret",
            "--secret-id",
            "TestSecret2"
        ],
        capture_output=True,
    )
    deleteSecretResponseJson = json.loads(deleteSecretResponse.stdout.decode("utf-8"))
    print(deleteSecretResponseJson)

def createStack():
    print("Creating cloudFormation stack !!!")
    '''
    aws cloudformation create-stack \
    --stack-name apigw-lambda-bedrock \
    --template-body file://infrastructure/root.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --disable-rollback
    '''
    createStackResponse = subprocess.run(
        [
            "aws",
            "cloudformation",
            "create-stack",
            "--stack-name",
            "apigw-lambda-bedrock",
            "--template-body",
            "file://root.yaml",
            "--capabilities",
            "CAPABILITY_NAMED_IAM",
            "--disable-rollback"
        ],
        capture_output=True,
    )
    createStackResponseJson = json.loads(createStackResponse.stdout.decode("utf-8"))
    print(createStackResponseJson)

def destroyStack():
    '''
    aws cloudformation delete-stack --stack-name apigw-lambda-bedrock
    '''
    deleteStackResponse = subprocess.run(
        [
            "aws",
            "cloudformation",
            "delete-stack",
            "--stack-name",
            "apigw-lambda-bedrock"
        ],
        capture_output=True,
    )
    print(deleteStackResponse)
    # deleteStackResponseJson = json.loads(deleteStackResponse.stdout.decode("utf-8"))
    # print(deleteStackResponseJson)


def deleteBucket():
    '''
    aws s3api delete-bucket --bucket logs-bucket-test-1
    '''
    deleteBucketResponse = subprocess.run(
        [
            "aws",
            "s3api",
            "delete-bucket",
            "--bucket",
            "logs-bucket-test-1"
        ],
        capture_output=True,
    )
    print(deleteBucketResponse)

def createBucket():
    '''
    aws s3api create-bucket --bucket logs-bucket-test-1
    '''
    createBucketResponse = subprocess.run(
        [
            "aws",
            "s3api",
            "create-bucket",
            "--bucket",
            "logs-bucket-test-1"
        ],
        capture_output=True,
    )
    createBucketResponseJson = json.loads(createBucketResponse.stdout.decode("utf-8"))
    print(createBucketResponseJson)


def loadingAnimation(process) :
    print("Start")
    while process.is_alive() :
        chars = "/—\|" 
        for char in chars:
            sys.stdout.write('\r'+'loading '+char)
            time.sleep(.1)
            sys.stdout.flush()
    print("\n")
    print("Finsihed !!")



def foo():
    time.sleep(5)
    return


def getApiGateWayEndpoint():
    api_name="HttpApi4328"
    stage_name="dev"

    getApiGwEndpointResponse = subprocess.run(
        [
            "aws",
            "apigatewayv2",
            "get-apis",
            "--query",
            "Items[?Name=='"+api_name+"'].ApiEndpoint",
            "--output",
            "text"
        ],
        capture_output=True,
        text=True
    )
    gateWayUrl = getApiGwEndpointResponse.stdout.removesuffix("\n")
    invoke_url=gateWayUrl + "/" + stage_name
    print(invoke_url)

if __name__ == '__main__':
    printBanner(banner="Epic Shelter")
    if validateArgs(sys.argv[1:]):
        operation = sys.argv[1]
        print(f"Performing operation: [{operation}]")
        if operation == CREATE_OPERATION:
            # createSecret()
            createBucket()
            # createStack()
            # loading_process = threading.Thread(target=foo)
            # loading_process.start()

            # loadingAnimation(loading_process)
            # loading_process.join()
            # getApiGateWayEndpoint()
        elif operation == DESTROY_OPERATION:
            #deleteSecret()
            deleteBucket()
            #destroyStack()
            pass

