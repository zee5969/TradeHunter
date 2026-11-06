import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("Settings")
st.caption("Configuration and API connection status")

st.subheader("API keys")
st.write(
    "Keys are read from environment variables or a local `.env` file. "
    "They are never shown on screen or stored in GitHub."
)


def key_status(env_name: str) -> str:
    return "Configured" if os.getenv(env_name) else "Not set"


st.write(f"**Groq API key (`GROQ_API_KEY`):** {key_status('GROQ_API_KEY')}")
st.write("**Search API key:** will be added in Phase 3.")

st.divider()
st.subheader("About")
st.write("TradeHunter AI. Global Importer & Exporter Intelligence.")
st.caption("Prototype build. Free-tier data sources only.")