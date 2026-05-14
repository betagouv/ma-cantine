with source as (
    select * from {{ ref('stg_canteens') }}
    where region is not null
      and region_lib is not null
),

ranked as (
    select
        region,
        region_lib,
        row_number() over (
            partition by region
            order by count(*) desc, region_lib asc
        ) as rn
    from source
    group by region, region_lib
)

select
    region                  as code_region,
    region_lib              as lib_region
from ranked
where rn = 1
order by region
