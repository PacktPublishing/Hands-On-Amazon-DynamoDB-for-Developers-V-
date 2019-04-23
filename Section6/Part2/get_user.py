import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['USER_TABLE']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    user_id = event["pathParameters"]["userid"]
    print("Loading user ID " + user_id)
    user = __get_user_by_id(user_id)

    print("User is " + str(user))

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

    return response['Items'][0]

