import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("Autonomous AI Data Analyst Platform")
st.markdown(
    "Upload a CSV dataset to preview the contents, inspect schema information, and get a quick overview of your data."
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], help="Select a local CSV dataset to preview")


@st.cache_data
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)


@st.cache_data
def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)

    return (
        pd.DataFrame(
            {
                "dtype": df.dtypes.astype(str),
                "missing_count": missing_count,
                "missing_pct": missing_pct,
                "unique": df.nunique(),
            }
        )
        .sort_values("missing_count", ascending=False)
        .rename_axis("column")
    )


def create_auto_charts(df: pd.DataFrame, max_categories: int = 25, sample_size: int = 10000, bins: int = 30):
    """Automatically create Plotly charts based on column dtypes.

    - numeric -> histogram
    - categorical/object/bool -> bar (top N values)
    - datetime -> line (counts by date)

    This helper samples large columns for performance and limits category counts.
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    # treat booleans as categorical
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    # also detect datetime-like columns (including string timestamps)
    datetime_candidates = []
    for col in df.columns:
        if col in numeric_cols or col in categorical_cols:
            continue
        try:
            sample = df[col].dropna().head(100)
            if not sample.empty:
                parsed = pd.to_datetime(sample, errors="coerce")
                if parsed.notna().sum() >= max(1, len(sample) // 2):
                    datetime_candidates.append(col)
        except Exception:
            continue

    # Numeric histograms
    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        if len(series) > sample_size:
            series = series.sample(sample_size, random_state=1)
        fig = px.histogram(series, x=col, nbins=bins, title=f"Numeric distribution: {col}")
        st.plotly_chart(fig, use_container_width=True)

    # Categorical bar charts (top N)
    for col in categorical_cols:
        counts = df[col].value_counts(dropna=False)
        if counts.empty:
            continue
        counts = counts.head(max_categories).reset_index()
        counts.columns = [col, "count"]
        fig = px.bar(counts, x=col, y="count", title=f"Value counts: {col}")
        st.plotly_chart(fig, use_container_width=True)

    # Datetime line charts (counts by date)
    for col in datetime_candidates:
        series = pd.to_datetime(df[col], errors="coerce").dropna()
        if series.empty:
            st.write(f"No valid datetime values found for column `{col}`.")
            continue
        # aggregate by date
        dates = series.dt.date.value_counts().sort_index().reset_index()
        dates.columns = ["date", "count"]
        fig = px.line(dates, x="date", y="count", title=f"Datetime distribution: {col}")
        st.plotly_chart(fig, use_container_width=True)


if uploaded_file is not None:
    try:
        df = load_csv(uploaded_file)
        st.success(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

        st.header("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        with st.expander("Dataset details"):
            st.write("### Column summary")
            st.dataframe(
                pd.DataFrame(
                    {
                        "dtype": df.dtypes.astype(str),
                        "non-null": df.notna().sum(),
                        "unique": df.nunique(),
                    }
                )
                .transpose()
                .rename(columns={0: "value"}),
                use_container_width=True,
            )

            st.write("### Missing value analysis")
            st.dataframe(missing_value_summary(df), use_container_width=True)

            st.write("### Sample statistics")
            st.dataframe(df.describe(include="all"), use_container_width=True)

        if st.button("Generate business insights"):
            with st.spinner("Generating insights from Gemini..."):
                try:
                    statistics_payload = {
                        "row_count": df.shape[0],
                        "column_count": df.shape[1],
                        "missing_values": missing_value_summary(df)["missing_count"].to_dict(),
                        "missing_percent": missing_value_summary(df)["missing_pct"].to_dict(),
                        "column_types": df.dtypes.astype(str).to_dict(),
                    }
                    response = requests.post(
                        f"{BACKEND_URL}/api/insights",
                        json={"statistics": statistics_payload},
                        timeout=30,
                    )
                    response.raise_for_status()
                    insights_data = response.json()
                    st.subheader("Business insights")
                    st.write(insights_data.get("insights", "No insights returned."))
                except Exception as exc:
                    st.error(f"Insight generation failed: {exc}")

        if st.button("Upload CSV to backend"):
            with st.spinner("Uploading dataset to backend..."):
                try:
                    csv_bytes = uploaded_file.getvalue()
                    files = {
                        "file": (
                            uploaded_file.name,
                            csv_bytes,
                            uploaded_file.type or "text/csv",
                        )
                    }
                    resp = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=60)
                    if resp.status_code == 403:
                        st.error(
                            "Upload was blocked with a 403 response. The file should be sent directly to the FastAPI backend, "
                            "so check that BACKEND_URL points to the backend service and that the upload route is reachable."
                        )
                        st.stop()
                    resp.raise_for_status()
                    st.success(f"Upload successful: {resp.json()}")
                except requests.HTTPError as exc:
                    status_code = exc.response.status_code if exc.response is not None else None
                    if status_code == 403:
                        st.error(
                            "Upload failed with 403 Forbidden. The backend should accept multipart uploads directly; "
                            "verify the deployed BACKEND_URL and Spaces networking configuration."
                        )
                    else:
                        st.error(f"Upload failed with HTTP error: {exc}")
                except requests.RequestException as exc:
                    st.error(f"Upload failed: {exc}")
                except Exception as exc:
                    st.error(f"Upload failed: {exc}")

        with st.expander("Column types"):
            st.write(df.dtypes.astype(str))

        with st.expander("Automatic charts"):
            # Use a helper to build appropriate charts for each column type
            if df.empty or df.shape[1] == 0:
                st.info("No data available for chart generation.")
            else:
                create_auto_charts(df)

        if st.button("Show full dataset summary"):
            st.write("## Full dataset preview")
            st.dataframe(df, use_container_width=True)

    except Exception as exc:
        st.error(f"Unable to read CSV file: {exc}")
else:
    st.info("Use the uploader above to add a CSV file and preview your dataset.")
