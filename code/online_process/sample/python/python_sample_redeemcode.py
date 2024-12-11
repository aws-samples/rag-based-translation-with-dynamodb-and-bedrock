import boto3
import json
from typing import Dict, Any, List

# AWS and model configuration
REGION = 'ap-southeast-1'
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
DICTIONARY_ID = 'dict_test'
SOURCE_LANG = 'en-us'
TARGET_LANG = 'zh-cn'
LAMBDA_FUNCTION_NAME = 'translate_tool'
LAMBDA_ALIAS = 'staging'

def create_lambda_client(region: str) -> boto3.client:
    """
    Create and return a boto3 Lambda client.
    
    :param region: AWS region name
    :return: boto3 Lambda client
    """
    return boto3.client('lambda', region_name=region)

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
        "dictionary_id": dictionary_id,
        "model_id": model_id,
        "response_with_term_mapping": response_with_term_mapping
    }

def invoke_lambda_function(client: boto3.client, function_name: str, alias_name:str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke the Lambda function and return the response.
    
    :param client: boto3 Lambda client
    :param function_name: Name of the Lambda function to invoke
    :param payload: Payload to send to the Lambda function
    :return: Dictionary containing the Lambda function response
    """
    response = client.invoke(
        FunctionName=function_name,
        Qualifier=alias_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    
    return json.loads(response['Payload'].read())

def main():
    # Initialize Lambda client
    lambda_client = create_lambda_client(REGION)
    
    # Content to be translated
    sample_content = """
    GUYS IF U FACED ANY ISSUE THEN PLEASE LET ME IN COMMENT BOX AND ALSO REEDEM ALL CODES MANUALLY 

    ( CODE 1 ) - LA5E77CLZX5V

    ( CODE 2 ) - MTLF6DKA7PQZ

    ( CODE 3 ) - HVQAUTYBANKE

    ( CODE 4 ) - AEXK6S4U93CF

    ( CODE 5 ) - EMVD38DBGX12

    ( CODE 6 ) - GENSHINGIFT
    """
    

    for i in range(1, 500):
        contents = [ sample_content ]
        # Create payload for Lambda function
        payload = create_payload(contents, SOURCE_LANG, TARGET_LANG, DICTIONARY_ID, MODEL_ID, False)
            
        # Invoke Lambda function
        response = invoke_lambda_function(lambda_client, LAMBDA_FUNCTION_NAME, LAMBDA_ALIAS, payload)
        
        # Extract results
        if 'translations' in response:
            for translation in response['translations']:
                if 'term_mapping' in translation:
                    term_mapping = translation['term_mapping']
                    for mapping in term_mapping:
                        print(f"Origin Term: {mapping[0]}, Translated: {mapping[1]}, Entity: {mapping[2]}")

                translated_text = translation['translated_text']
                print(f"{translated_text}")

if __name__ == "__main__":
    main()