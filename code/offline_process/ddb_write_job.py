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

args = getResolvedOptions(sys.argv, ['bucket', 'object_key','REGION'])
s3 = boto3.resource('s3')
bucket = args['bucket']
object_key = args['object_key']

REGION = args['REGION']

bedrock = boto3.client(service_name='bedrock-runtime',
                       region_name=REGION)

dynamodb = boto3.resource('dynamodb', REGION)
ddb_en_table = dynamodb.Table('rag_translate_en_table')
ddb_chs_table = dynamodb.Table('rag_translate_chs_table')

publish_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ingest_all_items(file_content, object_key):
    json_obj = json.loads(file_content)
    file_name = object_key.split('/')[-1].replace('.json', '')

    if json_obj["type"] == "multilingual_terminology":
        arr = json_obj["data"]
        doc_type = json_obj["type"]
        author = json_obj.get("author","")

        en_data = {}
        for item in arr:
            if 'EN' in item['mapping'].keys():
                key = item['mapping']['EN']
                en_data[key] = item

        chs_data = {}
        for item in arr:
            if 'CHS' in item['mapping'].keys():
                key = item['mapping']['CHS']
                chs_data[key] = item


        en_data_size = len(en_data.keys())
        print(f"en_data_size: {en_data_size}")

        chs_data_size = len(chs_data.keys())
        print(f"chs_data_size: {chs_data_size}")

        with ddb_en_table.batch_writer() as batch:
            for en_key, en_value in en_data.items():
                en_item = {
                    'term': en_key,
                    'entity': en_value['entity_type'],
                    'mapping' : en_value['mapping'],
                }
                batch.put_item(Item=en_item)

        with ddb_chs_table.batch_writer() as batch:
            for chs_key, chs_value in chs_data.items():
                chs_item = {
                    'term': chs_key,
                    'entity': chs_value['entity_type'],
                    'mapping' : chs_value['mapping']
                }
                batch.put_item(Item=chs_item)

        print("ingest {} term to ddb".format(en_data_size+chs_data_size))

def load_content_json_from_s3(bucket, object_key):
    if object_key.endswith('.json'):
        obj = s3.Object(bucket, object_key)
        file_content = obj.get()['Body'].read().decode('utf-8', errors='ignore').strip()
    else:
        raise RuntimeError("Invalid S3 File Format")
        
    return file_content

def WriteTermToDDB(bucket, object_key):
    file_content = load_content_json_from_s3(bucket, object_key)
    ingest_all_items(file_content, object_key)

def process_s3_uploaded_file(bucket, object_key):
    print("********** object_key : " + object_key)
    #if want to use different aos index, the object_key format should be: ai-content/company/username/filename

    WriteTermToDDB(bucket, object_key)

    

##如果是从chatbot上传，则是ai-content/username/filename
def get_filename_from_obj_key(object_key):
    paths = object_key.split('/')
    return paths[1] if len(paths) > 2 else 's3_upload'

for s3_key in object_key.split(','):
    s3_key = urllib.parse.unquote(s3_key) ##In case Chinese filename
    s3_key = s3_key.replace('+',' ') ##replace the '+' with space. ps:if the original file name contains space, then s3 notification will replace it with '+'.
    print("processing {}".format(s3_key))
    process_s3_uploaded_file(bucket, s3_key)