import hashlib
import json
import os
import time
import traceback
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
# table_name = os.environ['USER_TABLE']
table_name = "UsersTable"
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    request_body = json.loads(event["body"])

    email_address = request_body["email_address"]
    first_name = request_body["first_name"]
    last_name = request_body["last_name"]
    password = request_body["password"]

    new_user = __create_user(email_address, password, first_name, last_name)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "You've asked me to create a new user with": new_user,
            }
        ),
    }


def __create_user(email_address, password, first_name, last_name):
    print("Using DynamoDB table: " + table_name)

    last_login = int(round(time.time() * 1000))
    user_doc = {
        'user_id': str(uuid.uuid4().hex),
        'email_address': email_address,
        'first_name': first_name,
        'last_name': last_name,
        'password': str(__encrypt_password(password)),
        'last_login': last_login,
        'fav_courses': []
    }

    print("Will write " + str(user_doc))

    try:
        table.put_item(Item=user_doc)

    except:
        print("Failed to write user to Dynamo")
        traceback.print_exc()

    return user_doc


def __encrypt_password(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

__create_user("New", "New", "New", "New")
