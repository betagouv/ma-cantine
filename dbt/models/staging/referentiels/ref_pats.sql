with source as (
    select * from {{ ref('stg_canteens') }}
    where pat_list is not null
      and pat_list != '[]'
      and pat_lib_list is not null
      and pat_lib_list != '[]'
),

unnested as (
    select
        jsonb_array_elements_text(pat_list::jsonb)      as code_pat,
        jsonb_array_elements_text(pat_lib_list::jsonb)  as lib_pat
    from source
)

select distinct
    code_pat,
    lib_pat
from unnested
where code_pat is not null
order by code_pat
