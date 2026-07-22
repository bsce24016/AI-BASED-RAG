import os
from collections import Counter

import streamlit as st
import matplotlib.pyplot as plt

UPLOAD_FOLDER = "uploads"


def show():

    st.title("📊 Analytics Dashboard")

    st.caption("Monitor your Enterprise AI Assistant")

    files = []

    if os.path.exists(UPLOAD_FOLDER):
        files = os.listdir(UPLOAD_FOLDER)

    total_docs = len(files)

    total_messages = len(
        st.session_state.get("messages", [])
    )

    kb_ready = os.path.exists(
        "vectorstore/faiss_index"
    )

    # ==========================
    # Metrics
    # ==========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📄 Documents",
        total_docs
    )

    col2.metric(
        "💬 Messages",
        total_messages
    )

    col3.metric(
        "🧠 Knowledge Base",
        "Ready" if kb_ready else "Missing"
    )

    st.divider()

    # ==========================
    # Document Type Statistics
    # ==========================

    extensions = []

    for file in files:

        ext = os.path.splitext(file)[1].lower()

        if ext == "":
            ext = "Unknown"

        extensions.append(ext)

    counts = Counter(extensions)

    if counts:

        st.subheader("📁 Document Types")

        fig, ax = plt.subplots(figsize=(6,4))

        ax.bar(
            counts.keys(),
            counts.values()
        )

        ax.set_xlabel("File Type")

        ax.set_ylabel("Count")

        st.pyplot(fig)

        st.subheader("🥧 File Distribution")

        fig2, ax2 = plt.subplots(figsize=(5,5))

        ax2.pie(
            counts.values(),
            labels=counts.keys(),
            autopct="%1.1f%%"
        )

        ax2.axis("equal")

        st.pyplot(fig2)

    else:

        st.info("No uploaded documents.")

    st.divider()

    # ==========================
    # Recent Files
    # ==========================

    st.subheader("📄 Uploaded Documents")

    if files:

        for file in sorted(files):

            size = os.path.getsize(
                os.path.join(
                    UPLOAD_FOLDER,
                    file
                )
            ) / 1024

            st.write(
                f"📄 {file}  ({size:.2f} KB)"
            )

    else:

        st.info("Upload documents first.")

    st.divider()

    # ==========================
    # Storage Usage
    # ==========================

    total_size = 0

    for file in files:

        total_size += os.path.getsize(
            os.path.join(
                UPLOAD_FOLDER,
                file
            )
        )

    st.subheader("💾 Storage")

    st.metric(
        "Total Size",
        f"{total_size/1024:.2f} KB"
    )

    st.divider()

    # ==========================
    # System Information
    # ==========================

    st.subheader("⚙ System Information")

    st.success(
        "LLM : llama-3.3-70b-versatile"
    )

    st.success(
        "Embeddings : all-MiniLM-L6-v2"
    )

    st.success(
        "Vector Database : FAISS"
    )

    st.success(
        "Framework : LangChain"
    )

    st.success(
        "Frontend : Streamlit"
    )

    st.success(
        "Memory : Enabled"
    )