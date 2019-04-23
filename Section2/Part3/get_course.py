import json


def lambda_handler(event, context):
    course_id = event["pathParameters"]["courseid"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "course_id": course_id,
                "title": "Hands on with Dynamo",
                "publish_date": "01/01/2019",
                "author_name": "James Cross",
                "subject_area": "AWS",
                "course_rank": 1
            }
        ),
    }