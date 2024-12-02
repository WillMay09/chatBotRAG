import pinecone
from sentence_transformers import SentenceTransformer
# from langchain.vectorstores import Pinecone
# from langchain.embeddings import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
import os
import streamlit as st
import torch

pinecone_api_key = st.secrets["PINECONE_API_KEY"]


# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# Connect to your Pinecone index
pinecone_index = pc.Index("codebase-rag")

def retrieve_context(query):
    raw_query_embedding = get_huggingface_embeddings(query)
    
    print(torch.cuda.is_available())
    print(torch.cuda.get_device_name(0))
    print("commands:")
    top_matches = pinecone_index.query(vector=raw_query_embedding.tolist(), top_k=5, include_metadata=True, namespace="https://github.com/CoderAgent/SecureAgent")

    # Get the list of retrieved texts
    contexts = [item['metadata']['text'] for item in top_matches['matches']]

    augmented_query = "<CONTEXT>\n" + "\n\n-------\n\n".join(contexts[ : 10]) + "\n-------\n</CONTEXT>\n\n\n\nMY QUESTION:\n" + query

    # Modify the prompt below as need to improve the response quality
    system_prompt = f"""You are a Senior Software Engineer, specializing in TypeScript.

    Answer any questions I have about the codebase, based on the code provided. Always consider all of the context provided when forming a response.
    """

    # llm_response = client.chat.completions.create(
    #     model="llama-3.1-8b-instant",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": augmented_query}
    #     ]
    # )

    return augmented_query

def get_huggingface_embeddings(text, model_name="sentence-transformers/all-mpnet-base-v2"):
    model = SentenceTransformer(model_name)#pretrained model
    return model.encode(text)
