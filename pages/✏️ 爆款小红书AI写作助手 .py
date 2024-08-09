import streamlit as st
from utils2 import generate_xiaohongshu


st.header("✏️ 爆款小红书AI写作助手 ")

# 尝试从会话状态获取 OpenAI API 密钥，如果不存在则显示输入框
if 'openai_api_key' not in st.session_state:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key

# 从会话状态获取 OpenAI API 密钥
if 'openai_api_key' in st.session_state:
    openai_api_key = st.session_state['openai_api_key']

theme = st.text_input("主题")
submit = st.button("开始写作")

if submit:
    # 在此处添加判断，确保 openai_api_key 已定义
    if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
        st.info("请输入你的OpenAI API密钥")
        st.stop()
    if not theme:
        st.info("请输入生成内容的主题")
        st.stop()
    with st.spinner("AI正在努力创作中，请稍等..."):
        # 确保在调用函数时，openai_api_key 已经正确获取
        result = generate_xiaohongshu(theme, st.session_state['openai_api_key'])
    st.divider()
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("##### 小红书标题1")
        st.write(result.titles[0])
        st.markdown("##### 小红书标题2")
        st.write(result.titles[1])
        st.markdown("##### 小红书标题3")
        st.write(result.titles[2])
        st.markdown("##### 小红书标题4")
        st.write(result.titles[3])
        st.markdown("##### 小红书标题5")
        st.write(result.titles[4])
    with right_column:
        st.markdown("##### 小红书正文")
        st.write(result.content)
