"""Fetch, validate, optionally archive, and load timing results into BigQuery."""
import asyncio
import json
import os
from datetime import datetime, timezone

import httpx
from dotenv import load_dotenv

from ingestion.schema import RaceResult
from ingestion.bigquery_writer import load_results_to_bigquery

load_dotenv()


async def fetch_results(client: httpx.AsyncClient, url: str):
    token = os.getenv("TIMING_API_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = await client.get(url, headers=headers, timeout=30.0)
    response.raise_for_status()
    return response.json()


def extract_records(payload):
    """Accept a JSON list or a top-level object with a 'results' list.

    Provider-specific field mapping may still be required once the source API is known.
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return payload["results"]
    raise ValueError("Expected a JSON list or an object containing a 'results' list.")


def archive_raw_payload(payload):
    """Optionally archive the fetched response to GCS when GCS_RAW_BUCKET is set."""
    bucket_name = os.getenv("GCS_RAW_BUCKET")
    if not bucket_name:
        return None

    from google.cloud import storage

    project_id = os.getenv("GCP_PROJECT_ID")
    client = storage.Client(project=project_id or None)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    blob_name = f"timing-api/results_{timestamp}.json"
    blob = client.bucket(bucket_name).blob(blob_name)
    blob.upload_from_string(
        json.dumps(payload, ensure_ascii=False),
        content_type="application/json",
    )
    return f"gs://{bucket_name}/{blob_name}"


async def main():
    url = os.getenv("TIMING_API_URL")
    if not url:
        raise SystemExit("Set TIMING_API_URL before running ingestion.")
    if not os.getenv("GCP_PROJECT_ID"):
        raise SystemExit("Set GCP_PROJECT_ID before running ingestion.")

    async with httpx.AsyncClient() as client:
        payload = await fetch_results(client, url)

    archive_uri = archive_raw_payload(payload)
    records = extract_records(payload)
    validated = [RaceResult.model_validate(record) for record in records]
    if not validated:
        print("No result records returned; nothing to load.")
        return

    table_id = load_results_to_bigquery(validated)
    print(f"Loaded {len(validated)} validated records into {table_id}.")
    if archive_uri:
        print(f"Archived raw response to {archive_uri}.")


if __name__ == "__main__":
    asyncio.run(main())
