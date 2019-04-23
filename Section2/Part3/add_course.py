import json


def lambda_handler(event, context):
    user_id = event["pathParameters"]["userid"]
    course_id = event["pathParameters"]["courseid"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "You've asked me to add a new course to user ": user_id,
                "With course_id": course_id
            }
        ),
    }