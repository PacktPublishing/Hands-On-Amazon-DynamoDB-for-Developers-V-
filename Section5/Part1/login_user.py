import hashlib
import json
import os
import time
import traceback
import uuid
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['USER_TABLE']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    request_body = json.loads(event["body"])
    user_id = event["pathParameters"]["userid"]
    print("Loading user ID " + user_id)
    user = __get_user_by_id(user_id)

    print("User is " + str(user))

    if user is None:
        return {
            "statusCode": 404,
        }

    request_password = request_body["password"]
    encrypted_request_password = __encrypt_password(request_password)
    user_password = user["password"]

    if encrypted_request_password != user_password:
        return {
            "statusCode": 403,
        }

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "User ID": user["user_id"],
                "First Name": user["first_name"],
                "Last Name": user["last_name"],
                "Email Address": user["email_address"]
            }
        )
    }

def __get_user_by_id(user_id):
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    if len(response['Items']) != 1:
        return None

    return response['Items'][0]


def __encrypt_password(candidate_password):
    sha_signature = \
        hashlib.sha256(candidate_password.encode()).hexdigest()
    return sha_signature
