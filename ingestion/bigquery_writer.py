"""Write validated race results to a managed BigQuery table."""
import json
import os
from datetime import datetime, timezone

from google.api_core.exceptions import NotFound
from google.cloud import bigquery

from ingestion.schema import RaceResult


def load_results_to_bigquery(results: list[RaceResult]) -> str:
    """Create the destination dataset/table if needed and append validated rows.

    BigQuery insert IDs provide best-effort duplicate suppression for retries;
    they are not a substitute for a future MERGE-based idempotent upsert.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_name = os.getenv("BQ_DATASET", "marathon")
    location = os.getenv("BQ_LOCATION", "US")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be configured.")

    client = bigquery.Client(project=project_id, location=location)
    dataset_id = f"{project_id}.{dataset_name}"
    try:
        client.get_dataset(dataset_id)
    except NotFound:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = location
        client.create_dataset(dataset, exists_ok=True)

    table_id = f"{dataset_id}.raw_results"
    schema = [
        bigquery.SchemaField("race_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("bib", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("finish_seconds", "INT64", mode="NULLABLE"),
        bigquery.SchemaField("category", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("splits_json", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
    ]
    try:
        client.get_table(table_id)
    except NotFound:
        table = bigquery.Table(table_id, schema=schema)
        client.create_table(table, exists_ok=True)

    ingested_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    rows = [
        {
            "race_id": result.race_id,
            "bib": result.bib,
            "status": result.status,
            "finish_seconds": result.finish_seconds,
            "category": result.category,
            "splits_json": json.dumps(
                [split.model_dump(mode="json") for split in result.splits],
                ensure_ascii=False,
            ),
            "ingested_at": ingested_at,
        }
        for result in results
    ]
    row_ids = [f"{row['race_id']}:{row['bib']}:{ingested_at}" for row in rows]
    errors = client.insert_rows_json(table_id, rows, row_ids=row_ids)
    if errors:
        raise RuntimeError(f"BigQuery rejected one or more rows: {errors}")
    return table_id
