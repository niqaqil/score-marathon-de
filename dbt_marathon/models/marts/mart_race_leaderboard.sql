select
    race_id,
    bib,
    category,
    finish_seconds,
    rank() over (partition by race_id order by finish_seconds) as overall_rank,
    case when finish_seconds > 0 then 3600.0 * 42.195 / finish_seconds else null end as marathon_equivalent_kmh
from {{ ref('stg_race_results') }}
where status = 'FINISHED' and finish_seconds is not null
