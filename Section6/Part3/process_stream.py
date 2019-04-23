import json
import csv
import time
import os
import boto3

TEMP_FOLDER = '/tmp'

s3_bucket = os.environ['S3_BUCKET']
print("Using " + s3_bucket)


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        data_dict = get_data(record)
        temp_file_name = write_csv(data_dict)
        write_to_s3(temp_file_name)

    return 'Successfully processed {} records.'.format(len(event['Records']))

def get_data(record):
    dynamo_record = record['dynamodb']

    create_time = dynamo_record['ApproximateCreationDateTime']
    user_id = dynamo_record['Keys']['user_id']['S']
    email_address = dynamo_record['NewImage']['email_address']['S']
    first_name = dynamo_record['NewImage']['first_name']['S']
    last_name = dynamo_record['NewImage']['last_name']['S']
    last_login = dynamo_record['NewImage']['last_login']['N']

    data_dict = {
        "create_time": create_time,
        "user_id": user_id,
        "email_address": email_address,
        "first_name": first_name,
        "last_name": last_name,
        "last_login": last_login
    }
    return data_dict

def write_csv(data_dict):
    file_name = "users_" + str(time.time()) + " .csv"
    file_path = TEMP_FOLDER + "/" + file_name
    print("Writing CSV to " + file_path)
    with open(file_path, 'w') as f:
        w = csv.DictWriter(f, data_dict.keys())
        w.writeheader()
        w.writerow(data_dict)

    return file_name


def write_to_s3(file_name):
    file_path = TEMP_FOLDER + "/" + file_name
    print("Uploading " + file_path + " to " + s3_bucket)
    s3 = boto3.client('s3')
    s3.upload_file(file_path, s3_bucket, file_name)
