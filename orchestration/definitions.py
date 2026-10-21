"""Initial Dagster definitions; replace placeholder with pipeline assets."""
from dagster import Definitions, asset

@asset
def ingestion_setup_check() -> str:
    """Make the source configuration requirement visible in Dagster."""
    return "Configure TIMING_API_URL and implement validated DuckDB persistence."

defs = Definitions(assets=[ingestion_setup_check])
