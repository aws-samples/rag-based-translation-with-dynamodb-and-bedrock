import streamlit as st
import time
from utils.menu import menu
from utils.utils import (
    list_dictionary_ids,
    list_supported_language_codes,
    list_translate_models,
    translate_content,
)

# 配置 Streamlit 页面
st.set_page_config(page_title="LLM Translate", page_icon="⚧")

# 显示应用程序的菜单
menu()

# 添加应用标题
st.title("LLM Translate Tool")

# 获取可用的字典、模型和支持的语言代码列表
model_list = list_translate_models()
dictionaries = list_dictionary_ids() or ['default_dictionary']
supported_lang_codes_dict = list_supported_language_codes()

# 创建两列布局
col1, col2 = st.columns(2)

# 在第一列中选择字典和源语言
with col1:
    dictionary_name = st.selectbox(
        "专词映射表",
        dictionaries
    )
    source_lang_label = st.selectbox(
        "源语言",
        supported_lang_codes_dict.keys()
    )
    source_lang = supported_lang_codes_dict.get(source_lang_label)

# 在第二列中选择模型和目标语言
with col2:
    model_id = st.selectbox("翻译模型", model_list)
    target_lang_label = st.selectbox(
        "目标语言",
        supported_lang_codes_dict.keys()
    )
    target_lang = supported_lang_codes_dict.get(target_lang_label)

# 创建输入文本框以输入要翻译的文本
input_text = st.text_area("请在此输入要翻译的文本", height=150)

lambda_alias = st.selectbox("Lambda Alias", ["prod", "staging"])

# 创建翻译按钮并显示结果
if st.button("开始翻译"):
    if input_text:
        with st.spinner('正在翻译中，请稍候...'):
            # 开始计时
            start_time = time.time()

            # 执行翻译
            translation, term_mapping = translate_content(
                contents=[input_text],
                source_lang=source_lang,
                target_lang=target_lang,
                dictionary_id=dictionary_name,
                model_id=model_id,
                lambda_alias=lambda_alias,
            )

            # 计算翻译耗时
            elapsed_time = time.time() - start_time

        # 显示翻译结果和映射关系
        st.text_area("翻译后的文本", translation.strip(), height=150)
        st.text_area("专词映射关系", term_mapping, height=150)

        # 显示翻译耗时
        st.info(f"翻译耗时: {elapsed_time:.2f} 秒")
    else:
        st.warning("请输入要翻译的文本")