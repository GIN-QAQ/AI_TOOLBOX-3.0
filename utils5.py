
# 💡 CSV数据分析智能工具

import json
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


PROMPT_TEMPLATE = """
你是一位数据分析助手，你的回应内容取决于用户的请求内容。

1. 对于文字回答的问题，按照这样的格式回答：
   {"answer": "<你的答案写在这里>"}
例如：
   {"answer": "订单量最高的产品ID是'MNWC3-067'"}

2. 如果用户需要一个表格，按照这样的格式回答：
   {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

3. 如果用户的请求适合返回条形图，按照这样的格式回答：
   {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

4. 如果用户的请求适合返回折线图，按照这样的格式回答：
   {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

5. 如果用户的请求适合返回散点图，按照这样的格式回答：
   {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
   
注意：我们只支持三种类型的图表："bar", "line" 和 "scatter"。


请将所有输出作为JSON字符串返回。请注意要将"columns"列表和数据列表中的所有字符串都用双引号包围。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

你要处理的用户请求如下： 
"""


def dataframe_agent(openai_api_key, df, query):
    """
        处理用户的数据分析请求，并返回相应的结果

        参数：
        openai_api_key (str)：OpenAI API 密钥
        df (pandas.DataFrame)：要分析的数据框
        query (str)：用户的查询请求

        返回：
        dict：根据用户请求生成的响应字典
        """
    try:
        model = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            base_url="https://api.aigc369.com/v1",
            temperature=0
        )
        agent = create_pandas_dataframe_agent(
            llm=model,
            df=df,
            agent_executor_kwargs={"handle_parsing_errors": True},
            verbose=True,
            allow_dangerous_code=True
        )
        prompt = PROMPT_TEMPLATE + query
        response = agent.invoke({"input": prompt})
        response_dict = json.loads(response["output"])
        return response_dict
    except Exception as e:
        # 处理可能出现的异常，例如 API 调用错误、数据格式错误等
        print(f"发生错误: {e}")
        return {"answer": "抱歉，处理您的请求时发生错误"}
