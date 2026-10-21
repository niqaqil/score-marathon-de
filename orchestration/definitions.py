"""Dagster starter asset for the Google Cloud pipeline.

This intentionally remains a setup check until the timing provider schema and
deployment identity are configured. The Cloud Run Job can be scheduled directly
with Cloud Scheduler or invoked from a future Dagster asset/job.
"""
import os
from dagster import Definitions, asset


@asset
def ingestion_setup_check() -> str:
    """Validate required configuration without making cloud calls."""
    missing = [
        name
        for name in ("GCP_PROJECT_ID", "BQ_DATASET", "TIMING_API_URL")
        if not os.getenv(name)
    ]
    if missing:
        return "Missing configuration: " + ", ".join(missing)
    return (
        f"BigQuery target configured: {os.environ['GCP_PROJECT_ID']}."
        f"{os.environ['BQ_DATASET']}. Confirm source schema before running ingestion."
    )


defs = Definitions(assets=[ingestion_setup_check])
