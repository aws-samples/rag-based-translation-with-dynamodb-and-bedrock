import streamlit as st
from utils import translate_tool as trans

# 设置页面标题
st.set_page_config(page_title="LLM Translator")

# 创建输入文本框
input_text = st.text_area("输入要翻译的文本", height=200)

# 创建选择源语言和目标语言的下拉菜单
languages = ["English", "中文", "Español", "Français", "Deutsch", "Русский"]
lang_options ={
    "English": "EN",
    "简体中文": "CHS",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Русский": "ru"
}
source_lang_option = st.selectbox("选择源语言", lang_options.keys())
target_lang_option = st.selectbox("选择目标语言", lang_options.keys())
source_lang = lang_options[source_lang_option]
target_lang = lang_options[target_lang_option]

# 定义模拟翻译函数
def mock_translate(text, source, target):
    # 这里只是简单地将输入文本反转作为模拟翻译结果
    return text[::-1]

# 创建翻译按钮
if st.button("翻译"):
    if input_text:
        # translation = mock_translate(input_text, source_lang, target_lang)
        translation = trans.translate_content(input_text, source_lang, target_lang)
        st.divider()
        st.text_area("翻译结果", translation, height=200)
    else:
        st.write("请输入要翻译的文本")
