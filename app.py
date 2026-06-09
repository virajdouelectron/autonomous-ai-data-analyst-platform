import importlib
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Autonomous AI Data Analyst Platform",
    page_icon="📊",
    layout="wide",
)

st.title("Autonomous AI Data Analyst Platform")
st.markdown(
    "Use the sidebar to navigate between the Streamlit frontend pages that interact with the backend API."
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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
    page_module = importlib.import_module(module_name)
    importlib.reload(page_module)
except Exception as exc:
    st.error(f"Unable to load page '{page}': {exc}")
