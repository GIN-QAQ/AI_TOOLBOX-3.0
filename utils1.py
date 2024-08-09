
# 🎬 视频脚本生成器

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper


def generate_script(subject, video_length, creativity, openai_api_key):
    """
    生成视频脚本的函数

    参数：
    subject (str)：视频的主题
    video_length (float)：视频的时长（分钟）
    creativity (float)：脚本的创造力水平
    openai_api_key (str)：OpenAI API 密钥

    返回：
    tuple：包含维基百科搜索结果、标题和脚本的元组
    """
    # 检查输入参数的有效性
    if not subject:
        raise ValueError("主题不能为空")
    if video_length < 0.1:
        raise ValueError("视频长度必须大于或等于 0.1 分钟")

    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
           ("human",
            """你是一位短视频频道的博主，根据以下标题和相关信息，为短视频频道写一个视频脚本。
            视频标题: {title}，视频时长: {duration}分钟，生成的脚本的长度尽量遵循视频时长的要求，
            要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间、结尾】分隔，
            整体内容的表达方式尽量轻松有趣，吸引年轻人。
            脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略:
```{wikipedia_search}```""")
        ]
    )

    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=creativity, base_url="https://api.aigc369.com/v1")

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    try:
        search = WikipediaAPIWrapper(lang="zh")
        search_result = search.run(subject)
    except Exception as e:
        # 这里可以打印错误信息或者采取其他适当的处理方式，例如设置搜索结果为空字符串
        print(f"获取维基百科搜索结果时出错: {e}")
        search_result = ""

    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content

    return search_result, title, script
