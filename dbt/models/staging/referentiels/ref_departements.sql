with source as (
    select * from {{ ref('stg_canteens') }}
    where department is not null
      and department_lib is not null
)

select distinct
    department              as code_departement,
    department_lib          as lib_departement,
    region                  as code_region
from source
order by department
