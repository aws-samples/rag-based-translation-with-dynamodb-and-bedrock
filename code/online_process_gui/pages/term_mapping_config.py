import boto3
import pandas as pd
import streamlit as st

# 创建 DynamoDB 客户端
dynamodb = boto3.resource('dynamodb')

# 获取表对象
chs_table = dynamodb.Table('rag_translate_chs_table')
chs_response = chs_table.scan()
chs_items = chs_response['Items']

while 'LastEvaluatedKey' in chs_response:
    chs_response = chs_table.scan(ExclusiveStartKey=chs_response['LastEvaluatedKey'])
    chs_items.extend(chs_response['Items'])

chs_df = pd.json_normalize(chs_items)
chs_edited_df = chs_df.copy()

st.info("中文专词映射:")
chs_edited_df = st.data_editor(chs_edited_df)

if st.button("保存中文专词修改"):
    if chs_edited_df is not None:
        for index, row in chs_edited_df.iterrows():
            item = row.to_dict()
            chs_table.put_item(Item=item)
            st.success(f"已更新项目: {item}")
    else:
        st.warning("没有进行任何修改。")
        
st.divider()
en_table = dynamodb.Table('rag_translate_en_table')
en_response = en_table.scan()
en_items = en_response['Items']

while 'LastEvaluatedKey' in en_response:
    en_response = en_table.scan(ExclusiveStartKey=en_response['LastEvaluatedKey'])
    en_items.extend(en_response['Items'])

en_df = pd.json_normalize(en_items)
en_edited_df = en_df.copy()
st.info('英文专词映射:')
en_edited_df = st.data_editor(en_edited_df)
if st.button("保存英文专词修改"):
    if en_edited_df is not None:
        for index, row in en_edited_df.iterrows():
            item = row.to_dict()
            en_table.put_item(Item=item)
            st.success(f"已更新项目: {item}")
    else:
        st.warning("没有进行任何修改。")