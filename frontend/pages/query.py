import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "query_result" not in st.session_state:
    st.session_state.query_result = None

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None


@st.cache_data
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)


def build_schema(df: pd.DataFrame) -> dict:
    return df.dtypes.astype(str).to_dict()


def is_safe_query_code(code: str) -> bool:
    blocked_tokens = ["import ", "open(", "os.", "sys.", "subprocess", "__import__", "eval(", "exec(", "requests", "socket", "shlex", "pathlib"]
    normalized = code.replace("\n", " ").lower()
    return not any(token in normalized for token in blocked_tokens)


def execute_pandas_code(code: str, df: pd.DataFrame):
    if not is_safe_query_code(code):
        return None, "The generated code was blocked for safety and was not executed."

    local_vars = {}
    safe_globals = {
        "df": df,
        "pd": pd,
        "__builtins__": {
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "float": float,
            "int": int,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "range": range,
            "enumerate": enumerate,
            "sorted": sorted,
        },
    }

    try:
        exec(code, safe_globals, local_vars)
    except Exception as exc:
        return None, f"Execution error: {exc}"

    output = local_vars.get("result")
    if output is None and "df" in local_vars:
        output = local_vars.get("df")

    if output is None:
        return None, "The code executed successfully but did not assign a `result` value."

    return output, None


def render_result(output):
    if isinstance(output, pd.DataFrame):
        st.subheader("Query result")
        st.dataframe(output, use_container_width=True)

        numeric_cols = output.select_dtypes(include=["number"]).columns.tolist()
        if numeric_cols:
            fig = px.histogram(output, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}")
            st.plotly_chart(fig, use_container_width=True)
        return

    if isinstance(output, pd.Series):
        st.subheader("Query result")
        st.dataframe(output.to_frame(), use_container_width=True)
        if pd.api.types.is_numeric_dtype(output.dtype):
            fig = px.histogram(output.reset_index(), x=output.name or "value", title="Series distribution")
            st.plotly_chart(fig, use_container_width=True)
        return

    if isinstance(output, dict):
        st.subheader("Query result")
        st.json(output)
        return

    st.subheader("Query result")
    st.write(output)


st.title("Natural Language Data Query")
st.markdown(
    "Ask questions about your uploaded dataset in plain English, and receive generated pandas code plus a rendered result table or chart."
)

with st.sidebar:
    st.header("Data query workflow")
    st.write("1. Upload a CSV dataset")
    st.write("2. Ask a question using the chat input")
    st.write("3. View the generated pandas code and result")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], help="Select a local CSV dataset for natural language querying.")

if uploaded_file is not None:
    try:
        st.session_state.uploaded_df = load_csv(uploaded_file)
        st.success(f"Loaded dataset with {st.session_state.uploaded_df.shape[0]} rows and {st.session_state.uploaded_df.shape[1]} columns.")
    except Exception as exc:
        st.error(f"Unable to load CSV file: {exc}")

if st.session_state.uploaded_df is not None:
    df = st.session_state.uploaded_df

    with st.expander("Dataset preview"):
        st.dataframe(df.head(10), use_container_width=True)

    if prompt := st.chat_input("Ask a question about this dataset"):
        st.session_state.chat_history.append({"role": "user", "message": prompt})

        try:
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"question": prompt, "schema": build_schema(df)},
                timeout=60,
            )
            response.raise_for_status()
            payload = response.json()
            generated_code = payload.get("pandas_code", "")
            st.session_state.chat_history.append({"role": "assistant", "message": generated_code})

            output, error = execute_pandas_code(generated_code, df)
            if error:
                st.error(error)
                st.session_state.query_result = None
            else:
                st.session_state.query_result = output

        except Exception as exc:
            st.error(f"Query failed: {exc}")
            st.session_state.query_result = None

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["message"])
        else:
            st.chat_message("assistant").code(message["message"], language="python")

    if st.session_state.query_result is not None:
        render_result(st.session_state.query_result)
else:
    st.info("Upload a CSV file to begin asking questions using the chat interface.")
