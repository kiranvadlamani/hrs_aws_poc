import streamlit as st
from utils import nurse_report


st.set_page_config(layout="wide")
# title of the streamlit app
st.title(f""":blue[Nurse Chatbot]""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if question := st.chat_input("Ask Nurse Chatbot..."):
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("assistant"):
        # making sure there are no messages present when generating the answer
        message_placeholder = st.empty()
        with st.status("Determining the best possible answer!", expanded=True) as status:
            answer = nurse_report(question)    # Get Answer here: the result text, sql, dataframe used
            message_placeholder.markdown(f"""{answer[0].split('Question:')[0]}""")
            st.markdown(f""":green[SQL query:]""")
            st.code(f"{answer[1]}", language="sql")
            # st.markdown(f""":blue[Dataframe:]""")
            # st.dataframe(df)
            status.update(label="Question Answered...", state="complete", expanded=False)

    # appending the results to the session state
    st.session_state.messages.append({"role": "assistant", "content": answer})
