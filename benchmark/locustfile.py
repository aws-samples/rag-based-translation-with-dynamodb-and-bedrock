import json
import time
import boto3
from locust import User, task, events, between
from botocore.config import Config
import random
import os
from benchmark_util import content_list, split_content

# AWS 配置
AWS_REGION = os.environ.get('region')
AWS_ACCESS_KEY_ID=os.environ.get('ak')
AWS_SECRET_ACCESS_KEY=os.environ.get('sk')
MODEL_ID = os.environ.get('model_id')
# 创建 AWS Lambda 客户端
LAMBDA_FUNCTION_NAME = 'translate_tool'

class CustomClient:
    def __init__(self):
        # 初始化你的 SDK 客户端
        self.lambda_client = boto3.client('lambda', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def invoke_translate(self, src_content, src_lang, dest_lang, model_id):
        # 封装 SDK 方法调用
        payload = {
            "src_content": src_content,
            "src_lang": src_lang,
            "dest_lang": dest_lang,
            "request_type": "translate",
            "dictionary_id" : 'RPG',
            "model_id": model_id
        }

        translate_response = self.lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        payload_json = json.loads(translate_response.get('Payload').read())

        return payload_json.get('result')


class CustomUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = CustomClient()

class MyUser(CustomUser):
    wait_time = between(1, 3)

    @task
    def my_task(self):
        start_time = time.time()
        try:
            random_item = random.choice(content_list)

            chunks = split_content(random_item[0])

            result = self.client.invoke_translate(chunks, random_item[1], random_item[2], MODEL_ID)
            
            # 处理结果
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="custom",
                name="invoke_translate",
                response_time=total_time,
                response_length=len(result),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="custom",
                name="invoke_translate",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )