import re
import boto3
import json
import time
import datetime
from typing import Dict, List, Tuple, Optional, Any
from botocore.exceptions import ClientError

from app.core.config import settings

class AWSService:
    def __init__(self):
        self.region = settings.AWS_REGION
        self.upload_bucket = settings.UPLOAD_BUCKET
        self.table_prefix = settings.TABLE_PREFIX
        
        # Initialize AWS clients
        self.s3 = boto3.client('s3', region_name=self.region)
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.dynamodb_client = boto3.client('dynamodb', region_name=self.region)
        self.lambda_client = boto3.client('lambda', region_name=self.region)
        self.comprehend = boto3.client('comprehend', region_name=self.region)
        self.glue = boto3.client('glue', region_name=self.region)
        self.ssm = boto3.client('ssm', region_name=self.region)
        self.bedrock = boto3.client('bedrock', region_name=self.region)
    
    # Translation functions
    async def translate_content(
        self, 
        contents: List[str], 
        source_lang: str, 
        target_lang: str, 
        dictionary_id: str, 
        model_id: str,
        lambda_alias: str = "prod"
    ) -> Tuple[str, str]:
        """
        Translate content using AWS Lambda function
        """
        payload = {
            "src_contents": contents,
            "src_lang": source_lang,
            "dest_lang": target_lang,
            "request_type": "translate",
            "dictionary_id": dictionary_id,
            "model_id": model_id,
            "response_with_term_mapping": True,
            "max_content_length": 65535
        }

        translate_response = self.lambda_client.invoke(
            FunctionName='translate_tool',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload),
            Qualifier=lambda_alias
        )
        
        payload_json = json.loads(translate_response.get('Payload').read())
        
        if 'translations' in payload_json:
            result = payload_json['translations'][0]
            term_mapping = result.get('term_mapping')
            term_mapping_list = [
                self._build_mapping(src_term=tup[0], target_term=tup[1], entity_type=tup[2]) 
                for tup in term_mapping
            ]
            return result.get('translated_text'), '\n'.join(term_mapping_list)
        else:
            return payload_json.get("error"), ""
    
    def _build_mapping(self, src_term, target_term, entity_type):
        entity_tag = f"[{entity_type}] " if entity_type else ""
        if src_term and target_term:
            return f"{entity_tag}{src_term}=>{target_term}"
        else:
            return None
    
    # Dictionary functions
    async def list_dictionary_ids(self) -> List[str]:
        """
        Retrieve a list of dictionary IDs from DynamoDB tables.
        """
        translate_mapping_tables = []
        paginator = self.dynamodb_client.get_paginator('list_tables')
        page_iterator = paginator.paginate()

        for page in page_iterator:
            for table_name in page['TableNames']:
                if table_name.startswith(self.table_prefix):
                    translate_mapping_tables.append(table_name.removeprefix(self.table_prefix))

        return translate_mapping_tables
    
    async def get_dict_with_version(self, table_list: List[str]) -> Dict[str, List[str]]:
        """
        Get the dictionary id with version
        """
        dict_with_version = {}
        for table_name in table_list:
            # Split into parts and handle version separately
            if '_v' in table_name:
                # Find the last occurrence of '_v' to separate version
                base_name, version = table_name.rsplit('_v', 1)
                version = 'v' + version
                # Get dict_id by removing translate_mapping_ prefix
                dict_id = base_name
            else:
                dict_id = table_name
                version = None
                
            if dict_id not in dict_with_version:
                dict_with_version[dict_id] = []
            if version:  # Only append version if it exists
                dict_with_version[dict_id].append(version)
        
        # Sort versions numerically by extracting number after 'v'
        for dict_id in dict_with_version:
            versions = [v for v in dict_with_version[dict_id] if v.startswith('v')]
            versions.sort(key=lambda x: int(x.removeprefix('v')))
            dict_with_version[dict_id] = ['default'] + versions
        
        return dict_with_version
    
    async def get_current_version(self, dict_id: str) -> Optional[str]:
        """
        Get the current version of the dictionary
        """
        try:
            translate_meta_table = self.dynamodb.Table('translate_meta')
            response = translate_meta_table.get_item(Key={'dict': dict_id})
            if 'Item' in response:  
                return response['Item']['version']
            else:
                return None
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            # Table doesn't exist
            return None
    
    async def update_current_version(self, dict_id: str, version: str) -> None:
        """
        Update the current version of the dictionary
        """
        translate_meta_table = self.dynamodb.Table('translate_meta')
        translate_meta_table.put_item(Item={'dict': dict_id, 'version': version})
    
    async def query_term(self, table_name: str, term: str) -> Optional[Dict[str, Any]]:
        """
        Query a term from the dictionary
        """
        real_table_name = f"{self.table_prefix}{table_name}"
        ddb_table = self.dynamodb.Table(real_table_name)
        
        try:
            response = ddb_table.get_item(Key={'term': term})
            if "Item" in response:
                return response["Item"]
            return None
        except ClientError:
            return None
    
    async def update_term_mapping(self, table_name: str, term: str, entity: str, mapping_info: Dict[str, List[str]]) -> None:
        """
        Update a term mapping in the dictionary
        """
        real_table_name = f"{self.table_prefix}{table_name}"
        ddb_table = self.dynamodb.Table(real_table_name)

        ddb_item = {
            'term': term,
            'entity': entity,
            'mapping': mapping_info,
        }

        ddb_table.put_item(Item=ddb_item)
    
    # File upload functions
    async def upload_to_s3(self, file_content: bytes, s3_key: str) -> Tuple[bool, str]:
        """
        Upload a file to S3
        """
        try:
            self.s3.put_object(
                Body=file_content,
                Bucket=self.upload_bucket,
                Key=s3_key
            )
            return True, "Finish Uploading to S3"
        except Exception as e:
            return False, str(e)
    
    # Glue job functions
    async def start_glue_job(self, key_path: str, dictionary_name: str, job_name: str = 'ingest_knowledge2ddb') -> str:
        """
        Start a Glue job
        """
        publish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = self.glue.start_job_run(
            JobName=job_name,
            Arguments={
                '--additional-python-modules': 'boto3>=1.28.52,botocore>=1.31.52',
                '--dictionary_name': dictionary_name,
                '--object_key': key_path,
                '--bucket': self.upload_bucket,
            })
        return response['JobRunId']
    
    async def get_glue_job_run_status(self, run_id: str, job_name: str = 'ingest_knowledge2ddb') -> Optional[str]:
        """
        Get the status of a Glue job run
        """
        try:
            response = self.glue.get_job_run(
                JobName=job_name,
                RunId=run_id
            )
            return response['JobRun']['JobRunState']
        except Exception:
            return None
    
    # Parameter Store functions
    async def get_parameters_by_path(self, path: str) -> List[Dict[str, Any]]:
        """
        Get parameters from Parameter Store by path
        """
        try:
            response = self.ssm.get_parameters_by_path(
                Path=path,
                Recursive=True,
                WithDecryption=True
            )
            return response['Parameters']
        except Exception:
            return []
    
    async def update_parameter(self, name: str, value: str) -> bool:
        """
        Update a parameter in Parameter Store
        """
        try:
            self.ssm.put_parameter(
                Name=name,
                Value=value,
                Type='String',
                Overwrite=True
            )
            return True
        except Exception:
            return False
    
    # Bedrock functions
    async def list_foundation_models(self) -> List[str]:
        """
        List available foundation models from Amazon Bedrock
        """
        def remove_context_window_suffix(model_ids):
            """
            使用正则表达式移除模型ID中的context window后缀
            """

            cleaned_ids = []
            for model_id in model_ids:
                print(model_id)
                if model_id.endswith('k'):
                    parts = model_id.split(':')
                    model_id_no_suffix = ':'.join(parts[:-1])
                    cleaned_ids.append(model_id_no_suffix)
                else:
                    cleaned_ids.append(model_id)
            
            return list(set(cleaned_ids))

        try:
            response = self.bedrock.list_foundation_models()

            cris_prefix = ''
            if self.region.startswith('us'):
                cris_prefix = 'us.'
            elif self.region.startswith('eu'):
                cris_prefix = 'eu.'
            elif self.region.startswith('ap'):
                cris_prefix = 'apac.'

            # Filter for only Anthropic Claude models as they're used for translation
            models = []
            for model in response.get('modelSummaries', []):
                providerName = model.get('providerName')
                inputModalities = model.get('inputModalities')
                model_id = model.get('modelId')
                status = model.get('modelLifecycle').get('status')
                # Only include Anthropic Claude models
                if providerName in ['Anthropic', 'Amazon'] and 'TEXT' in inputModalities and status != 'LEGACY':
                    # Add model ID with version
                    models.append(f"{cris_prefix}{model_id}")
            return remove_context_window_suffix(models)
        except Exception as e:
            print(f"Error listing Bedrock foundation models: {str(e)}")
            # Fall back to config if there's an error
            return settings.SUPPORTED_MODELS
    
    # Language detection
    async def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of a text
        """
        try:
            response = self.comprehend.detect_dominant_language(Text=text)
            language_code = response['Languages'][0]['LanguageCode']
            
            lang_dict = {
                'zh': 'zh-cn',
                'zh-TW': 'zh-tw',
                'de': 'de-de',
                'en': 'en-us',
                'es': 'es-es',
                'fr': 'fr-fr',
                'id': 'id-id',
                'it': 'it-it',
                'ja': 'ja-jp',
                'ko': 'ko-kr',
                'pt': 'pt-pt',
                'ru': 'ru-ru',
                'th': 'th-th',
                'tr': 'tr-tr',
                'vi': 'vi-vn'
            }
            
            return lang_dict.get(language_code)
        except Exception:
            return None

# Create a singleton instance
aws_service = AWSService()
