"""Fetch a JSON response from a configured timing API endpoint."""
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def fetch_results(client: httpx.AsyncClient, url: str):
    token = os.getenv("TIMING_API_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = await client.get(url, headers=headers, timeout=30.0)
    response.raise_for_status()
    return response.json()

async def main():
    url = os.getenv("TIMING_API_URL")
    if not url:
        raise SystemExit("Set TIMING_API_URL in .env before running ingestion.")
    async with httpx.AsyncClient() as client:
        payload = await fetch_results(client, url)
    count = len(payload) if isinstance(payload, list) else "non-list JSON"
    print(f"Fetched response successfully ({count} records/items).")
    print("Provider-specific mapping and DuckDB persistence are the next steps.")

if __name__ == "__main__":
    asyncio.run(main())
