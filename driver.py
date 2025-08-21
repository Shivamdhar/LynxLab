import pyfiglet
import boto3
import json
import subprocess
import sys
import threading
import time

from botocore.exceptions import ClientError
 
# [OPERATION] - create/destroy/update

CREATE_OPERATION = 'create'
DESTROY_OPERATION = 'destroy'
UPDATE_OPERATION = 'update'
GET_API_URL = 'getUrl'
allowedOperations = [CREATE_OPERATION, DESTROY_OPERATION, GET_API_URL, UPDATE_OPERATION]

def printBanner(banner:str):

    # Generate the ASCII art banner
    # You can specify a font using the 'font' argument, e.g., font="slant"
    ascii_banner = pyfiglet.figlet_format(banner, font="ghost")

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


def handleOperation(operationName:str, response:subprocess.CompletedProcess):
    if response.returncode == 0:
        print(f"Operation  {operationName} successfull")
    else:
        print(f"An unexpected AWS error occurred: {response.stderr}")
        sys.exit()

def createSecret():
    #aws secretsmanager create-secret  --name AuthSecret --description SecretValue --secret-string file://secret.json

    session = boto3.session.Session()
    credentials = session.get_credentials()
    createSecretResponse = subprocess.run(
        [
            "aws",
            "secretsmanager",
            "create-secret",
            "--name",
            "AuthSecret",
            "--description",
            "SecretValue",
            "--secret-string",
            credentials.secret_key,
        ],
        capture_output=True,
    )
    handleOperation(operationName='Create Secret',response=createSecretResponse)

def getSecret(secretName:str):
    '''
    aws secretsmanager get-secret-value --secret-id TestSecret1
    '''
    try:
        # getSecretResponse = subprocess.run(
        #     [
        #         "aws",
        #         "secretsmanager",
        #         "get-secret-value",
        #         "--secret-id",
        #         "TestSecret99"
        #     ],
        #     capture_output=True,
        # )
        # print(getSecretResponse)
        # returnCode = getSecretResponse.returncode
        # print(returnCode)
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )
        
        get_secret_value_response = client.get_secret_value(
            SecretId=secretName
        )
    except ClientError as e:
        print('here !!!!!!!!!')
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('ResourceNotFoundException for secret ', secretName)
            # Perform specific actions for a missing resource, e.g., create it
        else:
            print(f"An unexpected AWS error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # getSecretResponseJson = json.loads(getSecretResponse.stdout.decode("utf-8"))
    # print(getSecretResponseJson)


def deleteSecret():
    deleteSecretResponse = subprocess.run(
        [
            "aws",
            "secretsmanager",
            "delete-secret",
            "--secret-id",
            "AuthSecret",
            "--force-delete-without-recovery"
        ],
        capture_output=True,
    )
    handleOperation(operationName='Delete Secret',response=deleteSecretResponse)

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
    handleOperation(operationName='Create Stack',response=createStackResponse)


def updateStack():
    print("Update cloudFormation stack !!!")
    '''
    aws cloudformation create-stack \
    --stack-name apigw-lambda-bedrock \
    --template-body file://infrastructure/root.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --disable-rollback
    '''
    updateStackResponse = subprocess.run(
        [
            "aws",
            "cloudformation",
            "update-stack",
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
    handleOperation(operationName='Update Stack',response=updateStackResponse)

def getStackStatus():
    '''
    aws cloudformation describe-stacks --stack-name apigw-lambda-bedrock
    '''
    getStackResponse = subprocess.run(
        [
            "aws",
            "cloudformation",
            "describe-stacks",
            "--stack-name",
            "apigw-lambda-bedrock"
        ],
        capture_output=True,
    )
    return getStackResponse


def monitorStackCreationStatus():
    currentStackResp = getStackStatus()
    getSecretResponseJson = json.loads(currentStackResp.stdout.decode("utf-8"))
    currentStackStatus = getSecretResponseJson['Stacks'][0]["StackStatus"] 
    print("StackStatus ", currentStackStatus)
    while currentStackStatus != 'CREATE_COMPLETE':
        monitorStackCreationStatus()
    sys.exit()


def monitorStackUpdationStatus():
    currentStackResp = getStackStatus()
    getSecretResponseJson = json.loads(currentStackResp.stdout.decode("utf-8"))
    currentStackStatus = getSecretResponseJson['Stacks'][0]["StackStatus"] 
    print("StackStatus ", currentStackStatus)
    while currentStackStatus != 'UPDATE_COMPLETE':
        monitorStackUpdationStatus()
    sys.exit()

def monitorStackDestroyStatus():
    currentStackResp = getStackStatus()
    if currentStackResp is not None and currentStackResp.stdout is not None and currentStackResp.returncode == 0:
        getSecretResponseJson = json.loads(currentStackResp.stdout.decode("utf-8"))
        currentStackStatus = getSecretResponseJson['Stacks'][0]["StackStatus"] 
        print("StackStatus ", currentStackStatus)
        while currentStackStatus != 'DELETE_COMPLETE':
            monitorStackDestroyStatus()
    sys.exit()



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
    handleOperation(operationName='Destroy Stack',response=deleteStackResponse)


def deleteBucket():
    '''
    aws s3 rb s3://your-bucket-name --force
    '''
    deleteBucketResponse = subprocess.run(
        [
            "aws",
            "s3",
            "rb",
            "s3://logs-bucket-test-1",
            "--force"
        ],
        capture_output=True,
    )
    handleOperation(operationName='Delete Bucket',response=deleteBucketResponse)

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
    handleOperation(operationName='Create Bucket',response=createBucketResponse)


def loadingAnimation(process) :
    while process.is_alive() :
        chars = "/—\|" 
        for char in chars:
            sys.stdout.write('\r'+'.. '+char)
            time.sleep(.1)
            sys.stdout.flush()



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
    if gateWayUrl == '':
        print("Stack creation is still in progress, please execute the command after few seconds")
    else:
        invoke_url=gateWayUrl + "/" + stage_name
        print("API gateway URL that can be invoked: ",invoke_url)

if __name__ == '__main__':
    # printBanner(banner="Lynx Lab")
    print('''
                            .-') _) (`-.                        ('-.    .-. .-')   
                           ( OO ) )( OO ).                     ( OO ).-.\  ( OO )  
 ,--.       ,--.   ,--.,--./ ,--,'(_/.  \_)-.       ,--.       / . --. / ;-----.\  
 |  |.-')    \  `.'  / |   \ |  |\ \  `.'  /        |  |.-')   | \-.  \  | .-.  |  
 |  | OO ) .-')     /  |    \|  | ) \     /\        |  | OO ).-'-'  |  | | '-' /_) 
 |  |`-' |(OO  \   /   |  .     |/   \   \ |        |  |`-' | \| |_.'  | | .-. `.  
(|  '---.' |   /  /\_  |  |\    |   .'    \_)      (|  '---.'  |  .-.  | | |  \  | 
 |      |  `-./  /.__) |  | \   |  /  .'.  \        |      |   |  | |  | | '--'  / 
 `------'    `--'      `--'  `--' '--'   '--'       `------'   `--' `--' `------'                                                                                                                                                                                                                                                           
    ''')
    if validateArgs(sys.argv[1:]):
        operation = sys.argv[1]
        print(f"Performing operation: [{operation}]")
        if operation == CREATE_OPERATION:
            createSecret()
            createBucket()
            createStack()
            loading_process = threading.Thread(target=monitorStackCreationStatus)
            loading_process.start()
            loadingAnimation(loading_process)
            loading_process.join()
            print("\n")
            print("Create operation compeleted!")
            print("Use operation getUrl (`python3 driver.py getUrl`) to get the api invocation URL")
        elif operation == DESTROY_OPERATION:
            deleteSecret()
            deleteBucket()
            destroyStack()
            loading_process = threading.Thread(target=monitorStackDestroyStatus)
            loading_process.start()
            loadingAnimation(loading_process)
            loading_process.join()
            print("\n")
            print("Destroy operation compeleted!")
        elif operation == GET_API_URL:
            getApiGateWayEndpoint()
        elif operation == UPDATE_OPERATION:
            updateStack()
            loading_process = threading.Thread(target=monitorStackUpdationStatus)
            loading_process.start()
            loadingAnimation(loading_process)
            loading_process.join()
            print("\n")
            print("Update operation compeleted!")


