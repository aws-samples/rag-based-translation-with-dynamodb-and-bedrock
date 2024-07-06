import os
import time
import json
import boto3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

import streamlit as st
from streamlit_ace import st_ace

from utils.utils import upload_to_s3, query_term, update_term_mapping, list_translate_mapping_tables, start_glue_job, get_glue_job_run_status

parent_dir = str(Path(__file__).parent.parent.parent.parent)
dotenv_path = os.path.join(parent_dir, 'deploy/.env')
s3 = boto3.client('s3')
print(f"dotenv_path:{dotenv_path}")

load_dotenv(dotenv_path)
bucket = os.getenv("UPLOAD_BUCKET")
print(f"bucket of translate service: {bucket}")

all_dictionaries = list_translate_mapping_tables()

col1, col2 = st.columns(2)
with col1:
    dictionary_name = st.selectbox("选择现有专词映射表", all_dictionaries)

with col2:
    new_dictionary_name = st.text_input(label="构建新的专词映射表", value="")

dictionary_name = new_dictionary_name if new_dictionary_name else dictionary_name
# 文件上传组件
uploaded_file = st.file_uploader("选择要上传的文件", type=["json"])

if st.button("上传"):
    s3_key = f"translate/{dictionary_name}/{uploaded_file.name}"
    print(f"s3_key:{s3_key}")
    status, msg = upload_to_s3(uploaded_file, bucket, s3_key)
    if not status:
        st.error(f"上传失败: {msg}")
    else:
        st.write(msg)
        placeholder = st.empty()
        elapse_secs = 0
        run_id = start_glue_job(s3_key, bucket, dictionary_name)
        job_status = ''
        while True:
            job_status = get_glue_job_run_status(run_id)
            if job_status == 'SUCCEEDED':
                placeholder.write(f"glue job status : {job_status}")
                break
            elif job_status in ['STARTING', 'RUNNING']:
                placeholder.write(f"glue job status: {job_status}, {elapse_secs} secconds elapsed")
                time.sleep(10)
                elapse_secs += 10
            else:
                placeholder.write(f"glue job status : {job_status}")
                break

st.divider()
json_container = None

search_term = st.text_input("专词搜索")
searched_item = query_term(dictionary_name, search_term)

if searched_item is None:
    st.warning(f"没有查到对应专词 - {search_term}")

col11, col22 = st.columns(2)

with col11:
    st.write("原始版本")
    json_container = st.empty()
    json_container.json(searched_item)

with col22:
    formatted_json = json.dumps(searched_item, indent=4, ensure_ascii=False)
    json_editor = st.empty()
    json_editor.text_area(label='编辑版本', value=formatted_json, key="text_input", height=550)
    if st.button("修改"):
        try:
            edited_item = json.loads(st.session_state.text_input)
            print("edited_item")
            print(edited_item)
            if edited_item is not None:
                if edited_item.get('term') != searched_item.get('term'):
                    st.warning("只允许修改mapping和entity.")
                else:     
                    update_term_mapping(dictionary_name, edited_item.get('term'), edited_item.get('entity'), edited_item.get('mapping'))
                    st.success(f"已更新项目: {edited_item.get('term')}")
                    json_container.json(edited_item)
        except Exception as e:
            st.warning(f"字典数据格式有误，请检查, {e}")
