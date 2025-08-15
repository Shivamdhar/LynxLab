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
3. Add secret id into the file secret.json
4. Set the value for APIGW_TOKEN , (export APIGW_TOKEN='*****')
5. Run python3 epicShelter.py create --> To create the stack
6. Run python3 epicShelter.py getUrl --> To get the invocation url
7. Sample usage of the model --> curl -s -X GET -H "Authorization: Bearer $APIGW_TOKEN" "<apiGetUrl>/invoke?inputText=What%20is%20the%20capital%20of%20India?
8. Run python3 epicShelter.py destroy --> To destroy the stack