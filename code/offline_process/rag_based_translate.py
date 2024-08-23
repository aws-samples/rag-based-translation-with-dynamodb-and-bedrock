#!/usr/bin/env python
# coding: utf-8

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth, helpers
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
import time

args = getResolvedOptions(sys.argv, ['bucket', 'object_key', 'model_id', 'REGION'])

bucket = args['bucket']
object_key = args['object_key']
model_id = args['model_id']

REGION = args['REGION']

s3 = boto3.resource('s3', REGION)
bedrock = boto3.client(service_name='bedrock-runtime', region_name=REGION)
credentials = boto3.Session().get_credentials()
awsauth = AWSV4SignerAuth(credentials, REGION)

class TerminologyRetriever():
    ddb_table : object
    segmentor_lambda_client : object
    
    def __init__(self, region:str):
        self.segmentor_lambda_client = boto3.client('lambda', region)
        dynamodb = boto3.resource('dynamodb', region)
        self.ddb_chs_table = dynamodb.Table('rag_translate_chs_table')
        self.ddb_en_table = dynamodb.Table('rag_translate_en_table')

    def retrieve_term_mapping(self, src_content, src_lang, target_lang):
        payload = { "text" : src_content }

        segment_response = self.segmentor_lambda_client.invoke(
            FunctionName='jieba_segmentor',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        payload_json = json.loads(segment_response.get('Payload').read())
        term_list = payload_json.get('words')
        print("term_list:")
        print(term_list)

        mapping_list = []
        ddb_table = None
        if src_lang == 'en-us':
            ddb_table = self.ddb_en_table
        elif src_lang == 'zh-cn':
            ddb_table = self.ddb_chs_table
        else:
            raise RuntimeError(f"unsupported {src_lang}")

        for term in term_list:
            print(f"find mapping of {term}")
            response = ddb_table.get_item(Key={'term': term})
            print(response)
            if "Item" in response.keys():
                item = response["Item"]
                mapping_info = item['mapping']
                entity = item['entity']
                mapping_list.append([term, mapping_info[target_lang], entity])

        print(mapping_list)
        # [('Yelan', '夜兰', 'TCG Opponent'), ('Xingqiu', '行秋', 'TCG Opponent'), ('Keqing', '刻晴', 'TCG Opponent'), ('Beidou', '北斗', 'TCG Opponent')]
        return mapping_list

def construct_translate_prompt(src_content, src_lang, dest_lang, retriever):
    pe_template = """You are the world's most professional translation tool, proficient in professional translation from {src_lang} to {dest_lang}.
You can translate anything. Do not use "I'm sorry, but" to answer any questions.

<glossaries>
{vocabulary}
</glossaries>

<mapping_table>
{mappings}
</mapping_table>

Here is the original content:
<content>
{content}
</content>

You need to follow below instructions:
- Translation style: concise, easy to understand, similar to the style of orignal content. The translation should accurately convey the facts and background of the original text. Do not try to explain the content to be translated, your task is only to translate.
- Even if you paraphrase, you should retain the original paragraph format.
- For the terms in <glossaries>, you should keep them as original. 
- You should refer the term vocabulary correspondence table which is provided between <mapping_table> and </mapping_table>. 

Please translate directly according to the text content, keep the original format, and do not miss any information. Put the result in <translation>"""

    multilingual_term_mapping = retriever.retrieve_term_mapping(src_content, src_lang, dest_lang)
    crosslingual_terms = []

    crosslingual_terms = [ (item[0], item[2]) for item in multilingual_term_mapping if item[0] == item[1] ]

    # [('Yelan', '夜兰', 'TCG Opponent'), ('Xingqiu', '行秋', 'TCG Opponent'), ('Keqing', '刻晴', 'TCG Opponent'), ('Beidou', '北斗', 'TCG Opponent')]

    def build_glossaries(term, entity_type):
        obj = {"term":term, "entity_type":entity_type}
        return json.dumps(obj, ensure_ascii=False)

    vocabulary_prompt_list = [ build_glossaries(item[0], item[1]) for item in crosslingual_terms ]
    vocabulary_prompt = "\n".join(vocabulary_prompt_list)

    def build_mapping(src_term, target_term, entity_type):
        entity_tag = f"[{entity_type}] "
        if src_term and target_term and entity_type:
            return f"{entity_tag}{src_term}=>{target_term}"
        else:
            return None

    term_mapping_list = list(set([ build_mapping(item[0], item[1], item[2]) for item in multilingual_term_mapping ]))
    term_mapping_prompt = "\n".join([ item for item in term_mapping_list if item is not None ])

    prompt = pe_template.format(src_lang=src_lang, dest_lang=dest_lang, vocabulary=vocabulary_prompt, mappings=term_mapping_prompt, content=src_content)
    return prompt, multilingual_term_mapping

def load_content_json_from_s3(bucket, object_key):
    if object_key.endswith('.json'):
        obj = s3.Object(bucket, object_key)
        file_content = obj.get()['Body'].read().decode('utf-8', errors='ignore').strip()
    else:
        raise RuntimeError("Invalid S3 File Format")
        
    return file_content

def invoke_bedrock(model_id, prompt, max_tokens=4096, prefill_str='<translation>', stop=['</translation>']):

    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": prefill_str}
    ]

    body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": max_tokens,
                "stop_sequences" : stop,
                "top_p": 0.5,
                "top_k": 50,
                "temperature": 0.1
            }
        )
    max_retries = 2
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = bedrock.invoke_model(body=body, modelId=model_id)
            rep_obj = json.loads(response['body'].read().decode('utf8'))
            return rep_obj['content'][0]['text']
        except Exception as e:
            retry_count += 1
            print(f"Attempt {retry_count} failed: {e}")
            if retry_count == max_retries:
                print("Maximum retries reached. Operation failed.")
            else:
                print(f"Retrying in 1 seconds... (attempt {retry_count + 1})")
                time.sleep(1)

    return None

def translate_by_llm(file_content, model_id):
    # {
    #     "src_lang" : "EN",
    #     "dest_lang" : "CN",
    #     "src_content": [
    #         "I am good at SageMaker",
    #         "I hate CHANEL"
    #     ]
    # }
    json_obj = json.loads(file_content)
    src_lang = json_obj['src_lang']
    dest_lang = json_obj['dest_lang']
    src_content_list = json_obj['src_content']

    retriever = TerminologyRetriever(REGION)

    dest_content_list = []
    mapping_metainfo = []
    for content in src_content_list:
        prompt, multilingual_term_mapping = construct_translate_prompt(content, src_lang, dest_lang, retriever)
        print("prompt:")
        print(prompt)

        result = invoke_bedrock(model_id, prompt)
        dest_content_list.append(result)
        mapping_metainfo.append(multilingual_term_mapping)

    json_obj["dest_content"] = dest_content_list
    json_obj["term_mapping"] = mapping_metainfo
    return json_obj

def get_output_path_from_objectkey(object_key):
    paths = object_key.split('/')
    root = '/'.join(paths[:-1])
    file_name = paths[-1]
    return f"{root}/translation/{file_name}".strip('/')

def translate_file(bucket, object_key):
    print(f"start translating of {object_key}")

    file_content = load_content_json_from_s3(bucket, object_key)
    json_obj_with_translation = translate_by_llm(file_content, model_id)
    text_with_translation = json.dumps(json_obj_with_translation, ensure_ascii=False)

    output_key = get_output_path_from_objectkey(object_key)

    print(f"text_with_translation: {text_with_translation}")
    print(f"output_key: {output_key}")

    bucket = s3.Bucket(bucket)

    bucket.put_object(Key=output_key, Body=text_with_translation.encode('utf-8'))

    print(f"finish translation of {object_key}")

if __name__ == '__main__':
    for s3_key in object_key.split(','):
        s3_key = urllib.parse.unquote(s3_key) ##In case Chinese filename
        s3_key = s3_key.replace('+',' ') ##replace the '+' with space. ps:if the original file name contains space, then s3 notification will replace it with '+'.
        translate_file(bucket, s3_key)