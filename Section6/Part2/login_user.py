import hashlib
import json
import os
import time
import traceback
import uuid
import boto3
from boto3.dynamodb.conditions import Key
import random
import string
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
user_table_name = os.environ['USER_TABLE']
auth_table_name = os.environ['AUTH_TABLE']
user_table = dynamodb.Table(user_table_name)
auths_table = dynamodb.Table(auth_table_name)


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

    new_token = __set_auth_token(user_id)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "Auth token": new_token,
            }
        )
    }

def __get_user_by_id(user_id):
    response = user_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id))

    if len(response['Items']) != 1:
        return None

    return response['Items'][0]


def __encrypt_password(candidate_password):
    sha_signature = \
        hashlib.sha256(candidate_password.encode()).hexdigest()
    return sha_signature


def __set_auth_token(user_id):
    token = __token_generator()
    expiry_time = datetime.now() + timedelta(hours=48)

    auth_doc = {
        'user_id': user_id,
        'auth_token': token,
        'ExpiryTime': int(expiry_time.timestamp())
    }

    auths_table.put_item(Item=auth_doc)

    return token

def __token_generator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
