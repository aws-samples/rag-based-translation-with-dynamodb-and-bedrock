import streamlit as st
from utils.menu import menu_with_redirect
import os
import time
import json
import boto3
import pandas as pd
from pathlib import Path
# from dotenv import load_dotenv

# from streamlit_ace import st_ace

from utils.utils import upload_to_s3, query_term, update_term_mapping, list_dictionary_ids, start_glue_job, get_glue_job_run_status
from utils.utils import upload_bucket, term_mapping_quality_check, get_dict_with_version, get_current_version, update_current_version

st.set_page_config(
    page_title="Term Config",
    page_icon="🔑",
)

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.role not in ["admin", "super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

# Here goes your normal streamlit app
# parent_dir = str(Path(__file__).parent.parent.parent)
# dotenv_path = os.path.join(parent_dir, 'deploy/.env')
# print(f"dotenv_path:{dotenv_path}")
# load_dotenv(dotenv_path)

bucket = upload_bucket
# print(f"bucket of translate service: {bucket}")

dictionary_name_to_upload = None
version_to_create = None
dictionary_is_new = False

all_dictionaries = list_dictionary_ids()
# print(f"all_dictionaries:{all_dictionaries}")
dict_with_version = get_dict_with_version(all_dictionaries)
# print(f"dict_with_version:{dict_with_version}")

tab1, tab2, tab3 = st.tabs(["创建/更新专词映射表", "专词映射表版本管理", "专词映射表内容搜索"])

with tab1:
    create_new_dict = st.checkbox("创建新的专词映射表", value=not all_dictionaries)
    if create_new_dict:
        dictionary_name = st.text_input(label="构建新的专词映射表", value="Default")
        if ' ' in dictionary_name:
            st.error("映射字典名称不能存在空格")
        dictionary_is_new = True
        dictionary_name_to_upload = dictionary_name
    else:
        dictionary_name = st.selectbox("现有专词映射表", dict_with_version.keys())
        if len(dict_with_version[dictionary_name]) > 1:
            st.info(f"字典{dictionary_name}存在如下版本")
            st.write(',  '.join(dict_with_version[dictionary_name]))
            max_version = dict_with_version[dictionary_name][-1]
            if max_version == 'default':
                version_to_create = 'v1'
            else:
                version_to_create = f'v{int(max_version.split("v")[1]) + 1}'
        else:
            st.info(f"{dictionary_name} 只有一个版本")
            version_to_create = 'v1'
        dictionary_is_new = False
        dictionary_name_to_upload = dictionary_name+'_'+version_to_create
        # st.info(f"将创建新版本: {version_to_create}, 新专词为: {dictionary_name_to_upload}")
        
        # st.write(dict_with_version[dictionary_name])


    # dictionary_name = new_dictionary_name if new_dictionary_name else dictionary_name
    # 文件上传组件
    uploaded_file = st.file_uploader("选择要上传的文件", type=["json"])

    upload_btn_status = False
    if uploaded_file:
        warn_list, error_list = term_mapping_quality_check(uploaded_file)

        if error_list:
            st.error(f"共有{len(error_list)}个专词映射中包含空字符!")
            # st.json(json.dumps(error_list))
            json_str = json.dumps(error_list, indent=2, ensure_ascii=False)
            json_bytes = json_str.encode('utf-8')  # 显式指定使用 UTF-8 编码
            st.download_button(
                label="📥 Download Error Report",
                data=json_bytes,
                file_name="error.json",
                mime="application/json",
                help="Click to download the full error report in JSON format"
            )
        else:
            st.success("没有发现专词映射表包含空字符。")

        if warn_list:
            st.warning(f"共有{len(warn_list)}个专词映射中包含过短专词，会对专词质量造成影响!")
            # st.json(json.dumps(warn_list))
            warn_json = json.dumps(warn_list, indent=2, ensure_ascii=False)
            warn_bytes = warn_json.encode('utf-8')  # 显式指定使用 UTF-8 编码
            st.download_button(
                label="Download Warn List",
                data=warn_bytes,
                file_name="warn.json",
                mime="application/json"
            )
        else:
            st.success("没有发现专词映射表包含过短专词。")
        
        if not dictionary_is_new:
            st.info(f"点击上传按钮, 将创建新版本: {version_to_create}, 新专词为: {dictionary_name_to_upload}")


        upload_btn_status = bool(error_list)

        if st.button("上传", disabled=upload_btn_status):
            s3_key = f"translate/{dictionary_name_to_upload}/{uploaded_file.name}"
            print(f"dictionary_name_to_upload:{dictionary_name_to_upload}, s3_key:{s3_key}")
            status, msg = upload_to_s3(uploaded_file, bucket, s3_key)
            if not status:
                st.error(f"上传失败: {msg}")
            else:
                st.write(msg)
                placeholder = st.empty()
                elapse_secs = 0
                run_id = start_glue_job(s3_key, bucket, dictionary_name_to_upload)
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

@st.dialog("修改版本")
def modify_version_dialog(dict, version):
    st.write(f"请确认将修改{dict}的版本为{version}")
    if st.button("确认"):
        update_current_version(dict, version)
        st.rerun()

with tab2:
    dictionary_name = st.selectbox("现有专词映射表", dict_with_version.keys(), key="dict_name_for_version_management")
    if len(dict_with_version[dictionary_name])==1:
        st.warning(f"字典{dictionary_name}只有默认版本")
    else:
        st.info(f"字典{dictionary_name}存在如下版本")
        st.caption(',  '.join(dict_with_version[dictionary_name]))
        current_version = get_current_version(dictionary_name)
        st.info(f"当前字典版本:")
        if current_version is None:
            st.caption(f"{dictionary_name}")
        else:
            st.caption(f"{current_version}")

        if st.checkbox("修改版本"):
            selected_version = st.selectbox("选择版本", dict_with_version[dictionary_name], key="selected_version_to_update")
            if st.button("修改", key="modify_version_btn"):
                modify_version_dialog(dictionary_name, selected_version)
                # update_current_version(dictionary_name, selected_version)

                # st.rerun()

with tab3:
    dictionary_name = st.selectbox("专词映射表", dict_with_version.keys(), key="dict_name_for_search")
    if len(dict_with_version[dictionary_name])>1:
        dict_version = st.selectbox("选择版本", dict_with_version[dictionary_name])
        if dict_version != 'default':
            dictionary_name = dictionary_name+'_'+dict_version

    st.write(f"当前字典: {dictionary_name}")

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