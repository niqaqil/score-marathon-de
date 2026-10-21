-- Expected source: marathon.raw_results
with source_data as (
    select * from {{ source('marathon', 'raw_results') }}
), cleaned as (
    select
        cast(race_id as varchar) as race_id,
        trim(cast(bib as varchar)) as bib,
        upper(coalesce(cast(status as varchar), 'UNKNOWN')) as status,
        try_cast(finish_seconds as integer) as finish_seconds,
        nullif(trim(cast(category as varchar)), '') as category
    from source_data
)
select * from cleaned where bib is not null and bib <> ''
