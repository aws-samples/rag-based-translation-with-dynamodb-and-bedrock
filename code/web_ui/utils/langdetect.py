import yaml
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

yaml_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(yaml_path, 'r') as f:
    lang_data = yaml.safe_load(f)
    
deploy_region = lang_data['deploy_region'][0]

comprehend = boto3.client('comprehend',region_name=deploy_region)
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

def detect_language_of(text):
    """
    Detect the dominant language of the input text.
    Args:
    text (str): The text to detect the language for.
    Returns:
    str: The detected dominant language code, or None if an error occurred.
    """
    # Detect the dominant language using AWS Comprehend
    detect_language_code = _detect_language_by_aws_comprehend(text)
    lang_dict = {
        'zh' : 'zh-cn',
        'zh-TW' : 'zh-tw',
        'de': 'de-de',
        'en': 'en-us',
        'es': 'es-es',
        'fr': 'fr-fr',
        'id': 'id-id',
        'it': 'it-it',
        'ja': 'ja-jp',
        'ko' : 'ko-kr',
        'pt' : 'pt-pt',
        'ru' : 'ru-ru',
        'th' : 'th-th',
        'tr' : 'tr-tr',
        'vi' : 'vi-vn'
    }

    if detect_language_code:
        # Get the standard language code
        standard_lang_code = lang_dict.get(detect_language_code)
        return standard_lang_code
    else:
        return None

if __name__ == "__main__":
    new_mapping_info = {
        "zh-cn" : "奇怪的渔人吐司",
        "zh-tw" : "奇怪的漁人吐司",
        "de-de" : "Misslungene Fischerschnitte",
        "en-us" : "Suspicious Fisherman’s Toast",
        "es-es" : "Tostada del pescador extraña",
        "fr-fr" : "Toast du pêcheur (suspect)",
        "id-id" : "Suspicious Fisherman’s Toast",
        "it-it" : "Toast del pescatore sospetto",
        "ja-jp" : "微妙な漁師トースト",
        "ko-kr" : "이상한 어부 토스트",
        "pt-pt" : "Torrada do Pescador Estranha",
        "ru-ru" : "Странный рыбацкий бутерброд",
        "th-th" : "Fisherman’s Toast รสประหลาด",
        "tr-tr" : "Balıkçı Tostu (Tuhaf)",
        "vi-vn" : "Bánh Người Cá Kỳ Lạ"
    }

    for key, value in new_mapping_info.items():
        print(f"""{value} --> {detect_language_of(value)}""")