# Score Marathon DE

An end-to-end data engineering project for marathon race results, inspired by the Boom+ Run dashboard. The project uses Google Cloud for managed storage and analytics, dbt for transformations, Dagster for orchestration, and Streamlit + Plotly for analysis.

> **Status:** Cloud-ready starter scaffold. Live ingestion still requires a confirmed timing API/export schema, and Google Cloud resources must be configured in your project. This change does not create or deploy cloud resources.

## Architecture

~~~text
Timing API / JSON export
        |
        v
Cloud Run Job (Python + Pydantic)
        |                    \
        v                     v
BigQuery raw_results     Cloud Storage (optional raw JSON archive)
        |
        v
dbt-bigquery staging -> analytical marts
        |
        v
Dagster orchestration (deployment/configuration still required)
        |
        v
Streamlit + Plotly on Cloud Run
~~~

## Repository structure

- ingestion/ — async source fetch, Pydantic validation, BigQuery loading, optional raw JSON archive
- dbt_marathon/ — BigQuery profile example, source declarations, staging models, analytical marts
- orchestration/ — Dagster asset scaffold
- dashboard/ — Streamlit and Plotly dashboard querying BigQuery
- tests/ — schema tests
- Dockerfile.ingestion — container entrypoint for a Cloud Run Job
- Dockerfile.dashboard — container for a Cloud Run service

## Google Cloud setup

1. Select your existing Google Cloud project and enable BigQuery API. Enable Cloud Storage API only if you want raw JSON archival.
2. Create a dataset (or let the ingestion script create it) in the location you choose. Set GCP_PROJECT_ID, BQ_DATASET, and BQ_LOCATION.
3. For local development, authenticate with Application Default Credentials: gcloud auth application-default login. For Cloud Run, use a dedicated service account attached to the job/service; do not bake credentials into an image or commit key files.
4. Grant the ingestion service account permission to create/load tables in the dataset (for example, an appropriately scoped BigQuery data editor role plus job-user permission at the project level). The dashboard identity should have read-only access to the dataset.
5. Copy .env.example to .env for local development and configure a permitted TIMING_API_URL. Keep tokens in Secret Manager or Cloud Run environment secrets, never in Git.
6. Install dependencies with pip install -r requirements.txt.
7. Run tests: pytest.
8. Run ingestion locally: python -m ingestion.scrape_results.
9. Configure the dbt profile using dbt_marathon/profiles.yml.example, then run dbt debug --project-dir dbt_marathon --profiles-dir dbt_marathon and dbt build --project-dir dbt_marathon --profiles-dir dbt_marathon.
10. Run the dashboard locally with streamlit run dashboard/app.py.

## Cloud deployment direction

- Build and deploy Dockerfile.ingestion as a Cloud Run Job after confirming the source API schema and secrets.
- Schedule the job with Cloud Scheduler (or a Dagster deployment if you prefer centralized orchestration).
- Build and deploy Dockerfile.dashboard as a Cloud Run service. Use a read-only service account and configure the same project/dataset environment variables.
- Create budget alerts and monitor BigQuery query bytes processed. BigQuery, Cloud Storage, Cloud Run, and networking can incur charges.

The repository includes deployment-oriented scaffolding, not a completed deployment. No cloud resources are created by GitHub commits, and no live timing source has been verified yet.

## Initial analytics

- Finish-time leaderboard and finishing status
- Checkpoint split consistency
- Pace decay and negative/positive split flags (future model work)
- Finishing-time percentiles
- Data-quality checks for missing, duplicate, or invalid records

## Data and privacy

Do not commit API tokens, service-account keys, or raw participant data. Follow the timing provider's terms, rate limits, and privacy requirements. Use least-privilege IAM and avoid public access to datasets or buckets.

## License

See LICENSE.
