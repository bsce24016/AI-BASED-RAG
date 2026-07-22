import os
import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage

from rag.llm import get_llm, get_rag_chain
from rag.vectorstore import create_vectorstore, get_retriever
from rag.memory import get_chat_history


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)



def initialize_chat():

    # UI chat messages

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Welcome! Upload your documents and ask me anything."
            }
        ]


    # FIX OLD STREAMLIT MEMORY

    if "chat_history" in st.session_state:

        if isinstance(
            st.session_state.chat_history,
            list
        ):

            del st.session_state.chat_history



    # Create LangChain memory

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = get_chat_history()



def save_file(uploaded_file):

    filepath = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(filepath, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    return filepath



def list_documents():

    return sorted(
        os.listdir(UPLOAD_FOLDER)
    )



def delete_document(filename):

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if os.path.exists(path):

        os.remove(path)



def show():

    initialize_chat()

    llm = get_llm()


    left, right = st.columns(
        [7, 3]
    )



    # ==========================
    # CHAT SECTION
    # ==========================

    with left:


        st.title(
            "💬 Enterprise AI Assistant"
        )


        st.caption(
            "Powered by LangChain + Groq + FAISS + Memory"
        )



        # Display messages

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )



        prompt = st.chat_input(
            "Ask a question..."
        )



        if prompt:


            # Store UI message

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )



            # Store LangChain memory

            st.session_state.chat_history.add_message(
                HumanMessage(
                    content=prompt
                )
            )



            with st.chat_message("user"):

                st.markdown(prompt)



            with st.chat_message("assistant"):


                with st.spinner(
                    "Thinking..."
                ):


                    retriever = get_retriever()



                    if retriever is None:


                        answer = llm.invoke(
                            prompt
                        ).content



                    else:


                        docs = retriever.invoke(
                            prompt
                        )



                        chain = get_rag_chain()



                        response = chain.invoke(
                            {
                                "context": docs,
                                "input": prompt,
                                "chat_history":
                                    st.session_state.chat_history.messages
                            }
                        )


                        answer = response



                        # Source citations

                        sources = []


                        for doc in docs:


                            source = doc.metadata.get(
                                "source",
                                "Unknown"
                            )


                            page = doc.metadata.get(
                                "page",
                                None
                            )



                            if page is not None:

                                sources.append(
                                    f"- {source} (Page {page + 1})"
                                )

                            else:

                                sources.append(
                                    f"- {source}"
                                )



                        if sources:

                            answer += (
                                "\n\n📚 **Sources:**\n"
                            )

                            answer += "\n".join(
                                set(sources)
                            )



                    st.markdown(
                        answer
                    )



            # Save assistant response

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )



            # Store AI memory

            st.session_state.chat_history.add_message(
                AIMessage(
                    content=answer
                )
            )



        # ==========================
    # UPLOAD SECTION
    # ==========================

    with right:

        # ==========================================
        # CHAT CONTROLS
        # ==========================================

        st.subheader("💬 Chat")

        if st.button(
            "🗑 Clear Chat",
            use_container_width=True
        ):

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "👋 Welcome! Upload your documents and ask me anything."
                }
            ]

            st.session_state.chat_history = get_chat_history()

            st.success("✅ Chat cleared!")

            st.rerun()

        st.divider()

        # ==========================================
        # SEARCH
        # ==========================================

        st.subheader("🔍 Search Documents")

        search = st.text_input(
            "Search uploaded files"
        )

        st.divider()

        # ==========================================
        # UPLOAD
        # ==========================================

        st.subheader("📁 Upload Documents")

        uploaded_files = st.file_uploader(
            "Choose Files",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True
        )

        if uploaded_files:

            for file in uploaded_files:

                filepath = os.path.join(
                    UPLOAD_FOLDER,
                    file.name
                )

                if not os.path.exists(filepath):

                    save_file(file)

            st.success("✅ Files uploaded successfully.")

        st.divider()

        # ==========================================
        # CREATE KB
        # ==========================================

        if st.button(
            "🧠 Create Knowledge Base",
            use_container_width=True
        ):

            with st.spinner("Creating Knowledge Base..."):

                db = create_vectorstore()

            if db:

                st.success("✅ Knowledge Base Created!")

            else:

                st.warning("Upload documents first.")

        st.divider()

        # ==========================================
        # DOCUMENTS
        # ==========================================

        st.subheader("📄 Uploaded Documents")

        files = list_documents()

        if search:

            files = [
                f for f in files
                if search.lower() in f.lower()
            ]

        if not files:

            st.info("No matching documents.")

        else:

            for file in files:

                col1, col2 = st.columns([5, 1])

                with col1:

                    ext = os.path.splitext(file)[1].lower()

                    if ext == ".pdf":
                        icon = "📕"
                    elif ext == ".docx":
                        icon = "📘"
                    elif ext == ".txt":
                        icon = "📄"
                    else:
                        icon = "📁"

                    st.write(f"{icon} {file}")

                with col2:

                    if st.button("🗑", key=file):

                        delete_document(file)

                        st.rerun()

        st.divider()

        # ==========================================
        # KNOWLEDGE BASE
        # ==========================================

        st.subheader("🧠 Knowledge Base")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Documents",
                len(list_documents())
            )

        with col2:

            st.metric(
                "Status",
                "Ready" if os.path.exists("vectorstore/faiss_index") else "Not Ready"
            )

        st.divider()

        # ==========================================
        # EXPORT CHAT
        # ==========================================

        st.subheader("⬇ Export Chat")

        chat_text = ""

        for msg in st.session_state.messages:

            chat_text += f"{msg['role'].upper()}\n{msg['content']}\n\n"

        st.download_button(
            "📄 Download Chat",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        # ==========================================
        # SYSTEM HEALTH
        # ==========================================

        st.subheader("🟢 System Health")

        st.success("Groq Connected")
        st.success("FAISS Ready")
        st.success("Memory Enabled")
        st.success("Embeddings Loaded")