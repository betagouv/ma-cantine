with source as (
    select * from {{ ref('stg_canteens') }}
    where epci is not null
      and epci_lib is not null
)

select distinct
    epci                    as code_epci,
    epci_lib                as lib_epci,
    department              as code_departement,
    region                  as code_region
from source
order by epci
