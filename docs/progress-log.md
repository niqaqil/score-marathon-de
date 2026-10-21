# SCORE Marathon 2026 — Project Progress Log

**Last updated:** 21 October 2026  
**Project:** `score-marathon-de`  
**Current phase:** Data-quality investigation and source extraction validation

## 1. Completed

### Marathon source extraction

- Results extracted: **5,802 rows**
- Unique bibs: **5,802**
- Checkpoint split records: **72,051**
- Checkpoint labels observed: `Start`, `CP1` through `CP12`, and `Finish`
- No duplicate bibs were found in the extracted Marathon results during the recorded audit.
- The source's blank status field is retained as a blank value; it is not automatically interpreted as a finishing status.

### Initial data-quality audit

- Generated checkpoint and finish-checkpoint audit outputs and a combined issue-flag report.
- Initial checks identified missing finish times, status/checkpoint mismatches, and records requiring manual review.
- **894** results have no finish time, matching the **894** finish-checkpoint rows with blank timing fields.
- Status values observed include blank, DNF, DNS, OOC, and DSQ.
- Some DNF/DNS records have timing data; these are flagged for review rather than silently corrected.

## 2. In progress — data-quality investigation

The initial audit is complete, but the investigation is **not yet complete**. The current focus is reviewing flagged records and recording a disposition for each issue.

- Preserve all original source values.
- Distinguish verified inconsistencies from items that need more context or source confirmation.
- Mark each reviewed issue as resolved, unresolved, or requiring source confirmation.
- Do not automatically change runner status, finish times, or checkpoint values based only on a flag.

## 3. Multi-category extraction

The HeyJom category query values have been identified:

| Race category | API category parameter |
| --- | --- |
| Marathon | `MARATHON` |
| Half Marathon | `HALF MARATHON` |
| 10K | `10K` |

A Python extractor has been prepared to save each category's result CSV, split CSV, and raw HTML into separate folders. The current script uses a small test limit of three runners per category.

**Not yet verified:** live extraction for Half Marathon and 10K, split-endpoint correctness for those categories, and full multi-category counts.

## 4. Next actions

- [ ] Review flagged Marathon records and record a disposition in the issue log.
- [ ] Confirm or document unresolved status/time and checkpoint anomalies without overwriting source values.
- [ ] Run the three-runner test for each category.
- [ ] Check category labels and runner bibs in each results CSV.
- [ ] Check that the split endpoint returns valid checkpoint rows for test bibs.
- [ ] Confirm pagination reaches all pages without repeating bibs.
- [ ] Set `MAX_RUNNERS = None` and run full extraction after the test passes.
- [ ] Run category-specific data-quality reports.
- [ ] Plan and test BigQuery loading only after the local extracts are validated.

## 5. Data handling

Keep raw participant data, detailed results, and generated CSVs out of the public repository unless publication is appropriate and permitted. Commit code, schemas, aggregate summaries, and documentation instead. Do not commit API tokens, service-account keys, or other secrets.

## 6. Project status boundaries

This progress log describes local work and the current extraction plan. It does **not** claim that the flagged-record review is complete, Half Marathon/10K extraction is complete, or BigQuery ingestion, dbt transformations, Dagster orchestration, or cloud deployment have completed.
