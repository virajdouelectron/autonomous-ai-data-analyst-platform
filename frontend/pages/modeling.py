import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

if "train_response" not in st.session_state:
    st.session_state.train_response = None

if "modeling_error" not in st.session_state:
    st.session_state.modeling_error = None


@st.cache_data
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)


st.title("AutoML Model Training")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
    key="modeling_uploader",
    help="Upload a CSV to preview columns and select the target variable.",
)
dataset_id = st.text_input("Backend Dataset ID", help="Use the dataset ID stored in MongoDB for training.")

df = None
if uploaded_file is not None:
    try:
        df = load_csv(uploaded_file)
        st.success(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
        with st.expander("Dataset preview"):
            st.dataframe(df.head(10), use_container_width=True)

        st.write("### Select target column")
        target_column = st.selectbox("Target column", options=df.columns.tolist())
    except Exception as exc:
        st.error(f"Failed to read uploaded file: {exc}")
        target_column = None
else:
    pass
    target_column = None

if st.button("Train AutoML Model"):
    st.session_state.train_response = None
    st.session_state.modeling_error = None

    if not dataset_id:
        st.error("A backend dataset ID is required to run training.")
    elif not target_column:
        st.error("Select a target column from the uploaded dataset.")
    else:
        with st.spinner("Training models..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/train",
                    json={
                        "dataset_id": dataset_id,
                        "target_column": target_column,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                st.session_state.train_response = response.json()
            except Exception as exc:
                st.session_state.modeling_error = str(exc)

if st.session_state.modeling_error:
    st.error(f"Training failed: {st.session_state.modeling_error}")

if st.session_state.train_response:
    result = st.session_state.train_response
    st.success(f"Training complete: best model is {result.get('best_model')}")

    st.subheader("Best Model Metrics")
    best_metrics = result.get("best_model_metrics", {})
    if best_metrics:
        metrics_df = pd.DataFrame.from_dict(best_metrics, orient="index", columns=["value"]).reset_index()
        metrics_df.columns = ["metric", "value"]
        st.table(metrics_df)
    else:
        st.write("No metrics were returned.")

    feature_importance = result.get("best_model_feature_importance")
    if feature_importance:
        fi_df = pd.DataFrame(
            {
                "feature": list(feature_importance.keys()),
                "importance": list(feature_importance.values()),
            }
        ).sort_values("importance", ascending=False)
        st.subheader("Feature Importance")
        fig = px.bar(fi_df, x="importance", y="feature", orientation="h", title="Best Model Feature Importance")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No feature importance data was available for the selected model.")

    if candidate_models := result.get("candidate_models"):
        st.subheader("Candidate Model Comparison")
        comparison_rows = []
        for model_name, details in candidate_models.items():
            row = {"model": model_name}
            row.update(details.get("metrics", {}))
            comparison_rows.append(row)
        if comparison_rows:
            st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True)

if df is not None and not dataset_id:
    st.warning(
        "You can still upload a CSV to preview the dataset, but training requires a backend dataset ID that points to an existing MongoDB dataset."
    )
