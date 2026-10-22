# Score Marathon DE

An end-to-end data engineering project for SCORE Marathon 2026 race results, inspired by the Boom+ Run dashboard. The project is being developed around Python/pandas ingestion and data-quality investigation, with Google Cloud, BigQuery, dbt, Dagster, and Streamlit/Plotly as the intended analytics stack.

> **Current status (22 October 2026):** Marathon results have been extracted. Data-quality investigation is **in progress**: initial audits and review flags exist, but flagged records and unresolved issues still need to be reviewed. The multi-category extractor is prepared for Marathon, Half Marathon, and 10K, but the Half Marathon and 10K live extraction still needs a small test run. A dedicated 5KM extraction returned 9,817 rows across 10 pages; its current CSV flags bib, timing, gender, nation, and status as missing for every row. This needs CSV/raw-HTML inspection to distinguish source-level absence from a parsing/schema-mapping issue. Cloud ingestion and deployment are not yet confirmed as operational.

## Current progress

### Completed locally

- Extracted **5,802 Marathon result records** and **72,051 checkpoint split records**.
- Completed initial duplicate-bib and checkpoint-consistency checks for the Marathon extraction.
- Generated initial data-quality review outputs, including checkpoint and finish-checkpoint audits and flagged records.
- Ran the dedicated 5KM extraction using the HeyJom endpoint with category=5KM: 9,817 rows across 10 pages (pages 1–9 returned 1,000 rows each; page 10 returned 817 rows).

### In progress

- Reviewing flagged Marathon records and unresolved data-quality issues.
- Investigating missing finish times and differences between source status and checkpoint completeness.
- Confirming which anomalies reflect source data versus issues that need further investigation. Source values are preserved; flags are not automatic corrections.
- Validating the 5KM output: bib, gun time, chip time, gender, nation, and status are flagged missing in all 9,817 rows. This may be due to source fields being absent or a parser/schema-mapping issue; inspect the CSV and saved raw HTML before concluding.

### Prepared for next validation

- Confirmed the HeyJom category query parameters:
  - Marathon: `MARATHON`
  - Half Marathon: `HALF MARATHON`
  - 10K: `10K`
  - 5KM: `5KM`
- Prepared a multi-category Python extractor that separates results, splits, and raw HTML by race category. It currently defaults to a three-runner test per category.

### Next steps

1. Inspect the 5KM CSV columns and first records; compare with `data/5km/raw_pages/page_001.html` to distinguish source absence from parser/schema-mapping issues.
2. Validate 5KM pagination, unique names/places, category values, and potential repeated records. Do not treat Place as a bib or invent timing data.
3. Continue reviewing the Marathon issue log and document each issue as reviewed, unresolved, or requiring source confirmation.
4. Run the multi-category extractor with the small test limit.
5. Verify that each category returns the expected runners and that the split endpoint returns valid checkpoint tables.
6. Review the test CSVs, then set `MAX_RUNNERS = None` for full extraction.
7. Run quality checks independently for each category.
6. Keep raw participant data and generated race CSVs out of Git unless there is a clear, appropriate reason and permission to publish them.
7. After extraction and validation are stable, plan ingestion into BigQuery and build dbt models and dashboard analytics.

See [the project progress log](docs/progress-log.md) for the current checkpoint and validation notes.

## Architecture

~~~text
HeyJom results API
        |
        v
Python extraction + raw HTML archive
        |
        v
Category-specific results and checkpoint CSVs
        |
        v
Data-quality validation and review
        |
        v
BigQuery raw/staging tables
        |
        v
dbt analytical models
        |
        v
Dagster orchestration
        |
        v
Streamlit + Plotly dashboard
~~~

The cloud components above describe the intended architecture. Cloud ingestion, orchestration, and deployment remain follow-up work and should not be considered live until individually tested.

## Repository structure

- `ingestion/` — ingestion implementation and source validation
- `dbt_marathon/` — BigQuery profile example, source declarations, staging models, and analytical marts
- `orchestration/` — Dagster asset scaffold
- `dashboard/` — Streamlit and Plotly dashboard
- `tests/` — schema and data-quality tests
- `docs/progress-log.md` — project progress and next validation steps
- `Dockerfile.ingestion` — container entrypoint for a Cloud Run Job
- `Dockerfile.dashboard` — container for a Cloud Run service

## Google Cloud setup

1. Select the intended Google Cloud project and enable the BigQuery API. Enable Cloud Storage API only if raw archival is required.
2. Create a BigQuery dataset in the selected location and configure `GCP_PROJECT_ID`, `BQ_DATASET`, and `BQ_LOCATION`.
3. For local development, authenticate with Application Default Credentials: `gcloud auth application-default login`. For Cloud Run, use a dedicated service account.
4. Grant least-privilege access to the ingestion identity and read-only access to the dashboard identity.
5. Configure local environment variables using `.env.example`. Keep tokens in Secret Manager or environment secrets; never commit credentials.
6. Install dependencies with `pip install -r requirements.txt`.
7. Run tests with `pytest`.
8. Validate the source schema and ingestion code before running cloud ingestion.
9. Configure dbt using `dbt_marathon/profiles.yml.example`, then run `dbt debug` and `dbt build` with the appropriate project/profile directories.
10. Run the dashboard locally with `streamlit run dashboard/app.py`.

## Initial analytics

- Finish-time leaderboard and finishing status
- Checkpoint split consistency
- Pace decay and negative/positive split flags
- Finishing-time percentiles
- Data-quality checks for missing, duplicate, or invalid records
- Comparisons across Marathon, Half Marathon, and 10K

## Data and privacy

Do not commit API tokens, service-account keys, or raw participant data. Follow the timing provider's terms, rate limits, and privacy requirements. Use least-privilege IAM and avoid public access to datasets or buckets.

## License

See LICENSE.
