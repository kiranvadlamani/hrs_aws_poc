from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
import streamlit as st
import sqlite3
import pandas as pd
import os
import re


load_dotenv()
api_key = os.getenv("API_KEY")

st.title("Nurse Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    if "content" in message:
        st.markdown(message["content"])
    if "data" in message:
        st.dataframe(message["data"])

if prompt := st.chat_input("Message Nurse Chatbot..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    llm = ChatMistralAI(endpoint="http://18.118.106.247:8000/",
                        model="mistralai/Mistral-7B-Instruct-v0.2",
                        temperature=0.1,
                        mistral_api_key=api_key,
                        max_tokens=8000)
    file_path = 'config/prompt'
    with open(file_path, 'r') as file:
        context = file.read()
    question = context.format(input_text=prompt)
    messages = [
        SystemMessage(content="You generate a sql query output based on an input text"),
        HumanMessage(content=question)
    ]
    response = llm.invoke(messages)
    st.markdown(response.content)
    pattern = r"```sql(.*?)```"
    try:
        query = re.findall(pattern, response.content,
                           re.IGNORECASE | re.DOTALL)[0]
    except Exception as e:
        st.error("Unable to capture SQL query from creator output. Please ask the prompt again.")
        st.error("Description: " + str(e))
        st.stop()
    conn = sqlite3.connect('hrs_biometric.db')
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    conn.close()
    st.session_state.messages.append({"data": df, "content": response.content})

    # db = SQLDatabase.from_uri("sqlite:///hrs_biometric.db")
    # db.run("SELECT * FROM Health_Synthetic LIMIT 10;")
    # print(db.dialect)
    # print(db.get_usable_table_names())
    # toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    # agent_executor = create_sql_agent(
    #     llm=llm,
    #     toolkit=toolkit,
    #     verbose=True,
    #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # )
    # agent_executor.run(
    #     prompt
    # )



