import boto3
import json

REGION = 'us-west-2'
MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

def translate_content(content, source_lang, target_lang, region=REGION, model_id=MODEL_ID):
    lambda_client = boto3.client('lambda', region)
    payload = {
        "src_content": content,
        "src_lang": source_lang,
        "dest_lang": target_lang,
        "request_type": "translate",
        "model_id": model_id
    }

    print(payload)
    translate_response = lambda_client.invoke(
        FunctionName='translate_tool',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    payload_json = json.loads(translate_response.get('Payload').read())
    print(payload_json)
    return payload_json.get('result')

        
    #     term_list = payload_json.get('words')
    #     print("term_list:")
    #     print(term_list)
    # result = translate.translate_text(
    #     Text=content,
    #     SourceLanguageCode=source_lang,
    #     TargetLanguageCode=target_lang
    # )
    # print(f'Translated content from {source_lang} to {target_lang}: {result["TranslatedText"]}')
    # return result['TranslatedText']

if __name__ == '__main__':
    result = translate_content('奇怪的渔人吐司可以达到下面效果，队伍中所有角色防御力提高88点，持续300秒。多人游戏时，仅对自己的角色生效。《原神手游》赤魔王图鉴，赤魔王能捉吗', 'CHS', 'EN')
    print(result)