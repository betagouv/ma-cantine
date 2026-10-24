-- Une ligne par jeton d'accès OAuth2 encore présent en base.
-- Au renouvellement, django-oauth-toolkit supprime le jeton d'accès (voir int_api_connexions).

with source as (
    select * from {{ source('datawarehouse', 'oauth2_access_tokens_raw') }}
),

renamed as (
    select
        id                                  as access_token_id,
        application_id,
        user_id,
        source_refresh_token_id,
        created,
        expires,
        scope
    from source
)

select * from renamed
