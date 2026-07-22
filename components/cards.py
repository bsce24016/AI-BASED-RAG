import streamlit as st


def info_card(title, value):

    st.metric(
        label=title,
        value=value,
    )