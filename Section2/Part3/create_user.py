import json


def lambda_handler(event, context):
    request_body = event["body"]
    user_id = event["pathParameters"]["userid"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "you've asked me to create a new user with": request_body,
                "user_id is": user_id
            }
        ),
    }