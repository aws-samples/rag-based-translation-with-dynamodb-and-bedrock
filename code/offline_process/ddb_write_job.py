#!/usr/bin/env python
# coding: utf-8

import boto3
import random
import json
from awsglue.utils import getResolvedOptions
import sys
import hashlib
import datetime
import re
import os
import itertools
import logging
import urllib.parse
import numpy as np
from urllib.parse import unquote
from datetime import datetime

args = getResolvedOptions(sys.argv, ['bucket', 'object_key','REGION', 'table_name'])
s3 = boto3.resource('s3')
BUCKET = args['bucket']
OBJECT_KEY = args['object_key']
TABLE_NAME = args['table_name']

REGION = args['REGION']

bedrock = boto3.client(service_name='bedrock-runtime',
                       region_name=REGION)

dynamodb = boto3.resource('dynamodb', REGION)

publish_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def table_exists(table_name):
    try:
        dynamodb.describe_table(TableName=table_name)
        return True
    except Exception as e:
        print(f"Error table_exists: {str(e)}")
        return False

def create_dynamodb_table_if_not_exist(table_name):
    if not table_exists(table_name):
        try:
            response = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'term',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'term',
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            print("Table created successfully.")
        except Exception as e:
            print(f"Error creating table: {str(e)}")
    else:
        print(f"Table {table_name} already exists. Skipping creation.")

def update_dictionary_keys(table_name, bucket, object_key, key_list):
    try:
        s3 = boto3.client('s3')

        path = os.path.dirname(object_key)

        dict_file_path = f"{path}/{table_name}/user_dict.txt"

        def file_exists(bucket, key):
            response = s3.list_objects_v2(Bucket=bucket, Prefix=key, MaxKeys=1)
            return 'Contents' in response

        content = ''
        if file_exists(bucket, dict_file_path):
            response = s3.get_object(Bucket=bucket, Key=dict_file_path)
            content = response['Body'].read().decode('utf-8')

        if content:
            content += "\n"
        content += '\n'.join(key_list)

        # 写入文件
        s3.put_object(Bucket=bucket, Key=dict_file_path, Body=content)
    except Exception as e:
        print(f"update_dictionary_keys Err: {str(e)}")

def ingest_all_items(file_content, object_key):
    json_obj = json.loads(file_content)
    file_name = object_key.split('/')[-1].replace('.json', '')
    key_list = []

    if json_obj["type"] == "multilingual_terminology":
        arr = json_obj["data"]
        doc_type = json_obj["type"]
        author = json_obj.get("author","")

        kv_data = {}
        for item in arr:
            for key, value in item['mapping'].items():
                kv_data[value] = item

        update_dictionary_keys(table_name=TABLE_NAME, bucket=BUCKET, object_key=object_key, key_list=kv_data.keys())
        kv_data_size = len(kv_data.keys())
        print(f"kv_data_size: {kv_data_size}")

        ddb_table = dynamodb.Table(TABLE_NAME)
        with ddb_table.batch_writer() as batch:
            for key, value in kv_data.items():
                ddb_item = {
                    'term': key,
                    'entity': value['entity_type'],
                    'mapping' : value['mapping'],
                }
                batch.put_item(Item=ddb_item)

        print("ingest {} term to ddb".format(kv_data_size))

def load_content_json_from_s3(bucket, object_key):
    if object_key.endswith('.json'):
        obj = s3.Object(bucket, object_key)
        file_content = obj.get()['Body'].read().decode('utf-8', errors='ignore').strip()
    else:
        raise RuntimeError("Invalid S3 File Format")
        
    return file_content

def process_s3_uploaded_file(bucket, object_key):
    print("********** object_key : " + object_key)
    file_content = load_content_json_from_s3(bucket, object_key)
    ingest_all_items(file_content, object_key)

##如果是从chatbot上传，则是ai-content/username/filename
def get_filename_from_obj_key(object_key):
    paths = object_key.split('/')
    return paths[1] if len(paths) > 2 else 's3_upload'

for s3_key in OBJECT_KEY.split(','):
    s3_key = urllib.parse.unquote(s3_key) ##In case Chinese filename
    s3_key = s3_key.replace('+',' ') ##replace the '+' with space. ps:if the original file name contains space, then s3 notification will replace it with '+'.
    print("processing {}".format(s3_key))
    create_dynamodb_table_if_not_exist(TABLE_NAME)
    process_s3_uploaded_file(BUCKET, s3_key)