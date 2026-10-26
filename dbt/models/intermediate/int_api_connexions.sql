-- Une ligne par jeton obtenu ou renouvelé par un logiciel (= une connexion à l'API).
-- Au renouvellement, django-oauth-toolkit supprime le jeton d'accès et garde le jeton de
-- renouvellement (révoqué, sans jeton d'accès lié) : on le reprend pour ne pas perdre ces
-- connexions (sinon les logiciels qui renouvellent, Salamandre surtout, sont sous-comptés).
-- Les jetons sans utilisateur sont gardés, comme dans les cartes.

select
    'acces'                                                 as type_jeton,
    access_token_id                                         as jeton_id,
    application_id,
    user_id,
    created                                                 as date_connexion,
    expires                                                 as date_expiration
from {{ ref('stg_oauth_access_tokens') }}
union all
select
    'renouvellement',
    refresh_token_id,
    application_id,
    user_id,
    created,
    created + interval '10 hours'   -- durée de vie d'un jeton d'accès (valeur par défaut)
from {{ ref('stg_oauth_refresh_tokens') }}
where access_token_id is null
