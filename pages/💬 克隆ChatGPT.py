import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils3 import get_chat_response

st.title("💬 克隆ChatGPT ")

# 尝试从会话状态获取 OpenAI API 密钥，如果不存在则显示输入框
if 'openai_api_key' not in st.session_state:
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key

# 从会话状态获取 OpenAI API 密钥
if 'openai_api_key' in st.session_state:
    openai_api_key = st.session_state['openai_api_key']

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    # 在此处添加判断，确保 openai_api_key 已定义
    if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
        st.info("请输入你的OpenAI API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"], st.session_state['openai_api_key'])
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)
