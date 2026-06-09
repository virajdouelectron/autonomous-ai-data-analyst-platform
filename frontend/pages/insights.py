import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("AI Insights")

insight_prompt = st.text_area("Insight prompt", "Provide a brief description of the dataset and ask the backend for key insights.")

if st.button("Generate insights"):
    with st.spinner("Calling backend insights API..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/insights",
                json={"statistics": {"prompt": insight_prompt}},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            st.success("Insights generated successfully")
            st.write(data)
        except Exception as exc:
            st.error(f"Insights request failed: {exc}")
