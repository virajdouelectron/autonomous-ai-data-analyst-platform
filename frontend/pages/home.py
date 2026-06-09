import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.title("Autonomous AI Data Analyst Platform")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is not None:
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv"
            )
        }
        response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state["dataset"] = data
            st.success(f"Loaded {data['rows']} rows")
        else:
            st.error(f"Upload failed: {response.text}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
