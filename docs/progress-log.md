# SCORE Marathon 2026 — Project Progress Log

**Last updated:** 23 October 2026  
**Project:** `score-marathon-de`  
**Current phase:** BigQuery validation and secure dashboard integration planning

## 1. Completed — local cleaning

The updated Python/pandas cleaning script ran successfully for all four race categories and the available split datasets.

| Category | Dataset | Input rows | Output rows |
| --- | --- | ---: | ---: |
| Marathon | Results | 5,802 | 5,802 |
| Marathon | Splits | 72,051 | 72,051 |
| Half Marathon | Results | 21,679 | 21,679 |
| Half Marathon | Splits | 183,593 | 183,593 |
| 10K | Results | 13,947 | 13,947 |
| 10K | Splits | 63,203 | 63,203 |
| 5K | Results | 9,817 | 9,817 |
| **Total** | **7 CSV outputs** | **376,092** | **376,092** |

- All seven datasets were processed without errors in the reported run.
- No rows were dropped.
- Source files were not overwritten.
- Outputs were written under `data/cleaned/<category>/`.
- The script generated `data/cleaned/quality_report.csv` and `data/cleaned/row_issues.csv`.
- The category input filename is standardized to `race_results.csv`, including `data/5k/race_results.csv`.

**Important:** row preservation and successful execution do not establish that the data is free of quality issues. The issue review remains open.

## 2. Completed — initial Google Cloud setup

- Uploaded the cleaned category folders to the existing private GCS bucket.
- Bucket location confirmed as `ASIA-SOUTHEAST1` (Singapore).
- BigQuery dataset `score_marathon` is configured in `asia-southeast1`.
- Created all seven BigQuery tables:
  - `marathon_results`
  - `marathon_splits`
  - `half_marathon_results`
  - `half_marathon_splits`
  - `10k_results`
  - `10k_splits`
  - `5k_results`

**Validation is not yet confirmed:** table creation does not prove that the loaded row counts match the local outputs. Run the row-count query and inspect table schemas before marking ingestion complete.

## 3. In progress — BigQuery validation

Expected counts based on local cleaned outputs:

| Table | Expected rows |
| --- | ---: |
| `marathon_results` | 5,802 |
| `marathon_splits` | 72,051 |
| `half_marathon_results` | 21,679 |
| `half_marathon_splits` | 183,593 |
| `10k_results` | 13,947 |
| `10k_splits` | 63,203 |
| `5k_results` | 9,817 |
| **Total** | **376,092** |

- [x] Create all seven tables.
- [ ] Run a row-count query across all seven BigQuery tables.
- [ ] Compare actual counts with the expected counts above.
- [ ] Inspect inferred column types, especially bib identifiers, timing fields, and checkpoint fields.
- [ ] Confirm blank/missing source values are represented appropriately.

## 4. Data-quality issues still under review

- Marathon results include a `missing_name` flag at source row index 4810.
- Marathon results have a series of `missing_gun_time` flags beginning around source row indices 4908 onward. Inspect the source records and count missing `gun_time` and `chip_time` separately before determining the cause.
- The 5K audit previously flagged bib, gun time, chip time, gender, nation, and status as missing in all 9,817 rows. Compare the CSV with the saved raw HTML to distinguish source-level absence from parser/schema mapping issues.
- Continue checking duplicate identifiers, status/time anomalies, and split-to-results consistency by category.
- Preserve source values. Do not invent missing data or silently correct timing/status fields.
- Record each reviewed issue as resolved, unresolved, or requiring source confirmation.

## 5. Next implementation steps

1. Validate row counts and schemas for the seven BigQuery tables.
2. Build a small secure API (recommended: Cloud Run) to query BigQuery for dashboard requests.
3. Use a dedicated service account with least-privilege permissions; keep credentials out of the browser and Git.
4. Connect the Lovable frontend to the API. Lovable currently has no backend connected.
5. Test category selection, leaderboard queries, participant lookup, and split retrieval.
6. Add automated validation and repeatable ingestion after the first end-to-end path works.

## 6. Security and repository hygiene

- Keep the GCS bucket and BigQuery tables private.
- Do not commit raw participant data, generated CSVs, API tokens, or service-account keys.
- Commit code, schemas, aggregate summaries, and documentation rather than participant-level extracts.
- dbt transformations, Dagster orchestration, and dashboard deployment remain future work until individually tested.
