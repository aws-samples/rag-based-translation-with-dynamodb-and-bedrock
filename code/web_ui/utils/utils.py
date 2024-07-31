import boto3
import json
import random
import datetime
import time
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import yaml

load_dotenv()

config_yaml_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_yaml_path, 'r') as f:
    config_data = yaml.safe_load(f)
    

deploy_region = boto3.session.Session().region_name
upload_bucket = os.getenv("UPLOAD_BUCKET")
TABLE_PREFIX = 'translate_mapping_'

def list_translate_models():
    """
    Retrieve a list of bedrock model IDs from config.yaml

    Returns:
        list: A list of model IDs
    """
    return config_data['supportedmodel']

def list_supported_language_codes():
    """
    Retrieve a list of supported language codes from config.yaml

    Returns:
        list: A list of supported languages
    """
    return list(config_data['supportedlang'].values())

def list_dictionary_ids():
    """
    Retrieve a list of dictionary IDs from DynamoDB tables.

    This function connects to DynamoDB, lists all tables, and filters for tables
    that start with a specific prefix. It then extracts and returns the dictionary
    IDs from these table names.

    Returns:
        list: A list of dictionary IDs extracted from the table names.
    """
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb', region_name=deploy_region)

    # Initialize an empty list to store the extracted dictionary IDs
    translate_mapping_tables = []

    # Create a paginator for the list_tables operation
    # This allows us to handle cases where there are many tables
    paginator = dynamodb.get_paginator('list_tables')
    page_iterator = paginator.paginate()

    # Iterate through each page of results
    for page in page_iterator:
        # For each table name in the current page
        for table_name in page['TableNames']:
            # Check if the table name starts with our specified prefix
            if table_name.startswith(TABLE_PREFIX):
                # If it does, remove the prefix and add the remainder (the ID) to our list
                translate_mapping_tables.append(table_name.removeprefix(TABLE_PREFIX))

    # Return the list of extracted dictionary IDs
    return translate_mapping_tables

def translate_content(contents, source_lang, target_lang, dictionary_id, model_id):
    lambda_client = boto3.client('lambda', region_name=deploy_region)
    payload = {
        "src_contents": contents,
        "src_lang": source_lang,
        "dest_lang": target_lang,
        "request_type": "translate",
        "dictionary_id" : dictionary_id,
        "model_id": model_id,
        "response_with_term_mapping" : True,
        "max_content_length" : 65535
    }

    translate_response = lambda_client.invoke(
        FunctionName='translate_tool',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    payload_json = json.loads(translate_response.get('Payload').read())
    if 'translations' in payload_json:
        result = payload_json['translations'][0]
        term_mapping = result.get('term_mapping')
        term_mapping_list = [ f"{tup[0]}=>{tup[1]}({tup[2]})" for tup in term_mapping ]
        return result.get('translated_text'), '\n'.join(term_mapping_list)
    else:
        return payload_json.get("error"), ""



def query_term(table_name, term):
    # 创建 DynamoDB 资源
    dynamodb = boto3.resource('dynamodb', region_name=deploy_region)
    
    # 获取表对象
    real_table_name = f"{TABLE_PREFIX}{table_name}"
    ddb_table = dynamodb.Table(real_table_name)
    
    try:
        response = ddb_table.get_item(Key={'term': term})
        if "Item" in response.keys():
            item = response["Item"]

            return item
    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return None, None

def update_term_mapping(table_name:str, term:str, entity:str, mapping_info:dict):
    dynamodb = boto3.resource('dynamodb', region_name=deploy_region)
    
    # 获取表对象
    real_table_name = f"{TABLE_PREFIX}{table_name}"
    ddb_table = dynamodb.Table(real_table_name)

    ddb_item = {
        'term': term,
        'entity': entity,
        'mapping' : mapping_info,
    }

    response = ddb_table.put_item(
        Item=ddb_item
    )

    print(response)

def delete_term(table_name:str, term:str):
    dynamodb = boto3.resource('dynamodb', region_name=deploy_region)

    real_table_name = f"{TABLE_PREFIX}{table_name}"
    ddb_table = dynamodb.Table(real_table_name)
    response = ddb_table.delete_item(
        Key={
            'PartitionKey': term
        }
    )
    print(response)


def upload_to_s3(local_file, bucket_name, s3_key):
    try:
        s3 = boto3.client('s3', region_name=deploy_region)
        s3.upload_fileobj(local_file, bucket_name, s3_key)
        return True, "Finish Uploading to S3"
    except Exception as e:
        return False, str(e)

def start_glue_job(key_path, bucket, dictionary_name, job_name='ingest_knowledge2ddb'):
    glue = boto3.client('glue', region_name=deploy_region)

    publish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    print('start job for {} at {}'.format(key_path, str(publish_date)))   
    response = glue.start_job_run(
        JobName=job_name,
        Arguments={
            '--additional-python-modules': 'boto3>=1.28.52,botocore>=1.31.52',
            '--dictionary_name': dictionary_name,
            '--object_key': key_path,
            '--bucket': bucket,
            })  
    return response['JobRunId']

def get_glue_job_run_status(run_id, job_name='ingest_knowledge2ddb'):
    # 创建 Glue 客户端
    glue_client = boto3.client('glue', region_name=deploy_region)
    
    try:
        # 获取 job 运行的详细信息
        response = glue_client.get_job_run(
            JobName=job_name,
            RunId=run_id
        )
        
        # 从响应中提取状态
        job_status = response['JobRun']['JobRunState']
        
        return job_status
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == '__main__':
    pass
    # result = translate_content(
    #     contents=['奇怪的渔人吐司可以达到下面效果，队伍中所有角色防御力提高88点，持续300秒。','多人游戏时，仅对自己的角色生效。《原神手游》赤魔王图鉴，赤魔王能捉吗'], 
    #     source_lang='CHS', 
    #     target_lang='EN',
    #     dictionary_id='dictionary_1',
    #     model_id='anthropic.claude-3-haiku-20240307-v1:0')
    # print(f"result: {result}")

    # tables = list_translate_mapping_tables()
    # print(f"tables: {tables}")

    # term_item = query_term("dictionary_1", "奇怪的渔人吐司")
    # print("term_item:")
    # print(term_item)

    # random_item = get_random_item("dictionary_1")
    # print("random_item")
    # print(random_item)

    # new_mapping_info = {        
    #     "CHS" : "奇怪的渔人吐司",
    #     "CHT" : "奇怪的漁人吐司",
    #     "DE" : "Misslungene Fischerschnitte",
    #     "EN" : "Suspicious Fisherman’s Toast",
    #     "ES" : "Tostada del pescador extraña",
    #     "FR" : "Toast du pêcheur (suspect)",
    #     "ID" : "Suspicious Fisherman’s Toast",
    #     "IT" : "Toast del pescatore sospetto",
    #     "JP" : "微妙な漁師トースト",
    #     "KR" : "이상한 어부 토스트",
    #     "PT" : "Torrada do Pescador Estranha",
    #     "RU" : "Странный рыбацкий бутерброд",
    #     "TH" : "Fisherman’s Toast รสประหลาด",
    #     "TR" : "Balıkçı Tostu (Tuhaf)",
    #     "VI" : "Bánh Người Cá Kỳ Lạ"
    # }
    # update_term_mapping("dictionary_1", "奇怪的渔人吐司", 'Character', new_mapping_info)
