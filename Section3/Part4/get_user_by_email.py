import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['USER_TABLE']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    email_address = event["pathParameters"]["email_address"]
    print("Loading email address " + email_address)
    user = __get_user_by_email(email_address)

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

def __get_user_by_email(email_address):
    response = table.query(
        IndexName='EmailIndex',
        KeyConditionExpression=Key('email_address').eq(email_address)
    )

    return response['Items'][0]
