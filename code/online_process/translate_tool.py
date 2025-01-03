import marisa_trie
import boto3
import os
import re
import logging
import json
import time
import asyncio
import string

from enum import Enum
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dictionary_info_dict = {}
ddb_table_dict = {}
bedrock_region = os.environ.get('bedrock_region')
bedrock = boto3.client(service_name='bedrock-runtime', region_name=bedrock_region)
dynamodb = boto3.resource('dynamodb')

Translate_Meta_Table_Name = 'translate_meta'

class LangCode(Enum):
    DeDe = "de-de"
    EnUs = "en-us"
    EsEs = "es-es"
    FrFr = "fr-fr"
    IdId = "id-id"
    ItIt = "it-it"
    JaJp = "ja-jp"
    KoKr = "ko-kr"
    PtPt = "pt-pt"
    RuRu = "ru-ru"
    ThTh = "th-th"
    TrTr = "tr-tr"
    ViVn = "vi-vn"
    ZhCn = "zh-cn"
    ZhTw = "zh-tw"

def build_trie(terms):
    return marisa_trie.Trie(terms)

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
- You must format your output to strictly follow the format of the original content. You are prohibited from adding, removing, or merging line breaks.
- For the terms in <glossaries>, you should keep them as original. 
- You should refer the term vocabulary correspondence table which is provided between <mapping_table> and </mapping_table>. 
- If the content is in {dest_lang}(target language) already,  leave it as is
- Keep the link to the image in markdown format, for example - "![0](icon.png)"

Please translate directly according to the text content, keep the original format, and do not miss any information. 

Notice that your target language is {dest_lang}, Don't output any characters in other languages. Put the result in <translation_{dest_lang}>"""

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
        logger.warn(f"Can't Find Prompt from parameter store - {ssm_key}, use default prompt instead")

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
        
        logger.info(f"find mapping of {term}")
        response = ddb_table.get_item(Key={'term': term})
        logger.info(f"ddb response: {response}")
        if "Item" in response.keys():
            item = response["Item"]
            mapping_info = item['mapping']
            entity = item['entity']
            if dest_lang in mapping_info:
                mapping_term = mapping_info.get(dest_lang)
                if mapping_term and isinstance(mapping_term, list):
                    mapping_list.append((term, mapping_term[0], entity))

    unique_mapping_set = set(mapping_list)
    unique_mapping_list = [list(item) for item in unique_mapping_set]
    return unique_mapping_list

def replace_no_translation_text_to_placeholder(src_content):

    # Extract prefix content (placeholders at the beginning of src_content)
    prefix_content = ''
    prefix_match = re.match(r'^[\s\t\r\n]*', src_content)
    if prefix_match:
        prefix_content = prefix_match.group(0)
        src_content = src_content[len(prefix_content):]
    # Extract suffix content (placeholders at the end of src_content)
    suffix_content = ''
    suffix_match = re.search(r'[\s\t\r\n]*$', src_content)
    if suffix_match:
        suffix_content = suffix_match.group(0)
        src_content = src_content[:len(src_content) - len(suffix_content)]

    affix = {
        'prefix': prefix_content,
        'suffix': suffix_content
    }


    pattern = r'<span class="notranslate">(.*?)</span>'
    exclusions = re.findall(pattern, src_content)

    placeholder = "![{}](icon.png)"
    for i, exclusion in enumerate(exclusions):
        src_content = src_content.replace(f'<span class="notranslate">{exclusion}</span>', placeholder.format(i))
    
    return src_content, exclusions, affix

def replace_placeholder_to_origin_text(translated_text, exclusions, affix):
    placeholder = "![{}](icon.png)"
    for i, exclusion in enumerate(exclusions):
        translated_text = translated_text.replace(placeholder.format(i), f'<span class="notranslate">{exclusion}</span>')
    
    translated_text = translated_text.strip()
    translated_text = affix['prefix'] + translated_text + affix['suffix']

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
        entity_tag = f"[{entity_type}] " if entity_type else ""
        if src_term and target_term:
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

    logger.info("messages:")
    logger.info(messages)

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
            logger.error(f"Attempt {retry_count} failed: {e}")
            if retry_count == max_retries:
                logger.error("Maximum retries reached. Operation failed.")
            else:
                logger.error(f"Retrying in 1 seconds... (attempt {retry_count + 1})")
                time.sleep(1)

    return None

def mfm_segment_trie(text, trie):
    words = []
    i = 0
    n = len(text)
    while i < n:
        # 使用 trie.prefixes 方法找到所有可能的前缀
        prefixes = trie.prefixes(text[i:])
        if prefixes:
            # 如果找到前缀，选择最长的一个
            longest_prefix = max(prefixes, key=len)
            if len(longest_prefix) == 0:
                i+= 1
                continue
            else:
                words.append(longest_prefix)
                i += len(longest_prefix)
        else:
            # 如果没有找到前缀，跳过当前字符
            i += 1
    return words

def mfm_segment_trie_en(text, trie):
    segment_chars = string.punctuation + string.whitespace

    words = []
    i = 0
    n = len(text)
    while i < n:
        # 使用 trie.prefixes 方法找到所有可能的前缀
        prefixes = trie.prefixes(text[i:])
        if prefixes:
            # 如果找到前缀，选择最长的一个
            longest_prefix = max(prefixes, key=len)
            if len(longest_prefix) == 0:
                i+= 1
                continue
            else:
                # 检查这个最大匹配的前后字符是否为分隔符，比如空格或者标点符号
                left_idx = i - 1
                right_idx = i + len(longest_prefix)
                if (left_idx < 0 or text[left_idx] in segment_chars) and (right_idx >= n or text[right_idx] in segment_chars):
                    words.append(longest_prefix)
                    i += len(longest_prefix)
                else:
                    i += 1
                    continue
        else:
            # 如果没有找到前缀，跳过当前字符
            i += 1
    return words

def list_language_paths(bucket_name, prefix_path):
    logger.info(f"[list_language_paths]: bucket_name: {bucket_name}, prefix_path: {prefix_path}")
    s3 = boto3.client('s3')

    paginator = s3.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket_name, Prefix=prefix_path, Delimiter='/')

    for page in result:
        if "CommonPrefixes" in page:
            for obj in page["CommonPrefixes"]:
                yield obj["Prefix"], obj["Prefix"].rstrip('/').split('/')[-1]

def get_dictionary_status(bucket, s3_prefix, dictionary_id):
    s3 = boto3.client('s3')

    s3_key = f"{s3_prefix}/{dictionary_id}/.update_flag"

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
        is_updated, last_modified = get_dictionary_status(bucket, s3_prefix, dictionary_id)
        logger.info(f"is_updated:{is_updated}, last_modified:{last_modified}")

        if is_updated:
            s3 = boto3.client('s3')
            try:
                dictionary_info_dict[dictionary_id] = { "last_modified" : last_modified, "trie" : {} }
                en_terms = None
                for lang_user_dict_path, lang_code in list_language_paths(bucket_name=bucket, prefix_path=f"{s3_prefix}/{dictionary_id}/"):
                    if lang_code == LangCode.EnUs.value:
                        logger.info(f'lang_user_dict_path: {lang_user_dict_path}, lang_code:{lang_code}')
                        local_file = f'/tmp/{dictionary_id}_{lang_code}_user_dict.txt'
                        user_dict_s3_key = f"{lang_user_dict_path}user_dict.txt"
                        s3.download_file(bucket, user_dict_s3_key, local_file)
                        with open(local_file, 'r') as file:
                            lines = file.readlines()
                            en_terms = set([ item.strip() for item in lines ])
                            trie = build_trie(en_terms)
                            dictionary_info_dict[dictionary_id]['trie'][lang_code] = trie
                
                for lang_user_dict_path, lang_code in list_language_paths(bucket_name=bucket, prefix_path=f"{s3_prefix}/{dictionary_id}/"):
                    if lang_code == LangCode.EnUs.value:
                        continue

                    logger.info(f'lang_user_dict_path: {lang_user_dict_path}, lang_code:{lang_code}')
                    local_file = f'/tmp/{dictionary_id}_{lang_code}_user_dict.txt'
                    user_dict_s3_key = f"{lang_user_dict_path}user_dict.txt"
                    s3.download_file(bucket, user_dict_s3_key, local_file)
                    with open(local_file, 'r') as file:
                        lines = file.readlines()
                        terms = set([ item.strip() for item in lines ])
                        if en_terms:
                            terms = terms | en_terms
                        trie = build_trie(terms)
                        dictionary_info_dict[dictionary_id]['trie'][lang_code] = trie
                
                logger.info(f'File downloaded successfully: {local_file}')
            except Exception as e:
                logger.exception(f'Error downloading file: {e}')

        if dictionary_id not in dictionary_info_dict:
            raise RuntimeError(f"There is no data for {dictionary_id}")

        return True

    except Exception as e:
        logger.exception(f'refresh_dictionary err: {e}')
        return False

def is_english(text):
    unicode_punctuation = [' ','«','»','¿','‐','‑','‒','–','—','―','‖','‘','’','“','”','†','‡','•','…','‰','′','″','※','‼','⁇','⁈','⁉','₠','₡','₢','₣','₤','₥','₦','₧','₨','₩','₪','₫','€','₹','∀','∂','∃','∅','∇','∈','∉','∋','∑','−','√','∞','∠','∧','∨','∩','∪','　','、','。','〃','々','〈','〉','《','》','「','」','『','』','【','】','〔','〕','〖','〗','〜','！','＂','＃','＄','％','＆','＇','（','）','＊','＋','，','－','．','／','：','；','＜','＝','＞','？','＠','︰','︱','︳','﹉','﹐','﹑','﹒','﹔','﹕','﹖','﹗','｡','｢','｣','､','･']
    allowed = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    allowed_list = list(allowed) + unicode_punctuation
    return all(char in allowed_list for char in text)

def process_request(idx, src_content, src_lang, dest_lang, dictionary_id, request_type, model_id, with_term_mapping):
    global dictionary_info_dict, ddb_table_dict

    words = []
    multilingual_term_mapping = []
    json_obj = {}

    # if dictionary is not passed, words will be []
    if dictionary_id:
        trie = dictionary_info_dict.get(dictionary_id).get('trie').get(src_lang)

        start_time = time.time()
        if is_english(src_content):
            words = mfm_segment_trie_en(src_content, trie)
        else:
            words = mfm_segment_trie(src_content, trie)
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"[task-{idx}][2] Elapsed time: {elapsed_time} seconds")

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
        logger.info(f"[task-{idx}][3] Elapsed time: {elapsed_time} seconds")

    if request_type == 'term_mapping':
        json_obj["term_mapping"] = multilingual_term_mapping
        return json_obj

    if with_term_mapping:
        json_obj["term_mapping"] = multilingual_term_mapping

    start_time = time.time()

    src_content_with_placeholder, exclusions, affix = replace_no_translation_text_to_placeholder(src_content)
    logger.info(f"src_content:{repr(src_content)}")
    logger.info(f"src_content_with_placeholder:{repr(src_content_with_placeholder)}")
    logger.info(f"exclusions:{exclusions}")
    logger.info(f"affix:{affix}")

    logger.info(f"src_content_with_placeholder:{src_content_with_placeholder}")
    logger.info(f"exclusions:{exclusions}")
    prompt = construct_translate_prompt(src_content_with_placeholder, src_lang, dest_lang, multilingual_term_mapping)
    logger.info(f"prompt:{prompt}")
    translated_text_with_placeholder = invoke_bedrock(model_id=model_id, prompt=prompt, prefill_str=f'<translation_{dest_lang}>', stop=[f'</translation_{dest_lang}>'])

    
    translated_text = replace_placeholder_to_origin_text(translated_text_with_placeholder, exclusions, affix)
    logger.info(f"translated_text_with_placeholder:{repr(translated_text_with_placeholder)}")
    logger.info(f"translated_text:{translated_text}")
    logger.info(f"translated_text:{repr(translated_text)}")
    json_obj["translated_text"] = translated_text
    json_obj["model"] = model_id
    json_obj["glossary_config"] = { "glossary": dictionary_id }
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"[task-{idx}][4] Elapsed time: {elapsed_time} seconds")
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
        #todo update dictionary id with version here
        # 1.check translate_meta table exist, if not, keep dictionary_id unchanged
        # 2.check translate_meta table exist, and dictionary_id is in translate_meta table, if not, keep dictionary_id unchanged
        # 3.check translate_meta table exist, and dictionary_id is in translate_meta table, check version for dictionary_id 
        #   if version is default, keep dictionary_id unchanged
        #   if version is not default, update dictionary_id to dictionary_id_version

        translate_meta_table = dynamodb.Table(Translate_Meta_Table_Name)
        try:
            response = translate_meta_table.get_item(Key={'dict': dictionary_id})
            if 'Item' in response:
                version = response['Item']['version']
                if version != 'default':
                    dictionary_id = f"{dictionary_id}_{version}"
                    logger.info(f"update dictionary_id to {dictionary_id}")
        except dynamodb.meta.client.exceptions.ResourceNotFoundException:
            logger.warning(f"Table translate_meta doesn't exist, dictionary_id: {dictionary_id}")
            pass    

        succeded = refresh_dictionary(bucket, s3_prefix, dictionary_id)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"[1] Elapsed time: {elapsed_time} seconds")

        if not succeded:
            raise RuntimeError(f"Error: There is no user_dict for {dictionary_id} on S3 ")

    async def run_async():
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            tasks = [
                loop.run_in_executor(
                    pool,
                    process_request,
                    idx, src_content, src_lang, dest_lang, dictionary_id, request_type, model_id, response_with_term_mapping
                )
                for idx, src_content in enumerate(src_contents)
            ]
        return await asyncio.gather(*tasks)
    
    results = asyncio.run(run_async())
    return { "translations" : results }

if __name__ == "__main__":
    def _test(src_content):

        src_content_with_placeholder, exclusions, line_break_count = replace_no_translation_text_to_placeholder(src_content)
        translated_text = replace_placeholder_to_origin_text(src_content_with_placeholder, exclusions, line_break_count)
        # print(f"src_content:{repr(src_content)}")
        # print(f"src_content_with_placeholder:{repr(src_content_with_placeholder)}")
        # print(f"exclusions:{exclusions}")
        # print(f"line_break_count:{line_break_count}")
        # print(f"translated_text:{repr(translated_text)}")

        print(f"{src_content == translated_text}: {repr(src_content)} -> {repr(translated_text)}")
    
    import random

    test_contents = [
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + " \nTest string 1" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Hello, world!" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Python is awesome" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Random newlines test" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Testing, testing, 1-2-3" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Newline madness" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Leading and trailing spaces" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "This is a test string" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Random number of newlines" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))),
        ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10))) + "Final test string" + ''.join(random.choices(['\n', '\t', ' ', '\r'], k=random.randint(0, 10)))
    ]

    for src_content in test_contents:
        _test(src_content)
