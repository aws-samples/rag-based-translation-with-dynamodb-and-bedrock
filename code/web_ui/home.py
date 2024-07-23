import streamlit as st
from utils.utils import translate_content, list_translate_mapping_tables, query_term, update_term_mapping, get_random_item

# 设置页面标题
st.set_page_config(page_title="LLM Translator")

col1, col2 = st.columns(2)

all_dictionaries = list_translate_mapping_tables()
model_id_list = ['anthropic.claude-3-sonnet-20240229-v1:0', 'anthropic.claude-3-5-sonnet-20240620-v1:0', 'anthropic.claude-3-haiku-20240307-v1:0', 'anthropic.claude-3-opus-20240229-v1:0']

if not all_dictionaries:
    all_dictionaries = ['default_dictionary']

dictionary_name = None
with col1:
    dictionary_name = st.selectbox("选择专词映射表", all_dictionaries)

random_item = get_random_item(dictionary_name)

if random_item:
    languages = list(random_item["mapping"].keys())
    en_index = languages.index('EN')
    chs_index = languages.index('CHS')
else:
    languages = ['-']
    en_index = 0
    chs_index = 0


# 在第一列中放置第一个 selectbox
with col1:
    source_lang = st.selectbox(label="选择源语言", options=languages, index=chs_index)

# 在第二列中放置第二个 selectbox
with col2:
    choosed_model_id = st.selectbox("选择模型", model_id_list)
    target_lang = st.selectbox(label="选择目标语言", options=languages, index=en_index)

# 创建输入文本框
input_text = st.text_area("输入要翻译的文本", height=150)

# 创建翻译按钮
if st.button("翻译"):
    if input_text:
        translation, term_mapping = translate_content(contents=[input_text], source_lang=source_lang, target_lang=target_lang, dictionary_id=dictionary_name, model_id=choosed_model_id)
        st.divider()
        st.text_area("翻译结果", translation.strip(), height=150)
        st.text_area("映射关系", term_mapping, height=150)
    else:
        st.write("请输入要翻译的文本")
