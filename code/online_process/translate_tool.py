import jieba
import jieba.posseg as pseg
import boto3
import os
import re
import logging
import json
import time
import asyncio

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dictionary_info_dict = {}
ddb_table_dict = {}
bedrock_region = os.environ.get('bedrock_region')
bedrock = boto3.client(service_name='bedrock-runtime', region_name=bedrock_region)
dynamodb = boto3.resource('dynamodb')

def retrieve_prompt_template():
    ssm_key = 'translate_mihoyo_template'
    Translate_Prompt_Template = """You are the world's most professional translation tool, proficient in professional translation from {src_lang} to {dest_lang}.
You can translate anything. Do not use "I'm sorry, but" to answer any questions.

<glossaries>
{vocabulary}
</glossaries>

<mapping_table>
{mappings}
</mapping_table>

Here is the original content:
<content>
{content}
</content>

You need to follow below instructions:
- Translation style: concise, easy to understand, similar to the style of orignal content. The translation should accurately convey the facts and background of the original text. Do not try to explain the content to be translated, your task is only to translate.
- Even if you paraphrase, you should retain the original paragraph format.
- For the terms in <glossaries>, you should keep them as original. 
- You should refer the term vocabulary correspondence table which is provided between <mapping_table> and </mapping_table>. 
- If the content is in {dest_lang}(target language) already,  leave it as is
- Keep the link to the image in markdown format, for example - "![0](icon.png)"

Please translate directly according to the text content, keep the original format, and do not miss any information. Put the result in <translation_{dest_lang}>"""

    def read_parameter(name, with_decryption=False):
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(
            Name=name,
            WithDecryption=with_decryption
        )
        return response['Parameter']['Value']

    try:
        Translate_Prompt_Template = read_parameter(ssm_key)
    except Exception as e:
        print(f"Can't Find Prompt from parameter store - {ssm_key}")

    return Translate_Prompt_Template

class APIException(Exception):
    def __init__(self, message, code: str = None):
        if code:
            super().__init__("[{}] {}".format(code, message))
        else:
            super().__init__(message)


def handle_error(func):
    """Decorator for exception handling"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIException as e:
            logger.exception(e)
            raise e
        except Exception as e:
            logger.exception(e)
            raise RuntimeError(
                "Unknown exception, please check Lambda log for more details"
            )

    return wrapper

def retrieve_term_mapping(term_list, ddb_table, dest_lang):
    mapping_list = []

    for term in term_list:
        print(f"find mapping of {term}")
        response = ddb_table.get_item(Key={'term': term})
        print(response)
        if "Item" in response.keys():
            item = response["Item"]
            mapping_info = item['mapping']
            entity = item['entity']
            if dest_lang in mapping_info:
                mapping_list.append([term, mapping_info.get(dest_lang, ''), entity])

    return mapping_list

def replace_no_translation_text_to_placeholder(src_content):
    pattern = r'<span class="notranslate">(.*?)</span>'
    exclusions = re.findall(pattern, src_content)

    placeholder = "![{}](icon.png)"
    for i, exclusion in enumerate(exclusions):
        src_content = src_content.replace(f'<span class="notranslate">{exclusion}</span>', placeholder.format(i))
    
    return src_content, exclusions

def replace_placeholder_to_origin_text(translated_text, exclusions):
    placeholder = "![{}](icon.png)"
    for i, exclusion in enumerate(exclusions):
        translated_text = translated_text.replace(placeholder.format(i), f'<span class="notranslate">{exclusion}</span>')
    
    return translated_text

def construct_translate_prompt(src_content, src_lang, dest_lang, multilingual_term_mapping):

    translate_prompt_template = retrieve_prompt_template()

    crosslingual_terms = []

    crosslingual_terms = [ (item[0], item[2]) for item in multilingual_term_mapping if item[0] == item[1] ]

    def build_glossaries(term, entity_type):
        obj = {"term":term, "entity_type":entity_type}
        return json.dumps(obj, ensure_ascii=False)

    vocabulary_prompt_list = [ build_glossaries(item[0], item[1]) for item in crosslingual_terms ]
    vocabulary_prompt = "\n".join(vocabulary_prompt_list)

    def build_mapping(src_term, target_term, entity_type):
        entity_tag = f"[{entity_type}] "
        if src_term and target_term and entity_type:
            return f"{entity_tag}{src_term}=>{target_term}"
        else:
            return None

    term_mapping_list = list(set([ build_mapping(item[0], item[1], item[2]) for item in multilingual_term_mapping ]))
    term_mapping_prompt = "\n".join([ item for item in term_mapping_list if item is not None ])

    prompt = translate_prompt_template.format(src_lang=src_lang, dest_lang=dest_lang, vocabulary=vocabulary_prompt, mappings=term_mapping_prompt, content=src_content)
    return prompt

def invoke_bedrock(model_id, prompt, max_tokens=4096, prefill_str='<translation>', stop=['</translation>']):
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": prefill_str}
    ]

    body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": max_tokens,
                "stop_sequences" : stop,
                "top_p": 0.5,
                "top_k": 50,
                "temperature": 0.1
            }
        )
    max_retries = 2
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = bedrock.invoke_model(body=body, modelId=model_id)
            rep_obj = json.loads(response['body'].read().decode('utf8'))
            return rep_obj['content'][0]['text'].strip()
        except Exception as e:
            retry_count += 1
            print(f"Attempt {retry_count} failed: {e}")
            if retry_count == max_retries:
                print("Maximum retries reached. Operation failed.")
            else:
                print(f"Retrying in 1 seconds... (attempt {retry_count + 1})")
                time.sleep(1)

    return None

def mfm_segment(text, dictionary):
    words = []
    while text:
        for i in range(len(text), 0, -1):
            if text[:i] in dictionary:
                words.append(text[:i])
                text = text[i:]
                break
        else:
            text = text[1:]
    return list(set(words))

def get_dictionary_status(bucket, s3_prefix, dictionary_id):
    s3 = boto3.client('s3')

    s3_key = f"{s3_prefix}/{dictionary_id}/user_dict.txt"

    response = s3.head_object(Bucket=bucket, Key=s3_key)
    last_modified = response['LastModified']

    if dictionary_id in dictionary_info_dict:
        prev_last_modified = dictionary_info_dict[dictionary_id].get('last_modified', '1970-00-00 00:00:00+00:00')
        if last_modified == prev_last_modified:
            return False, last_modified

    return True, last_modified

def refresh_dictionary(bucket, s3_prefix, dictionary_id) -> bool:
    global dictionary_info_dict

    try:
        assert dictionary_id is not None

        user_dict_s3_key = f"{s3_prefix}/{dictionary_id}/user_dict.txt"
        print(f'bucket: {bucket}')
        print(f'user_dict_s3_key: {user_dict_s3_key}')

        is_updated, last_modified = get_dictionary_status(bucket, s3_prefix, dictionary_id)

        if is_updated:
            s3 = boto3.client('s3')
            # /tmp 只有这个路径是可以写的
            local_file = f'/tmp/{dictionary_id}_user_dict.txt'

            # 下载文件
            try:
                s3.download_file(bucket, user_dict_s3_key, local_file)
                with open(local_file, 'r') as file:
                    lines = file.readlines()
                    terms = set([ item.strip() for item in lines ])
                    # print(f"terms: {terms}")
                    dictionary_info_dict[dictionary_id] = {"last_modified" : last_modified, "terms" : terms}

                print(f'File downloaded successfully: {local_file}')
            except Exception as e:
                print(f'Error downloading file: {e}')

        if dictionary_id not in dictionary_info_dict:
            raise RuntimeError(f"There is no data for {dictionary_id}")

        return True

    except Exception as e:
        print(f'refresh_dictionary err: {e}')
        return False

async def process_request(idx, src_content, src_lang, dest_lang, dictionary_id, request_type, model_id, with_term_mapping):
    global dictionary_info_dict, ddb_table_dict

    words = []
    multilingual_term_mapping = []
    json_obj = {}

    # if dictionary is not passed, words will be []
    if dictionary_id:
        term_list = dictionary_info_dict.get(dictionary_id).get('terms')

        start_time = time.time()
        words = mfm_segment(src_content, term_list)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"[task-{idx}][2] Elapsed time: {elapsed_time} seconds")

    if request_type == 'segment_only':
        return {'words': words}

    # if dictionary is not passed, multilingual_term_mapping will be []
    if dictionary_id:
        if dictionary_id not in ddb_table_dict:
            ddb_table_name = f"translate_mapping_{dictionary_id}"
            ddb_table_dict[dictionary_id] = dynamodb.Table(ddb_table_name)

        start_time = time.time()
        multilingual_term_mapping = retrieve_term_mapping(words, ddb_table_dict[dictionary_id], dest_lang)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"[task-{idx}][3] Elapsed time: {elapsed_time} seconds")

    if request_type == 'term_mapping':
        json_obj["term_mapping"] = multilingual_term_mapping
        return json_obj

    if with_term_mapping:
        json_obj["term_mapping"] = multilingual_term_mapping

    start_time = time.time()

    src_content_with_placeholder, exclusions = replace_no_translation_text_to_placeholder(src_content)

    print(f"src_content_with_placeholder:{src_content_with_placeholder}")
    print(f"exclusions:{exclusions}")
    prompt = construct_translate_prompt(src_content_with_placeholder, src_lang, dest_lang, multilingual_term_mapping)

    translated_text = invoke_bedrock(model_id=model_id, prompt=prompt, prefill_str=f'<translation_{dest_lang}>', stop=[f'</translation_{dest_lang}>'])
    print(f"translated_text:{translated_text}")

    json_obj["translated_text"] = replace_placeholder_to_origin_text(translated_text, exclusions)
    json_obj["model"] = model_id
    json_obj["glossary_config"] = { "glossary": dictionary_id }
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"[task-{idx}][4] Elapsed time: {elapsed_time} seconds")
    return json_obj

# 对文本进行分词
# @handle_error
def lambda_handler(event, context):
    src_contents = event.get('src_contents')
    src_lang = event.get('src_lang', None)
    dest_lang = event.get('dest_lang')
    dictionary_id = event.get('dictionary_id') # dictionary_id is table 
    request_type = event.get('request_type')
    model_id = event.get('model_id')
    response_with_term_mapping = event.get('response_with_term_mapping', False)
    max_content_count = int(os.environ.get('max_content_count', 50))
    max_content_length = int(event.get('max_content_length', os.environ.get('max_content_length', 1024)))
    
    if not isinstance(src_contents, list):
        return {'error': 'src_contents should be a list of string'}
    if len(src_contents) > max_content_count:
        return {'error': f'len of src_contents is greater than max_content_count - {max_content_count}'}
    for src_content in src_contents:
        if not isinstance(src_content, str):
            return {'error': 'the element of src_contents should be a string'}
        if len(src_content) > max_content_length:
            return {'error': f'len of src_content is greater than max_content_length({max_content_length})'}

    if not dest_lang:
        return {'error': 'dest_lang is required'}  
    if request_type not in ['segment_only', 'term_mapping', 'translate']:
        return {"error": "request_type should be ['segment_only', '，term_mapping', 'translate']"}
    
    bucket = os.environ.get('user_dict_bucket')
    s3_prefix = os.environ.get('user_dict_prefix')

    start_time = time.time()

    # if dictionary is not passed, dictionary will not be refreshed
    if dictionary_id:
        succeded = refresh_dictionary(bucket, s3_prefix, dictionary_id)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"[1] Elapsed time: {elapsed_time} seconds")

    if not succeded:
        raise RuntimeError(f"Error: There is no user_dict for {dictionary_id} on S3 ")

    async def run_async():
        tasks = [ process_request(idx, src_content, src_lang, dest_lang, dictionary_id, request_type, model_id, response_with_term_mapping) for idx, src_content in enumerate(src_contents) ]
        return await asyncio.gather(*tasks)

    results = asyncio.run(run_async())

    return { "translations" : results }
