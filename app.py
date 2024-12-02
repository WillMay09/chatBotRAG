import streamlit as st
from openai import OpenAI 
from groq import Client
from embeddings import retrieve_context
st.title("ChatGPT-Clone RAG Implementation")

client = Client(api_key=st.secrets["GROQ_API_KEY"])
models = [
    "llama-3.1-70b-versatile",
    "llama-3.2-90b-vision-preview",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",



]
#create dropdown menu in the sidbar for selecting the model
selected_model = st.sidebar.selectbox("Selecte a model", models)

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = selected_model
else:
    st.session_state["groq_model"] = selected_model


#intialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []#empty list
#Display chat message from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown("Welcome to my Context Retrieval App")
st.write("""Please enter your query below. This app specializes in retreiving
information on codebases.  If your question is code related, our RAG retrevial system to give you the most optimal answer based on the code base https://github.com/CoderAgent/SecureAgent""")
st.write(f"Current model selected: {st.session_state['groq_model']}")

prompt = st.chat_input("Ask me anything") 
if prompt:
      # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder=st.empty()
        assistant_response = ""
        augmented_query = retrieve_context(prompt)
        # Define the system prompt
        system_prompt = """You are a Senior Software Engineer.  An expert in all things code related

        Answer any questions I have about the codebase, based on the code provided. Always consider all of the context provided when forming a response.
        """
        messages = [{"role": "system", "content": system_prompt},
        {"role": "user", "content": augmented_query},]
        messages.extend({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)

        #parse in chunks
        for response in client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=messages,
             stream=True,  # Ensure streaming is set to True for chunks
        ):
            
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].delta.content
                if content: 
                    assistant_response += content
                    message_placeholder.markdown(assistant_response+ " ")
            #message_placeholder.markdown(assistant_response)
        
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})



