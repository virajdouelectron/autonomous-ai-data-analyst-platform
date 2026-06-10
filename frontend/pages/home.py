import os
import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.title("Autonomous AI Data Analyst Platform")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
    key="home_csv_uploader",
    help="Upload a CSV file for analysis.",
)

if uploaded_file is not None:
    try:
        with st.spinner("Uploading CSV..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv",
                )
            }
            response = requests.post(
                f"{BACKEND_URL}/upload",
                files=files,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            st.session_state["home_dataset"] = data

        st.success(f"Loaded {data['rows']} rows and {data['columns']} columns.")
        st.write("### Columns")
        st.write(data["column_names"])

        if data.get("data"):
            try:
                df = pd.DataFrame(data["data"])
                st.write("### Sample data")
                st.dataframe(df.head(10), use_container_width=True)
            except Exception:
                pass
    except requests.exceptions.RequestException as exc:
        error_message = None
        if exc.response is not None:
            try:
                error_message = exc.response.json()
            except Exception:
                error_message = exc.response.text
        else:
            error_message = str(exc)
        st.error(f"Upload failed: {error_message}")
    except Exception as exc:
        st.error(f"Error uploading file: {exc}")
