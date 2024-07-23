import boto3
import json
from typing import Dict, Any

# AWS and model configuration
REGION = 'us-west-2'
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
DICTIONARY_ID = 'test_dict1'
SOURCE_LANG = 'CHS'
TARGET_LANG = 'EN'
LAMBDA_FUNCTION_NAME = 'translate_tool'

def create_lambda_client(region: str) -> boto3.client:
    """
    Create and return a boto3 Lambda client.
    
    :param region: AWS region name
    :return: boto3 Lambda client
    """
    return boto3.client('lambda', region_name=region)

def create_payload(content: str, src_lang: str, dest_lang: str, dictionary_id: str, model_id: str) -> Dict[str, Any]:
    """
    Create the payload for the Lambda function.
    
    :param content: Content to be translated
    :param src_lang: Source language code
    :param dest_lang: Target language code
    :param dictionary_id: Dictionary ID for translation
    :param model_id: Model ID for translation
    :return: Dictionary containing the payload
    """
    return {
        "src_content": content,
        "src_lang": src_lang,
        "dest_lang": dest_lang,
        "request_type": "translate",
        "dictionary_id": dictionary_id,
        "model_id": model_id
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
    lambda_client = create_lambda_client(REGION)
    
    # Content to be translated
    content = '蚕食者之影在哪里能找到？'
    print(f"Original content: {content}")
    
    # Create payload for Lambda function
    payload = create_payload(content, SOURCE_LANG, TARGET_LANG, DICTIONARY_ID, MODEL_ID)
    
    # Invoke Lambda function
    response = invoke_lambda_function(lambda_client, LAMBDA_FUNCTION_NAME, payload)
    
    # Extract results
    translation_result = response.get('result')
    term_mapping = response.get('term_mapping')
    
    # Print results
    print(f"Translated result: {translation_result}")
    print(f"Term mapping: {term_mapping}")

if __name__ == "__main__":
    main()