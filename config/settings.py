import streamlit as st

from config.constants import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_K,
)


def initialize_settings():
    defaults = {
        "model": DEFAULT_MODEL,
        "temperature": DEFAULT_TEMPERATURE,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
        "top_k": DEFAULT_TOP_K,
        "chat_history": [],
        "documents": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value