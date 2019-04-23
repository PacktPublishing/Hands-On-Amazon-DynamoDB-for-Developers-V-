import json
import os
import traceback
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['COURSE_TABLE']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    request_body = json.loads(event["body"])

    title = request_body["title"]
    publish_date = request_body["publish_date"]
    author_name = request_body["author_name"]
    subject_area = request_body["subject_area"]

    new_course = __create_course(title, publish_date, author_name, subject_area)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "you've asked me to create a new course with": request_body,
                "Details saved": new_course
            }
        ),
    }


def __create_course(title, publish_date, author_name, subject_area):
    course_doc = {
        'course_id': str(uuid.uuid4().hex),
        'title': title,
        'publish_date': publish_date,
        'author_name': author_name,
        'subject_area': subject_area
    }

    try:
        table.put_item(Item=course_doc)

    except:
        print("Failed to write user to Dynamo")
        traceback.print_exc()

    return course_doc
