with source as (
    select * from {{ ref('stg_canteens') }}
    where city_insee_code is not null
      and city is not null
),

-- un seul libellé par code INSEE : on prend le plus fréquent
ranked as (
    select
        city_insee_code,
        city,
        department,
        region,
        count(*) as nb,
        row_number() over (
            partition by city_insee_code
            order by count(*) desc, city asc
        ) as rn
    from source
    group by city_insee_code, city, department, region
)

select
    city_insee_code         as code_insee_commune,
    city                    as lib_commune,
    department              as code_departement,
    region                  as code_region
from ranked
where rn = 1
order by city_insee_code
