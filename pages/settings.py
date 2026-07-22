import os
import shutil
import streamlit as st

UPLOAD_FOLDER = "uploads"

VECTOR_DB = "vectorstore"


def show():

    st.title("⚙ Settings")

    st.subheader("Model")

    st.text_input(
        "LLM",
        "llama-3.3-70b-versatile",
        disabled=True
    )

    st.text_input(
        "Embeddings",
        "sentence-transformers/all-MiniLM-L6-v2",
        disabled=True
    )

    st.text_input(
        "Vector Database",
        "FAISS",
        disabled=True
    )

    st.divider()

    st.subheader("Maintenance")

    if st.button(
        "🗑 Delete Knowledge Base",
        use_container_width=True
    ):

        if os.path.exists(VECTOR_DB):

            shutil.rmtree(VECTOR_DB)

            st.success(
                "Knowledge Base Deleted"
            )

        else:

            st.warning(
                "Knowledge Base Not Found"
            )

    if st.button(
        "🗑 Delete Uploaded Documents",
        use_container_width=True
    ):

        if os.path.exists(UPLOAD_FOLDER):

            for file in os.listdir(UPLOAD_FOLDER):

                os.remove(
                    os.path.join(
                        UPLOAD_FOLDER,
                        file
                    )
                )

            st.success(
                "Documents Deleted"
            )

        else:

            st.warning(
                "Upload Folder Empty"
            )

    st.divider()

    st.subheader("Application")

    st.info(
        """
Enterprise AI Assistant

Version 1.0

LangChain + Groq + FAISS
"""
    )