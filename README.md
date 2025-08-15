# LynxLab


### Pre requsities
1. Python3, pip3
2. aws cli


### Setup
1. Add secret id into the file secret.json
2. Set the value for APIGW_TOKEN , (export APIGW_TOKEN='*****')
3. Run python3 epicShelter.py create --> To create the stack
4. Run python3 epicShelter.py getUrl --> To get the invocation url
5. Sample usage of the model --> curl -s -X GET -H "Authorization: Bearer $APIGW_TOKEN" "<apiGetUrl>/invoke?inputText=What%20is%20the%20capital%20of%20India?
6. Run python3 epicShelter.py destroy --> To destroy the stack