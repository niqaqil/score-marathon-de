"""Streamlit dashboard backed by Google BigQuery."""
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from google.api_core.exceptions import GoogleAPIError
from google.cloud import bigquery

st.set_page_config(page_title="Score Marathon Analytics", page_icon="🏃", layout="wide")
st.title("🏃 Score Marathon Analytics")
st.caption("Race results pipeline · BigQuery + dbt + Dagster")

project_id = os.getenv("GCP_PROJECT_ID")
dataset_id = os.getenv("BQ_DATASET", "marathon")
location = os.getenv("BQ_LOCATION", "US")

if not project_id:
    st.info("Set GCP_PROJECT_ID and BQ_DATASET, then authenticate with Google Cloud Application Default Credentials.")
    st.code("gcloud auth application-default login\nstreamlit run dashboard/app.py", language="bash")
    st.stop()

client = bigquery.Client(project=project_id, location=location)
table_candidates = [
    f"{project_id}.{dataset_id}.mart_race_leaderboard",
    f"{project_id}.{dataset_id}.stg_race_results",
    f"{project_id}.{dataset_id}.raw_results",
]

try:
    existing = {table.table_id for table in client.list_tables(f"{project_id}.{dataset_id}")}
    available = [table_id for table_id in table_candidates if table_id.split(".")[-1] in existing]
    if not available:
        st.info(f"No results tables found in {project_id}.{dataset_id} yet. Configure the timing source and run ingestion/dbt.")
        st.stop()

    selected_table = st.selectbox("Results table", available, format_func=lambda name: name.split(".")[-1])
    # Table names are selected only from the fixed candidates above.
    query = "SELECT * FROM " + chr(96) + selected_table + chr(96) + " LIMIT 10000"
    df = client.query(query).to_dataframe()
    st.metric("Rows loaded", f"{len(df):,}")
    st.dataframe(df, use_container_width=True)

    if {"bib", "finish_seconds"}.issubset(df.columns):
        chart_df = df.dropna(subset=["finish_seconds"]).copy()
        if not chart_df.empty:
            chart_df["finish_minutes"] = pd.to_numeric(chart_df["finish_seconds"], errors="coerce") / 60
            chart_df = chart_df.dropna(subset=["finish_minutes"])
            if not chart_df.empty:
                st.plotly_chart(
                    px.histogram(chart_df, x="finish_minutes", title="Finish-time distribution (minutes)"),
                    use_container_width=True,
                )
except (GoogleAPIError, ValueError) as exc:
    st.error(f"Could not query BigQuery. Check project/dataset settings, IAM permissions, and billing/API configuration. Details: {exc}")
