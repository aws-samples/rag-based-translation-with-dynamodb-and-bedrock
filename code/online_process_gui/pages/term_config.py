import streamlit as st
import boto3

if "init_config" not in st.session_state:
    st.session_state["config_path"] = 'sample-bucket/user_dict/user_dict.txt'
    st.session_state["init_config"] = None

st.markdown('## 配置专词')

s3_client = boto3.client(
    's3'
)

file_path = st.text_input("输入 S3 文件路径(替换sample-bucket为你自己的bucket)", st.session_state["config_path"])
read_button = st.button("显示专词配置")

if read_button or file_path != 'sample-bucket/user_dict/user_dict.txt':
    try:
        st.session_state["config_path"] = file_path
        # 从 S3 读取文件内容
        bucket_name, key = st.session_state["config_path"].split('/', 1)
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        st.session_state["init_config"] = response['Body'].read().decode('utf-8')
        update_content = st.text_area("", st.session_state["init_config"], height=200)
    except Exception as e:
        st.error(f"Error reading file from S3: {e}")
# if update_content!=st.session_state["init_config"]:
    update_button = st.button("更新专词配置")
    if update_button:
        pass
        bucket_name, key = st.session_state["config_path"].split('/', 1)
        s3_client.put_object(Body=update_content.encode('utf-8'), Bucket=bucket_name, Key=key)
        st.success("文件已成功更新。")
    