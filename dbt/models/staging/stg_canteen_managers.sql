with source as (
    select * from {{ source('datawarehouse', 'canteen_managers_raw') }}
),

renamed as (
    select
        canteen_id,
        user_id
    from source
)

select * from renamed