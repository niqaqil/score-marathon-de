# dbt + DuckDB

Install the root requirements, then create `~/.dbt/profiles.yml`:

```yaml
dbt_marathon:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: /absolute/path/to/score-marathon-de/data/marathon.duckdb
      schema: main
      threads: 4
```

Update the path for your machine. Configure dbt sources after the ingestion table schema is finalized.
