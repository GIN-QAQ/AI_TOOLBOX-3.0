import streamlit as st
from utils1 import generate_script

st.title("🎬 视频脚本生成器 ")

# 尝试从会话状态获取 OpenAI API 密钥，如果不存在则显示输入框
if 'openai_api_key' not in st.session_state:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key

# 从会话状态获取 OpenAI API 密钥
if 'openai_api_key' in st.session_state:
    openai_api_key = st.session_state['openai_api_key']

subject = st.text_input("💡 请输入视频的主题")
video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）",
                               min_value=0.1, max_value=3.0, step=0.1)
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）",
                       value=0.5, min_value=0.0, max_value=1.0, step=0.1)
submit = st.button("生成脚本")

if submit:
    if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
        st.info("请输入你的OpenAI API密钥")
        st.stop()
    if not subject:
        st.info("请输入视频的主题")
        st.stop()
    if not video_length >= 0.1:
        st.info("视频长度需要大于或等于0.1")
        st.stop()
    with st.spinner("AI正在思考中，请稍等..."):
        # 确保在调用函数时，openai_api_key 已经正确获取
        search_result, title, script = generate_script(subject, video_length, creativity,
                                                       st.session_state['openai_api_key'])
    st.success("视频脚本已生成！")
    st.subheader("🔥 标题：")
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)