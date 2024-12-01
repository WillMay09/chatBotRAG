import streamlit as st
import numpy as np

with st.chat_message("user"):
    st.write("Hello")
    st.bar_chart(np.random.randn(30, 3))
#session state stores history of current chat session

# prompt = st.chat_input("Ask anything, I am listening?")
# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")


############################################
st.title("Echo Bot")

#initialize the chat history
if "messages" not in st.session_state:#if there are no messages in the session state
    st.session_state.messages = []#initialize empty list

#Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#if the user provides input
if prompt := st.chat_input("what is up"):
#display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        #add user message to chat history
    st.session_state.messages.append({"role":"user", "content": prompt})
###Chatbot's response
response = f"Echo: {prompt}"
with st.chat_message("assistant"):
    st.markdown(response)
st.session_state.messages.append({"role": "assistant","content": response})