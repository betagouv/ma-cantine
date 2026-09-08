with source as (
    select * from {{ ref('stg_canteens') }}
    where epci is not null
      and epci_lib is not null
),

ranked as (
    select
        epci,
        epci_lib,
        count(*) as nb,
        row_number() over (
            partition by epci
            order by count(*) desc, epci_lib asc
        ) as rn
    from source
    group by epci, epci_lib
)

select
    epci                    as code_epci,
    epci_lib                as lib_epci
from ranked
where rn = 1
order by epci
