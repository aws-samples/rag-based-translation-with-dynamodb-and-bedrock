import boto3
import json
import os

# AWS 配置
AWS_REGION = os.environ.get('region')
AWS_ACCESS_KEY_ID=os.environ.get('ak')
AWS_SECRET_ACCESS_KEY=os.environ.get('sk')
MODEL_ID = os.environ.get('model_id')
# 创建 AWS Lambda 客户端
LAMBDA_FUNCTION_NAME = 'translate_tool'
DICT_ID='test1'

class CustomClient:
    def __init__(self):
        # 初始化你的 SDK 客户端
        # self.lambda_client = boto3.client('lambda', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.lambda_client = boto3.client('lambda', region_name='ap-southeast-1')
        
    def invoke_translate(self, src_contents, src_lang, dest_lang, model_id):
        # 封装 SDK 方法调用
        payload = {
            "src_contents": src_contents,
            "src_lang": src_lang,
            "dest_lang": dest_lang,
            "request_type": "translate",
            "dictionary_id" : DICT_ID,
            "model_id": model_id
        }

        translate_response = self.lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        payload_json = json.loads(translate_response.get('Payload').read())

        return payload_json.get('translations')

chunks = [
    "Full on auto!\nGot this team on auto and got full stars!The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~",
    "Perfect Coin Flip\nKaeya’s idle animations are my favorite!\n\n(I think I was trying to capture Chenyu Vale at a distance, but at least you can see Fontaine from here!"
]

client = CustomClient()

result = client.invoke_translate(chunks, 'en-us', 'zh-cn', 'us.anthropic.claude-3-haiku-20240307-v1:0')
print(result)

# from benchmark_util import content_list

# print(set([ item[2] for item in content_list]))


