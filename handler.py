import json
import boto3
import os
import pprint
import StringIO

bucket = "waraiotoko"
s3 = boto3.client('s3')

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    pprint.pprint(event)

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        img_path = '/tmp/' + key
        s3.download_file(bucket, key, img_path)
        with open(img_path) as img_file:
            print('opened!')
            #pprint.pprint(img_file)
            #print(img_file.read())
