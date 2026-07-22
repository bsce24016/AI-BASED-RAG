import os
import streamlit as st

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from rag.loader import load_documents


DB_PATH = "vectorstore/faiss_index"


@st.cache_resource
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vectorstore():

    documents = load_documents()

    if len(documents) == 0:
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    db = FAISS.from_documents(
        chunks,
        get_embeddings()
    )

    os.makedirs("vectorstore", exist_ok=True)

    db.save_local(DB_PATH)

    return db


@st.cache_resource
def load_vectorstore():

    if not os.path.exists(DB_PATH):
        return None

    return FAISS.load_local(
        DB_PATH,
        get_embeddings(),
        allow_dangerous_deserialization=True
    )


def get_retriever():

    db = load_vectorstore()

    if db is None:
        return None

    return db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 4,
        
    }
)