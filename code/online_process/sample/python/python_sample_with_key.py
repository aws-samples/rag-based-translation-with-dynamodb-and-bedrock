import boto3
import json
from typing import Dict, Any, List

# AWS and model configuration
REGION = 'ap-southeast-1'
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
DICTIONARY_ID = 'dict_1'
SOURCE_LANG = 'EN'
TARGET_LANG = 'CHS'
LAMBDA_FUNCTION_NAME = 'translate_tool'
AK = 'XXXXXX'
SK = 'YYYYYY'
def create_lambda_client(region: str, ak:str, sk:str) -> boto3.client:
    """
    Create and return a boto3 Lambda client.
    
    :param region: AWS region name
    :param ak: aws_access_key_id
    :param sk: aws_secret_access_key
    :return: boto3 Lambda client
    """
    # return boto3.client('lambda', region_name=region)
    return boto3.client('lambda', region_name=region, aws_access_key_id=ak,
                        aws_secret_access_key=sk)

def create_payload(contents: List[str], src_lang: str, dest_lang: str, dictionary_id: str, model_id: str, response_with_term_mapping: bool=False) -> Dict[str, Any]:
    """
    Create the payload for the Lambda function.
    
    :param contents: List of content strings to be translated
    :param src_lang: Source language code
    :param dest_lang: Target language code
    :param dictionary_id: Dictionary ID for translation
    :param model_id: Model ID for translation
    :param response_with_term_mapping: Flag to include term mapping in the response
    :return: Dictionary containing the payload
    """
    return {
        "src_contents": contents,
        "src_lang": src_lang,
        "dest_lang": dest_lang,
        "request_type": "translate",
        "dictionary_id": dictionary_id,
        "model_id": model_id,
        "response_with_term_mapping": response_with_term_mapping
    }

def create_payload(contents: List[str], src_lang: str, dest_lang: str, dictionary_id: str, model_id: str, response_with_term_mapping: bool=False) -> Dict[str, Any]:
    """
    :return: Dictionary containing the payload
    """
    return {
        "src_contents": contents,
        "src_lang": src_lang,
        "dest_lang": dest_lang,
        "request_type": "translate",
        # "dictionary_id": dictionary_id,
        "model_id": model_id,
        "response_with_term_mapping": response_with_term_mapping
    }

def invoke_lambda_function(client: boto3.client, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke the Lambda function and return the response.
    
    :param client: boto3 Lambda client
    :param function_name: Name of the Lambda function to invoke
    :param payload: Payload to send to the Lambda function
    :return: Dictionary containing the Lambda function response
    """
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    
    return json.loads(response['Payload'].read())

def main():
    # Initialize Lambda client
    lambda_client = create_lambda_client(REGION,AK, SK)
    
    # Content to be translated
    
    contents = ['miHoYo is great!']
    print(f"Original contents: {contents}")
    print("--------------------")   
    
    # Create payload for Lambda function
    payload = create_payload(contents, SOURCE_LANG, TARGET_LANG, DICTIONARY_ID, MODEL_ID, False)
    
    print(f"input: {payload}")
    
    # Invoke Lambda function
    response = invoke_lambda_function(lambda_client, LAMBDA_FUNCTION_NAME, payload)
    print(f"response: {response}")
    
    # Extract results
    for translation in response['translations']:
        if 'term_mapping' in translation:
            term_mapping = translation['term_mapping']
            for mapping in term_mapping:
                print(f"Origin Term: {mapping[0]}, Translated: {mapping[1]}, Entity: {mapping[2]}")

        translated_text = translation['translated_text']
        print(f"Translated Text: {translated_text}")

        model = translation['model']
        print(f"Model: {model}")

        glossary_config = translation['glossary_config']
        print(f"Dict: {glossary_config}")

        print("--------------------")   
    

if __name__ == "__main__":
    main()