import os
import requests

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Autonomous AI Data Analyst Platform",
    page_icon="📊",
    layout="wide",
)

st.title("Autonomous AI Data Analyst Platform")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select a page",
        ["Home", "Insights", "Query", "Modeling"],
        index=0,
    )
    st.markdown("---")

PAGE_MODULES = {
    "Home": "frontend.pages.home",
    "Insights": "frontend.pages.insights",
    "Query": "frontend.pages.query",
    "Modeling": "frontend.pages.modeling",
}

module_name = PAGE_MODULES.get(page)
try:
    __import__(module_name)
except Exception as exc:
    st.error(f"Unable to load page '{page}': {exc}")
