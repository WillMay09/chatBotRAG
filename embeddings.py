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
    
    
    top_matches = pinecone_index.query(vector=raw_query_embedding.tolist(), top_k=5, include_metadata=True, namespace="https://github.com/CoderAgent/SecureAgent")

    # Get the list of retrieved texts
    contexts = [item['metadata']['text'] for item in top_matches['matches']]

    augmented_query = "<CONTEXT>\n" + "\n\n-------\n\n".join(contexts[ : 10]) + "\n-------\n</CONTEXT>\n\n\n\nMY QUESTION:\n" + query

    

    return augmented_query

#used to embed the text
def get_huggingface_embeddings(text, model_name="sentence-transformers/all-mpnet-base-v2"):
    model = SentenceTransformer(model_name)#pretrained model
    return model.encode(text)
