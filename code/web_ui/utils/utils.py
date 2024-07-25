import boto3
import json
import random
import datetime
import time
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

# 加载 .env 文件中的变量
load_dotenv()

deploy_region = os.getenv('CDK_DEFAULT_REGION')
upload_bucket = os.getenv("UPLOAD_BUCKET")
# region='us-west-2'
TABLE_PREFIX = 'translate_mapping_'

def list_translate_models():
    bedrock = boto3.client(service_name='bedrock', region_name=deploy_region)
    response = bedrock.list_foundation_models()
    response['modelSummaries']
    def check_model(model_id) -> bool:
        legacy_models = ['anthropic.claude-instant-v1', 'anthropic.claude-v2:1', 'anthropic.claude-v2']
        if not model_id.startswith('anthropic.'):
            return False 
        elif model_id.endswith('k'):
            return False
        elif model_id in legacy_models:
            return False 
        return True
    return [ model_info['modelId'] for model_info in response['modelSummaries'] if check_model(model_info['modelId']) ]

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

def list_translate_mapping_tables():
    # 创建 DynamoDB 客户端
    dynamodb = boto3.client('dynamodb', region_name=deploy_region)

    # 用于存储匹配的表名
    translate_mapping_tables = []

    # 初始化分页标记
    paginator = dynamodb.get_paginator('list_tables')
    page_iterator = paginator.paginate()

    # 遍历所有页面
    for page in page_iterator:
        for table_name in page['TableNames']:
            if table_name.startswith(TABLE_PREFIX):
                translate_mapping_tables.append(table_name.removeprefix(TABLE_PREFIX))

    return translate_mapping_tables

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

def get_random_item(table_name:str):
    # 创建 DynamoDB 客户端
    dynamodb = boto3.resource('dynamodb', region_name=deploy_region)
    real_table_name = f"{TABLE_PREFIX}{table_name}"
    ddb_table = dynamodb.Table(real_table_name)

    try:
        # 扫描整个表
        response = ddb_table.scan()
        items = response['Items']

        # 如果表不为空，随机选择一个项目
        if items:
            random_item = random.choice(items)
            return random_item
        else:
            return None

    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

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
    result = translate_content(
        content='奇怪的渔人吐司可以达到下面效果，队伍中所有角色防御力提高88点，持续300秒。多人游戏时，仅对自己的角色生效。《原神手游》赤魔王图鉴，赤魔王能捉吗', 
        source_lang='CHS', 
        target_lang='EN',
        dictionary_id='dictionary_1')
    print(f"result: {result}")

    tables = list_translate_mapping_tables()
    print(f"tables: {tables}")

    term_item = query_term("dictionary_1", "奇怪的渔人吐司")
    print("term_item:")
    print(term_item)

    random_item = get_random_item("dictionary_1")
    print("random_item")
    print(random_item)

    new_mapping_info = {        
        "CHS" : "奇怪的渔人吐司",
        "CHT" : "奇怪的漁人吐司",
        "DE" : "Misslungene Fischerschnitte",
        "EN" : "Suspicious Fisherman’s Toast",
        "ES" : "Tostada del pescador extraña",
        "FR" : "Toast du pêcheur (suspect)",
        "ID" : "Suspicious Fisherman’s Toast",
        "IT" : "Toast del pescatore sospetto",
        "JP" : "微妙な漁師トースト",
        "KR" : "이상한 어부 토스트",
        "PT" : "Torrada do Pescador Estranha",
        "RU" : "Странный рыбацкий бутерброд",
        "TH" : "Fisherman’s Toast รสประหลาด",
        "TR" : "Balıkçı Tostu (Tuhaf)",
        "VI" : "Bánh Người Cá Kỳ Lạ"
    }
    update_term_mapping("dictionary_1", "奇怪的渔人吐司", 'Character', new_mapping_info)
