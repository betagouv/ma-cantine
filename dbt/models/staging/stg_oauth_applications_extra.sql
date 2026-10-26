-- Une ligne par application OAuth2 : champs saisis dans l'admin (nom de l'entreprise).

with source as (
    select * from {{ source('datawarehouse', 'oauth2_applications_extra_raw') }}
),

renamed as (
    select
        application_id,
        company_name
    from source
)

select * from renamed
