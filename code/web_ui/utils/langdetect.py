import yaml
import boto3
import os

comprehend = boto3.client('comprehend')

yaml_path = os.path.join(os.path.dirname(__file__), 'lang.yaml')
with open(yaml_path, 'r') as f:
    lang_data = yaml.safe_load(f)

def _detect_language_by_aws_comprehend(text):
    """
    Detect the dominant language of the input text using AWS Comprehend.
    Args:
    text (str): The text to detect the language for.
    Returns:
    str: The detected dominant language code, or None if an error occurred.
    """
    try:
        # Call the detect_dominant_language API
        response = comprehend.detect_dominant_language(Text=text)
        
        # Get the detected dominant language code
        language_code = response['Languages'][0]['LanguageCode']
        return language_code
    except Exception as e:
        print(f"Error occurred while calling Comprehend: {e}")
        return None
    
def _get_customized_language_code(language_code):
    """
    Get the customized language code defined by customer
    Args:
    language_code (str): The aws comprehend language code
    Returns:
    str: The customized language code, or None if the language code is not supported.
    """
    # Check if the language code is supported
    if language_code in lang_data['supportedlang']:
        return lang_data['supportedlang'][language_code]
    else:
        return None

def detect_language_of(text):
    """
    Detect the dominant language of the input text.
    Args:
    text (str): The text to detect the language for.
    Returns:
    str: The detected dominant language code, or None if an error occurred.
    """
    # Detect the dominant language using AWS Comprehend
    language_code = _detect_language_by_aws_comprehend(text)

    if language_code:
        # Get the customized language code
        customized_language_code = _get_customized_language_code(language_code)
        return customized_language_code
    else:
        return None
    

if __name__ == "__main__":
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

    for key, value in new_mapping_info.items():
        print(f"""{value} --> {detect_language_of(value)}""")