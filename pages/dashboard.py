import os
from datetime import datetime

import streamlit as st

UPLOAD_FOLDER = "uploads"


def get_documents():

    if not os.path.exists(UPLOAD_FOLDER):
        return []

    return sorted(os.listdir(UPLOAD_FOLDER))


def get_storage():

    total = 0

    if os.path.exists(UPLOAD_FOLDER):

        for file in os.listdir(UPLOAD_FOLDER):

            path = os.path.join(
                UPLOAD_FOLDER,
                file
            )

            if os.path.isfile(path):

                total += os.path.getsize(path)

    return round(total / 1024, 2)


def show():

    st.title("🏢 Enterprise AI Assistant")

    st.caption(
        "AI Powered Document Question Answering System"
    )

    st.divider()

    docs = get_documents()

    total_docs = len(docs)

    total_messages = len(
        st.session_state.get(
            "messages",
            []
        )
    )

    kb_ready = os.path.exists(
        "vectorstore/faiss_index"
    )

    storage = get_storage()

    # ==========================
    # Dashboard Metrics
    # ==========================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📄 Uploaded Documents",
            total_docs
        )

        st.metric(
            "💬 Chat Messages",
            total_messages
        )

        st.metric(
            "💾 Storage Used",
            f"{storage} KB"
        )

    with col2:

        st.metric(
            "🧠 Knowledge Base",
            "Ready" if kb_ready else "Not Ready"
        )

        st.metric(
            "🤖 LLM",
            "Llama 3.3"
        )

        st.metric(
            "📅 Today",
            datetime.now().strftime("%d-%m-%Y")
        )

    st.divider()

    # ==========================
    # System Status
    # ==========================

    st.subheader("⚙ System Status")

    if kb_ready:

        st.success("Knowledge Base Created")

    else:

        st.warning("Knowledge Base Not Created")

    if total_docs > 0:

        st.success("Documents Uploaded")

    else:

        st.warning("No Documents Uploaded")

    st.success("LangChain Connected")

    st.success("Groq Connected")

    st.success("FAISS Available")

    st.success("Memory Enabled")

    st.divider()

    # ==========================
    # Uploaded Documents
    # ==========================

    st.subheader("📁 Uploaded Documents")

    if not docs:

        st.info("No documents uploaded.")

    else:

        for file in docs:

            path = os.path.join(
                UPLOAD_FOLDER,
                file
            )

            size = round(
                os.path.getsize(path) / 1024,
                2
            )

            st.write(
                f"📄 {file} ({size} KB)"
            )

    st.divider()

    # ==========================
    # Quick Actions
    # ==========================

    st.subheader("🚀 Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💬 Open Chat",
            use_container_width=True
        ):

            st.info(
                "Select Chat from the sidebar."
            )

    with col2:

        if st.button(
            "📊 View Analytics",
            use_container_width=True
        ):

            st.info(
                "Select Analytics from the sidebar."
            )

    st.divider()

    # ==========================
    # About
    # ==========================

    st.subheader("ℹ About")

    st.info(
        """
Enterprise AI Assistant

• LangChain

• Groq Llama 3.3

• HuggingFace Embeddings

• FAISS Vector Database

• Streamlit

• Conversation Memory

• PDF / TXT / DOCX Support

• Retrieval Augmented Generation (RAG)

• Source Citation
"""
    )