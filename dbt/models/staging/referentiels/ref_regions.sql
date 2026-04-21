with source as (
    select * from {{ ref('stg_canteens') }}
    where region is not null
      and region_lib is not null
)

select distinct
    region                  as code_region,
    region_lib              as lib_region
from source
order by region
