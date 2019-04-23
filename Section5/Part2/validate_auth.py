import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['USER_TABLE']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    headers = event["headers"]

    user_id = headers["user_id"]
    auth_token = headers["auth_token"]

    print("Loading user ID " + user_id)
    user = __get_user_by_id(user_id)

    if user["auth_token"] != auth_token:
        return {
            "statusCode": 403,
        }
    else:
      return {
          "statusCode": 200,
          "body": json.dumps({
              "Status": "Auth token is valid",
          })
      }


def __get_user_by_id(user_id):
    response = table.query(KeyConditionExpression=Key('user_id').eq(user_id))

    return response['Items'][0]
