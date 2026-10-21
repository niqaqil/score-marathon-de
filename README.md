# Score Marathon DE

An end-to-end data engineering project for marathon race results, inspired by the Boom+ Run dashboard. The goal is to ingest timing data, validate it, store it in DuckDB, transform it with dbt, orchestrate the pipeline with Dagster, and expose race-performance insights through Streamlit.

> **Status:** Initial setup. A timing API endpoint and its access rules must be confirmed before live ingestion can run.

## Architecture

```text
Timing API / JSON export
        |
        v
Python ingestion + Pydantic validation
        |
        v
DuckDB
        |
        v
dbt staging -> analytical marts
        |
        v
Dagster orchestration
        |
        v
Streamlit + Plotly dashboard
```

## Planned repository structure

- `ingestion/` — asynchronous ingestion and Pydantic validation
- `dbt_marathon/` — staging models and analytical marts
- `orchestration/` — Dagster assets
- `dashboard/` — Streamlit and Plotly UI
- `tests/` — schema and transformation tests
- `data/` — local data files (not committed)

## Initial analytics

- Finish-time leaderboard and finishing status
- Checkpoint split consistency
- Pace decay and negative/positive split flags
- Finishing-time percentiles
- Data-quality checks for missing, duplicate, or invalid records

## Development roadmap

- [ ] Confirm the race timing API/export format and permitted access method
- [ ] Implement pagination, retries, and rate-limit handling
- [ ] Validate incoming results with Pydantic
- [ ] Persist raw and normalized records to DuckDB
- [ ] Build dbt staging models and analytical marts
- [ ] Orchestrate ingestion and transformations with Dagster
- [ ] Build dashboard filters and charts
- [ ] Add tests and continuous integration

## Getting started

Python 3.11+ is recommended. Starter dependencies and configuration will be added as the pipeline implementation progresses.

Do not commit API tokens, secrets, or raw participant data. Follow the timing provider's terms, rate limits, and privacy requirements.

## License

See [LICENSE](LICENSE).
