import json


def lambda_handler(event, context):
    # Code here to load a user from dynamo
    user_id = event["pathParameters"]["userid"]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "email_address": "joe.bloggs@gmail.com",
                "last_login": 1545066160142,
                "user_id": user_id,
                "password": "hashed_password",
                "first_name": "Joe",
                "last_name": "Bloggs",
                "favourite_courses": [
                    "course_id_1",
                    "course_id_2",
                    "course_id_3"
                ]
            }
        ),
    }