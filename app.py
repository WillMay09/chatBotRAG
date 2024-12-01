import streamlit as st
from openai import OpenAI 
from groq import Client
st.title("ChatGPT-like clone")

client = Client(api_key=st.secrets["GROQ_API_KEY"])

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.1-70b-versatile"

#intialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []#empty list
#Display chat message from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Accept user input
if prompt := st.chat_input("Ask me anything"):
      # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare assistant response
    

   # Send the request to the API
    with st.chat_message("assistant"):
        message_placeholder=st.empty()
        assistant_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
             stream=True,  # Ensure streaming is set to True for chunks
        ):
            print(f"Chunk: {response}")  # Debug: Print each chunk
            print(f"Chunk type: {type(response)}")  # Debug: Print the type of each chunk
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].delta.content
                if content: 
                    assistant_response += content
                    message_placeholder.markdown(assistant_response+ " ")
            message_placeholder.markdown(assistant_response)
        
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
