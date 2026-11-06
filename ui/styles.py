import streamlit as st

CSS = """
<style>
    #MainMenu, footer {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1300px;
    }

    [data-testid="stSidebar"] {
        background-color: #0A1222;
        border-right: 1px solid #1E2D4A;
    }

    [data-testid="stMetric"] {
        background-color: #111D35;
        border: 1px solid #1E2D4A;
        border-radius: 12px;
        padding: 16px 20px;
    }

    [data-testid="stMetricLabel"] {
        color: #8FA3C4;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)