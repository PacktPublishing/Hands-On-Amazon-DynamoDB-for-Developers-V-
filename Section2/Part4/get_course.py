import json
import os
import traceback

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['COURSE_TABLE']
# table_name = "CourseTable"
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    print("Table name is " + table_name)
    course_id = event["pathParameters"]["courseid"]
    print("Course ID is " + course_id)
    course = __get_course_by_id(course_id)

    print("Course is " + str(course))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "course_id": course_id,
                "title": course["title"],
                "publish_date": course["publish_date"],
                "author_name": course["author_name"],
                "subject_area": course["subject_area"]
            }
        ),
    }


def __get_course_by_id(course_id):
    try:
        response = table.query(
            KeyConditionExpression=Key('course_id').eq(course_id)
        )
    except:
        print("Failed to write user to Dynamo")
        traceback.print_exc()

    return response['Items'][0]
