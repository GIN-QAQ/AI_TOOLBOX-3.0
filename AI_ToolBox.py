import streamlit as st

st.header("AI_ToolBox")
st.markdown("""##### 这是一个AI小工具箱，通过点击左侧边栏的不同项目可以按照您的需求跳转到相应界面来帮助您完成任务。首先，您需要在左侧输入您的OPENAI_API_KEY来保证后续操作顺利完成 """)


with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
    submit = st.button("提交")

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key

if submit:
    if openai_api_key:
        st.session_state['openai_api_key'] = openai_api_key
        st.markdown("### 密钥已保存，请选择您需要的小工具并使用")
    else:
        st.info("请输入您的 OpenAI API 密钥")

# 可以添加一些后续的操作或展示，例如根据是否有密钥显示不同的内容
if st.session_state.openai_api_key:
    st.write("您已成功提交 API 密钥，可以继续操作")
else:
    st.write("尚未提交有效的 API 密钥")
# if submit and not openai_api_key:
#     st.info("请输入你的OpenAI API密钥")
#     st.stop()
# if submit and openai_api_key:
#     st.session_state.openai_api_key = openai_api_key
#     st.markdown("### 请选择您需要的小工具并使用")
