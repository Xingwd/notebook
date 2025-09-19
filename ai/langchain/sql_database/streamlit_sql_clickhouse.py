from langchain.globals import set_verbose

set_verbose(False)

from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)

history = StreamlitChatMessageHistory(key="chat_messages")

history.add_user_message("hi!")
history.add_ai_message("whats up?")

# Optionally, specify your own session_state key for storing messages
msgs = StreamlitChatMessageHistory(key="special_app_key")

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://ip:port/v1", api_key="any", model="gpt-4o", temperature=0
)

from langchain_community.utilities.sql_database import SQLDatabase

db_uri = "clickhouse://username:password@127.0.0.1:8123/db"
db = SQLDatabase.from_uri(db_uri)

from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
context = toolkit.get_context()
tools = toolkit.get_tools()

from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain_core.messages import AIMessage


system_msg = f"""
你是一个经验丰富的数据分析师，每次回复时，如果有查询sql和数据结果，
在回复中附上查询sql和数据结果表格，并输出合适的echarts图表的html代码，
其中echarts cdn地址使用bootcdn。
"""

system_msg = f"""
你是一个经验丰富的数据分析师，会使用clickhouse sql分析数据。
每次回复时，如果有查询sql和数据结果，在回复中附上查询sql和数据结果表格，
并输出合适的echarts图表的html代码，其中echarts cdn地址使用bootcdn。
然后对数据结果进行解读，并给出运营建议。
"""

messages = [
    ("system", system_msg),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("human", "{question}"),
    AIMessage(content=SQL_FUNCTIONS_SUFFIX),
]

prompt = ChatPromptTemplate.from_messages(messages)

from langchain.agents import create_openai_tools_agent
from langchain.agents.agent import AgentExecutor

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
)

chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: msgs,  # Always return the instance created earlier
    input_messages_key="question",
    history_messages_key="history",
)

import streamlit as st

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

import streamlit.components.v1 as components

if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
    config = {"configurable": {"session_id": "any"}}
    response = chain_with_history.invoke({"question": prompt}, config)
    # st.chat_message("ai").write(response.content)
    st.chat_message("ai").write(response.get("output"))

    text = response.get("output")
    ps = text.split("\n")
    chart_html, add_p = [], False
    for p in ps:
        if p.startswith("```html"):
            add_p = True
            continue
        if add_p:
            chart_html.append(p)
        if p.startswith("```") and add_p:
            break

    components.html("\n".join(chart_html), height=400)
