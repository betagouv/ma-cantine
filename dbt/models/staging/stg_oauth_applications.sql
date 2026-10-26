-- Une ligne par application OAuth2 (logiciel client de l'API).

with source as (
    select * from {{ source('datawarehouse', 'oauth2_applications_raw') }}
),

renamed as (
    select
        id                                  as application_id,
        name,
        user_id,
        client_type,
        authorization_grant_type,
        created,
        updated
    from source
)

select * from renamed
