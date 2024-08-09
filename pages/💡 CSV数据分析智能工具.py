import pandas as pd
import streamlit as st
from utils5 import dataframe_agent


def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)


st.title("💡 CSV数据分析智能工具 ")

# 尝试从会话状态获取 OpenAI API 密钥，如果不存在则显示输入框
if 'openai_api_key' not in st.session_state:
    openai_api_key = st.text_input("请输入你的OpenAI API密钥：", type="password")
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key

# 从会话状态获取 OpenAI API 密钥
if 'openai_api_key' in st.session_state:
    openai_api_key = st.session_state['openai_api_key']

data = st.file_uploader("上传你的数据文件（CSV格式）：", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")
button = st.button("生成回答")

if button:
    # 在此处添加判断，确保 openai_api_key 已定义
    if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
        st.info("请输入你的OpenAI API密钥")
    elif "df" not in st.session_state:
        st.info("请先上传数据文件")
    elif st.session_state['openai_api_key'] and "df" in st.session_state:
        with st.spinner("AI正在思考中，请稍后..."):
            response_dict = dataframe_agent(st.session_state['openai_api_key'], st.session_state["df"], query)
        if "answer" in response_dict:
            st.write(response_dict["answer"])
        if "table" in response_dict:
            st.table(pd.DataFrame(response_dict["table"]["data"],
                                  columns=response_dict["table"]["columns"]))
        if "bar" in response_dict:
            create_chart(response_dict["bar"], "bar")
        if "line" in response_dict:
            create_chart(response_dict["line"], "line")
        if "scatter" in response_dict:
            create_chart(response_dict["scatter"], "scatter")
