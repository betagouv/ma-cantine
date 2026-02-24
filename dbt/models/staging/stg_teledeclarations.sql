with source as (
    select * from {{ source('datawarehouse', 'teledeclarations') }}
)

select * from source
