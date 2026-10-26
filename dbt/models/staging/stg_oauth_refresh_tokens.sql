-- Une ligne par jeton de renouvellement OAuth2.
-- Un jeton révoqué (revoked renseigné) n'a plus de jeton d'accès lié (access_token_id null).

with source as (
    select * from {{ source('datawarehouse', 'oauth2_refresh_tokens_raw') }}
),

renamed as (
    select
        id                                  as refresh_token_id,
        application_id,
        user_id,
        access_token_id,
        created,
        revoked
    from source
)

select * from renamed
