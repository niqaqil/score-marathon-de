# dbt + BigQuery

The project uses the dbt-bigquery adapter. Copy profiles.yml.example to profiles.yml in this directory (the local file is ignored by Git), then set GCP_PROJECT_ID, BQ_DATASET, and BQ_LOCATION in your environment.

For local development, authenticate using Application Default Credentials:

~~~bash
gcloud auth application-default login
pip install -r requirements.txt
dbt debug --project-dir dbt_marathon --profiles-dir dbt_marathon
dbt build --project-dir dbt_marathon --profiles-dir dbt_marathon
~~~

The source declaration expects the ingestion-created raw_results table in the configured dataset. Confirm that the timing provider's fields map to RaceResult before running against live data. No credentials or service-account keys belong in this repository.
