from streamlit_option_menu import option_menu


def render_sidebar():
    with __import__("streamlit").sidebar:
        selected = option_menu(
            menu_title="Enterprise AI",
            options=[
                "Dashboard",
                "Chat",
                "Analytics",
                "Settings",
            ],
            icons=[
                "speedometer2",
                "chat-dots",
                "bar-chart",
                "gear",
            ],
            menu_icon="robot",
            default_index=0,
        )

    return selected