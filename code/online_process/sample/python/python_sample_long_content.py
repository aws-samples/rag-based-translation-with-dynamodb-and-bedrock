import boto3
import json
from typing import Dict, Any, List

# AWS and model configuration
REGION = 'ap-southeast-1'
MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'
DICTIONARY_ID = 'dict_1'
SOURCE_LANG = 'en-us'
TARGET_LANG = 'zh-cn'
LAMBDA_FUNCTION_NAME = 'translate_tool'

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
        "response_with_term_mapping": response_with_term_mapping,
        "max_content_length": 65535
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
    s="""Star Crusher Swarm King: Skaracabaz (Synthetic)" encounter is not particularly difficult and it reminds of the Swarm encounter in the simulated universe.

Phase 1:

- Entanglement I: E Radiating Venom - The boss will apply Entanglement to a randomly chosen teammate, stunning them and leaving them unable to act while taking additional damage per action of Skaracabaz. This can easily be countered by cleansing the affected teammate and continuing the fight.

- The carapace of Begotton Spawn - "Multiply" - When Skaracabaz is attacked, he summons a Gnaw sting. If the weakness is broken during this period, deal toughness damage to all enemies. There are a few ways to get past this, either through brute forcing the toughness down with break effect units, tanking all of the mobs with a big defensive unit such as Gepard or Fu Xuan, or simply eliminating Skarazbaz outright. Another method is eliminating the summons that spawn, causing them to explode and splash defence down on all targets, causing Skaracbaz to be vulnerable to heavy damage.

Phase 2:

- Skaracabaz will summon lesser stings during this phase, and after a short time, they will explode on the party, inflicting heavy damage and debilitating status ailments.

- Ovum of Collapsed Star - This deals incredibly heavy AOE damage, which must either be mitigated by a preservation shielder such as Gepard, Main Character Fire Preservation Shields, or redirected by Fu-Xuan to keep other party members alive.

Overall, this encounter is not incredibly challenging and is not too different from the Swarm encounter."""
    contents = [s]
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