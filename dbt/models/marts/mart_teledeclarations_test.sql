with source as (
    select * from {{ source('datawarehouse', 'teledeclarations') }}
),

final as (
    select
        *
    from source
)

select * from final
