import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
auth_table_name = os.environ['AUTH_TABLE']
auths_table = dynamodb.Table(auth_table_name)


def lambda_handler(event, context):
    headers = event["headers"]

    user_id = headers["user_id"]
    auth_token = headers["auth_token"]

    print("Loading user ID " + user_id)
    auths = __get_auths(user_id)

    auth_token_list = []
    for auth in auths:
        auth_token_list.append(auth["auth_token"])

    print(auth_token_list)
    
    if any(auth_token in s for s in auth_token_list):
        return {
            "statusCode": 200,
            "body": json.dumps({
                "Status": "Auth token is valid",
            })
        }
    else:
        return {
            "statusCode": 403,
        }
        
        
def __get_auths(user_id):
    response = auths_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id))

    return response['Items']
