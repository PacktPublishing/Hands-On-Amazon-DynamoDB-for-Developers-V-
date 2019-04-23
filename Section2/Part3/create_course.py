import json


def lambda_handler(event, context):
    request_body = event["body"]
    course_id = event["pathParameters"]["courseid"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "you've asked me to create a new course with": request_body,
                "course_id is": course_id
            }
        ),
    }