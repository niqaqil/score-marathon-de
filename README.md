# Score Marathon DE

An end-to-end data engineering project for SCORE Marathon 2026 race results, inspired by the Boom+ Run dashboard. The project uses Python/pandas for cleaning and quality checks, Google Cloud Storage for file storage, and BigQuery for analytics. A secure API and Lovable dashboard integration are planned next.

> **Current status (23 October 2026):** Local cleaning completed for four race categories. Seven cleaned CSV outputs were generated with **376,092 rows preserved** and no rows dropped. The cleaned category folders were uploaded to a private Google Cloud Storage bucket in `asia-southeast1` (Singapore). The BigQuery dataset `score_marathon` is configured for that region, and **all seven BigQuery tables have now been created**. Row-count and schema validation are still pending; table creation alone does not confirm that every table loaded the expected data. Data-quality issues remain under review. Lovable has no backend connected yet.

## Current progress

### Completed locally

- Standardized results input filenames as `race_results.csv` across `marathon/`, `half_marathon/`, `10k/`, and `5k/`.
- Ran the pandas cleaning script for four results datasets and three split datasets.
- Generated cleaned outputs under `data/cleaned/` and quality reports `quality_report.csv` and `row_issues.csv`.
- Preserved all **376,092 rows** across seven outputs; no rows were dropped and source files were not overwritten.
- Retained missing values rather than imputing unverified participant names or timing values.

### Google Cloud progress

- Uploaded the cleaned category folders to the existing private GCS bucket in `asia-southeast1`.
- Created/configured BigQuery dataset `score_marathon` in `asia-southeast1`.
- Created all seven BigQuery tables:
  - `marathon_results`
  - `marathon_splits`
  - `half_marathon_results`
  - `half_marathon_splits`
  - `10k_results`
  - `10k_splits`
  - `5k_results`
- **Pending:** verify actual row counts against the expected counts, inspect column types, and confirm missing-value representation.
- **Pending:** build a secure backend/API for Lovable. Do not expose service-account credentials in frontend code or make the bucket/tables public.

### Data-quality investigation still in progress

- Review the missing-name flag in Marathon results and the consecutive missing-gun-time flags around source row indices 4908 onward.
- Confirm whether missing timing values are source omissions or extraction/schema-mapping issues.
- Investigate the 5K output: previous audit flagged bib, timing, gender, nation, and status as missing in all 9,817 rows. Compare the CSV with its saved raw HTML before concluding those fields are absent from the source.
- Review duplicate and checkpoint consistency checks by category. Do not automatically alter status, timing, or checkpoint values based only on a flag.

## Dataset inventory

| Category | Dataset | Expected rows |
| --- | --- | ---: |
| Marathon | Results | 5,802 |
| Marathon | Splits | 72,051 |
| Half Marathon | Results | 21,679 |
| Half Marathon | Splits | 183,593 |
| 10K | Results | 13,947 |
| 10K | Splits | 63,203 |
| 5K | Results | 9,817 |
| **Total** | **7 CSV outputs** | **376,092** |

These are the local cleaned-output row counts and the baseline for BigQuery validation. They are not a claim that every data-quality issue has been resolved.

## Next steps

1. Run a BigQuery row-count query across all seven tables and compare with the inventory above.
2. Review inferred schema types and verify that bib identifiers, timing fields, and checkpoint fields are represented appropriately.
3. Investigate flagged source-data issues and record their dispositions without overwriting original data.
4. Create a secure Cloud Run API with least-privilege access to BigQuery.
5. Connect the Lovable frontend to the API and test leaderboard, participant lookup, and split endpoints.
6. Add automated validation and repeatable ingestion after the initial integration is verified.

See [the project progress log](docs/progress-log.md) for the current checkpoint and detailed validation notes.

## Intended architecture

~~~text
Race source / local CSVs
        |
        v
Python + pandas cleaning and issue reports
        |
        v
Private Google Cloud Storage (cleaned CSV files)
        |
        v
BigQuery tables
        |
        v
Secure Cloud Run API
        |
        v
Lovable dashboard
~~~

dbt transformations, Dagster orchestration, and additional analytics can be added after the initial cloud load and dashboard API are validated. These components should not be considered operational until individually tested.

## Repository structure

- `ingestion/` — ingestion implementation and source validation
- `dbt_marathon/` — BigQuery profile example, source declarations, staging models, and analytical marts
- `orchestration/` — Dagster asset scaffold
- `dashboard/` — dashboard scaffold
- `tests/` — schema and data-quality tests
- `docs/progress-log.md` — project progress and next validation steps
- `Dockerfile.ingestion` — container entrypoint for a Cloud Run Job
- `Dockerfile.dashboard` — container for a Cloud Run service

## Security and data handling

- Keep GCS buckets and BigQuery tables private.
- Use a dedicated service account with least-privilege permissions for the API.
- Keep credentials server-side; never place service-account keys in Lovable frontend code.
- Do not commit API tokens, service-account keys, raw participant data, or generated participant CSVs to Git.
- Follow the timing provider's terms, rate limits, and privacy requirements.

## License

See LICENSE.
