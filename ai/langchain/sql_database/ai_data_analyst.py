from langchain.globals import set_verbose
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor
from langchain_openai import ChatOpenAI
import streamlit as st
import streamlit.components.v1 as components


set_verbose(False)
st.set_page_config(page_title="AI数据分析师", layout="wide")

system_msg = """
你是一个经验丰富的数据分析师，会使用clickhouse sql分析数据。
你的回答是一个html代码编写的数据分析报告，数据报告中的表格和图表使用echarts实现，并且echarts cdn使用bootcdn。
数据分析报告不得包含明细数据，并至少包含如下几部分内容：
1. 摘要
1.1 研究的问题和目标
1.2 主要发现、结论和建议
2. 数据源描述（详细描述数据源，包括数据库名称、表结构、字段类型等）
3. SQL查询概述
3.1 SQL查询的目的和逻辑
3.2 查询中使用的SQL语句
4. 探索性分析（使用图表来探索数据特征、分布、趋势和模式，图表支持toolbox所有特性）
5. 结果分析（详细解释分析结果）
6. 结论与建议
6.1 主要发现和结论
6.2 建议和行动方案
如果你觉得你不知道如何编写代码来回答问题，就直接使用html代码返回"我并不知道"作为答案。
"""

messages = [
    ("system", system_msg),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("human", "{question}"),
    AIMessage(content=SQL_FUNCTIONS_SUFFIX),
]

prompt = ChatPromptTemplate.from_messages(messages)

llm = ChatOpenAI(base_url="https://ip", api_key="any", model="gpt-4o", temperature=0)
db_uri = "clickhouse://username:password@ip:port/db"
db = SQLDatabase.from_uri(db_uri)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
context = toolkit.get_context()
tools = toolkit.get_tools()

agent = create_openai_tools_agent(llm, tools, prompt)


agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
)

# Optionally, specify your own session_state key for storing messages
msgs = StreamlitChatMessageHistory(key="special_app_key")

if len(msgs.messages) == 0:
    msgs.add_ai_message(
        "嗨！我是AI数据分析师，可以帮您分析数据，并提供一份数据分析报告，请提出您的数据分析问题。"
    )

chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: msgs,  # Always return the instance created earlier
    input_messages_key="question",
    history_messages_key="history",
)


def write_html(content):
    if (
        content.startswith("```html")
        and content.endswith("```")
        or content.startswith("<!DOCTYPE html>")
        and content.endswith("</html>")
    ):
        html = "\n".join(content.split("\n")[1:-1])
        components.html(html, height=1000, scrolling=True)
    else:
        st.chat_message("ai").write(content)


for msg in msgs.messages:
    if msg.type == "ai":
        write_html(msg.content)
    else:
        st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
    config = {"configurable": {"session_id": "any"}}
    try:
        response = chain_with_history.invoke({"question": prompt}, config)
        # st.chat_message("ai").write(response.content)

        # with st.expander("html代码："):
        #     st.chat_message("ai").write(response.get("output"))

        write_html(response.get("output"))
    except BaseException as e:
        st.chat_message("ai").write("分析失败，请重新提问。")
        with st.expander("异常信息："):
            st.chat_message("ai").write(e)


# 启动命令：streamlit run --theme.base=light ai_data_analyst.py
# 参考提问：
# 1. 最近一周xyio设备数情况
# 2. 上个月的营收情况
