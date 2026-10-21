-- Expected source: marathon.raw_results
with source_data as (
    select * from {{ source('marathon', 'raw_results') }}
),
cleaned as (
    select
        cast(race_id as string) as race_id,
        trim(cast(bib as string)) as bib,
        upper(coalesce(cast(status as string), 'UNKNOWN')) as status,
        safe_cast(finish_seconds as int64) as finish_seconds,
        nullif(trim(cast(category as string)), '') as category,
        splits_json,
        ingested_at
    from source_data
)
select *
from cleaned
where bib is not null and bib != ''
