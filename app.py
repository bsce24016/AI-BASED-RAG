import streamlit as st

from config.settings import initialize_settings
from config.logging_config import logger

from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer

from pages import dashboard
from pages import chat
from pages import analytics
from pages import settings


st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_settings()

logger.info("Application started.")

render_header()

selected = render_sidebar()

if selected == "Dashboard":
    dashboard.show()

elif selected == "Chat":
    chat.show()

elif selected == "Analytics":
    analytics.show()

elif selected == "Settings":
    settings.show()

render_footer()