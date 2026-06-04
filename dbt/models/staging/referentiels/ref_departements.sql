with source as (
    select * from {{ ref('stg_canteens') }}
    where department is not null
      and department_lib is not null
),

ranked as (
    select
        department,
        department_lib,
        region,
        row_number() over (
            partition by department
            order by count(*) desc, department_lib asc
        ) as rn
    from source
    group by department, department_lib, region
)

select
    department              as code_departement,
    department_lib          as lib_departement,
    region                  as code_region
from ranked
where rn = 1
order by department
