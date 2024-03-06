import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")

st.title("Nurse Chatbot")

if prompt := st.chat_input("Message Nurse Chatbot..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    llm = ChatMistralAI(endpoint="http://18.118.106.247:8000/",
                        model="mistralai/Mistral-7B-Instruct-v0.2",
                        mistral_api_key=api_key,
                        max_tokens=8000)
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    st.info(response.content)
