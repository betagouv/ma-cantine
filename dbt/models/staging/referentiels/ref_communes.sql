with source as (
    select * from {{ ref('stg_canteens') }}
    where city_insee_code is not null
      and city is not null
)

select distinct
    city_insee_code         as code_insee_commune,
    city                    as lib_commune,
    postal_code,
    department              as code_departement,
    region                  as code_region
from source
order by city_insee_code
