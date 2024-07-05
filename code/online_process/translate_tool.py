import jieba
import jieba.posseg as pseg
import boto3
import os
import logging
import json
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dictionary_info_dict = {}
bedrock = boto3.client(service_name='bedrock-runtime')


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

def retrieve_term_mapping(term_list, src_lang, dest_lang):
    mapping_list = []
    ddb_table = None
    global ddb_en_table, ddb_chs_table
    if src_lang == 'EN':
        ddb_table = ddb_en_table
    elif src_lang == 'CHS':
        ddb_table = ddb_chs_table
    else:
        raise RuntimeError(f"unsupported {src_lang}")

    for term in term_list:
        print(f"find mapping of {term}")
        response = ddb_table.get_item(Key={'term': term})
        print(response)
        if "Item" in response.keys():
            item = response["Item"]
            mapping_info = item['mapping']
            entity = item['entity']
            mapping_list.append([term, mapping_info[dest_lang], entity])

    return mapping_list

def construct_translate_prompt(src_content, src_lang, dest_lang, multilingual_term_mapping):
    pe_template = """You are the world's most professional translation tool, proficient in professional translation from {src_lang} to {dest_lang}.
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

Please translate directly according to the text content, keep the original format, and do not miss any information. Put the result in <translation>"""

    crosslingual_terms = []

    crosslingual_terms = [ (item[0], item[2]) for item in multilingual_term_mapping if item[0] == item[1] ]

    # [('Yelan', '夜兰', 'TCG Opponent'), ('Xingqiu', '行秋', 'TCG Opponent'), ('Keqing', '刻晴', 'TCG Opponent'), ('Beidou', '北斗', 'TCG Opponent')]

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

    prompt = pe_template.format(src_lang=src_lang, dest_lang=dest_lang, vocabulary=vocabulary_prompt, mappings=term_mapping_prompt, content=src_content)
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
            return rep_obj['content'][0]['text']
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
        prev_last_modified = dictionary_info_dict['dictionary_id'].get('last_modified', '1970-00-00 00:00:00+00:00')
        if last_modified == prev_last_modified:
            return False, last_modified

    return True, last_modified

def refresh_dictionary(bucket, s3_prefix, dictionary_id) -> bool:
    global dictionary_info_dict

    try:
        assert dictionary_id is not None

        is_updated, last_modified = get_dictionary_status(bucket, s3_prefix, dictionary_id)

        if is_updated:
            s3 = boto3.client('s3')
            dict_file_path = f"{s3_prefix}/{dictionary_id}/user_dict.txt"
            local_file = f'/tmp/{dictionary_id}/user_dict.txt' # /tmp 只有这个路径是可以写的

            # 下载文件
            try:
                s3.download_file(bucket, dict_file_path, local_file)
                with open(local_file, 'r') as file:
                    lines = file.readlines()
                    dictionary_info_dict[dictionary_id] = {"last_modified" : last_modified, "terms" : [ item.strip() for item in lines ]}

                print(f'File downloaded successfully: {local_file}')
            except Exception as e:
                print(f'Error downloading file: {e}')

        if dictionary_id not in dictionary_info_dict:
            raise RuntimeError(f"There is no data for {dictionary_id}")

        return True

    except Exception as e:
        return False


# 对文本进行分词
@handle_error
def lambda_handler(event, context):
    src_content = event.get('src_content')
    src_lang = event.get('src_lang')
    dest_lang = event.get('dest_lang')
    dictionary_id = event.get('dictionary_id') # dictionary_id is table 
    request_type = event.get('request_type')
    model_id = event.get('model_id')

    if not src_content:
        return {'error': 'src_content is required'}
    if not src_lang:
        return {'error': 'src_lang is required'}
    if not dest_lang:
        return {'error': 'dest_lang is required'}
    if request_type not in ['segment_only', 'term_mapping', 'translate']:
        return {"error": "request_type should be ['segment_only', '，term_mapping', 'translate']"}
    
    bucket = os.environ.get('user_dict_bucket')
    s3_prefix = os.environ.get('user_dict_prefix')

    succeded = refresh_dictionary(bucket, s3_prefix, dictionary_id)

    if not succeded:
        return { "error" : f"There is no user_dict for {dictionary_id} on S3 " }

    global dictionary_info_dict

    words = mfm_segment(src_content, dictionary_info_dict.get(dictionary_id))
    if request_type == 'segment_only':
        return {'words': words}

    json_obj = {}

    multilingual_term_mapping = retrieve_term_mapping(words, src_lang, dest_lang)
    json_obj["term_mapping"] = multilingual_term_mapping
    if request_type == 'term_mapping':
        return json_obj

    prompt = construct_translate_prompt(src_content, src_lang, dest_lang, multilingual_term_mapping)
    print("prompt:")
    print(prompt)

    result = invoke_bedrock(model_id, prompt)
    json_obj["result"] = result
    
    return json_obj
    

