import streamlit as st


def render_header():

    st.markdown(
        """
        <h1 style='text-align:center;
        color:white;
        font-size:42px;'>

        🤖 Enterprise AI Assistant

        </h1>

        <p style='text-align:center;
        color:lightgray;'>

        Production Ready Multi Document RAG Platform

        </p>

        """,
        unsafe_allow_html=True,
    )