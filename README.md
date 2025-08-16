# LynxLab


### Pre requsities
1. Python3, pip3
2. aws cli


### Setup
1. pip install -r requirements.txt
2. Need to configure ~/.aws/config
    [default]
    region = <your-region>
    aws_access_key_id = <your-secret-key-id>
    aws_secret_access_key = <your-secret-access-key>
3. Set the value for APIGW_TOKEN , (export APIGW_TOKEN='*****')
4. Run python3 driver.py create --> To create the stack
5. Run python3 driver.py getUrl --> To get the invocation url
6. Sample usage of the model --> curl -s -X GET -H "Authorization: Bearer $APIGW_TOKEN" "<apiGetUrl>/invoke?inputText=What%20is%20the%20capital%20of%20India?
7. Run python3 driver.py destroy --> To destroy the stack