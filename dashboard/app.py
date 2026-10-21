"""Initial Streamlit dashboard for marathon results."""
import os
from pathlib import Path
import duckdb
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Score Marathon Analytics", page_icon="🏃", layout="wide")
st.title("🏃 Score Marathon Analytics")
st.caption("Race results pipeline · DuckDB + dbt + Dagster")
db_path = Path(os.getenv("DUCKDB_PATH", "data/marathon.duckdb"))
if not db_path.exists():
    st.info("No DuckDB database found yet. Configure ingestion and load race results to activate analytics.")
    st.code("python -m ingestion.scrape_results\nstreamlit run dashboard/app.py", language="bash")
    st.stop()
try:
    with duckdb.connect(str(db_path), read_only=True) as con:
        tables = con.execute("show tables").df()["name"].tolist()
        st.write("Available tables:", ", ".join(tables) if tables else "No tables yet")
        table = next((t for t in ["mart_race_leaderboard", "stg_race_results", "raw_results"] if t in tables), None)
        if table:
            # Table name is selected from a fixed allowlist above.
            df = con.execute(f'SELECT * FROM "{table}" LIMIT 10000').df()
            st.dataframe(df, use_container_width=True)
            if {"bib", "finish_seconds"}.issubset(df.columns):
                chart_df = df.dropna(subset=["finish_seconds"]).copy()
                if not chart_df.empty:
                    chart_df["finish_minutes"] = chart_df["finish_seconds"] / 60
                    st.plotly_chart(px.histogram(chart_df, x="finish_minutes", title="Finish-time distribution (minutes)"), use_container_width=True)
        else:
            st.warning("Database exists, but no recognized results table is available yet.")
except Exception as exc:
    st.error(f"Could not read the DuckDB database: {exc}")
