import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['USER_TABLE']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    user_id = event["pathParameters"]["userid"]
    course_id = event["pathParameters"]["courseid"]

    last_login = __get_user_by_id(user_id)["last_login"]
    __add_course(user_id, last_login, course_id)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "Status": "User information updated"
            }
        ),
    }


def __add_course(user_id, last_login, course_id):
    response = table.update_item(
        Key={
            "user_id": user_id,
            "last_login": last_login
        },
        UpdateExpression="SET #attrName = list_append(#attrName, :course_id)",
        ExpressionAttributeNames={
            "#attrName": "fav_courses"
        },
        ExpressionAttributeValues={
            ":course_id": [course_id]
        },
        ReturnValues="UPDATED_NEW"
    )


def __get_user_by_id(user_id):
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    return response['Items'][0]
