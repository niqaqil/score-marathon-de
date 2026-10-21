# SCORE Marathon 2026 — Project Progress Log

**Last updated:** 21 October 2026  
**Project:** `score-marathon-de`  
**Current phase:** Source extraction and data-quality validation

## 1. Completed

### Marathon source extraction

- Results extracted: **5,802 rows**
- Unique bibs: **5,802**
- Checkpoint split records: **72,051**
- Checkpoint labels observed: `Start`, `CP1` through `CP12`, and `Finish`
- No duplicate bibs were found in the extracted Marathon results during the recorded audit.
- The source's blank status field is retained as a blank value; it is not automatically interpreted as a finishing status.

### Data-quality investigation

The investigation reviewed missing finish times, checkpoint completeness, source status values, and the consistency of finish-checkpoint records.

Key observations from the Marathon audit:

- **894** results have no finish time, matching the **894** finish-checkpoint rows with blank timing fields.
- Status values observed include blank, DNF, DNS, OOC, and DSQ.
- Some DNF/DNS records have timing data; these are flagged for review rather than silently corrected.
- A review log and supporting audit CSVs were generated locally. Flags indicate records needing investigation; they are not source-data corrections.

## 2. Multi-category extraction

The HeyJom category query values have been identified:

| Race category | API category parameter |
| --- | --- |
| Marathon | `MARATHON` |
| Half Marathon | `HALF MARATHON` |
| 10K | `10K` |

A Python extractor has been prepared to save each category's result CSV, split CSV, and raw HTML into separate folders. The current script uses a small test limit of three runners per category.

**Not yet verified:** live extraction for Half Marathon and 10K, split-endpoint correctness for those categories, and full multi-category counts.

## 3. Next actions

- [ ] Run the three-runner test for each category.
- [ ] Check category labels and runner bibs in each results CSV.
- [ ] Check that the split endpoint returns valid checkpoint rows for test bibs.
- [ ] Confirm pagination reaches all pages without repeating bibs.
- [ ] Set `MAX_RUNNERS = None` and run full extraction after the test passes.
- [ ] Run category-specific data-quality reports.
- [ ] Review unresolved flags before making any data corrections.
- [ ] Plan and test BigQuery loading only after the local extracts are validated.

## 4. Data handling

Keep raw participant data, detailed results, and generated CSVs out of the public repository unless publication is appropriate and permitted. Commit code, schemas, aggregate summaries, and documentation instead. Do not commit API tokens, service-account keys, or other secrets.

## 5. Project status boundaries

This progress log describes local work and the current extraction plan. It does **not** claim that Half Marathon/10K extraction, BigQuery ingestion, dbt transformations, Dagster orchestration, or cloud deployment have completed.
