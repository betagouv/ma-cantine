-- Une ligne par application OAuth2 (logiciel client de l'API), avec son éditeur.
-- Règles reprises telles quelles des cartes du dashboard Metabase 86.

select
    a.application_id,
    a.name                                                  as application_nom,
    -- éditeur = « nom de l'entreprise » saisi dans l'admin (fiche de l'application OAuth2)
    coalesce(nullif(e.company_name, ''), 'À qualifier : ' || a.name)
                                                            as editeur,
    nullif(e.company_name, '') is null                      as est_a_qualifier,
    -- company_name ne distingue pas les tests : on les repère au nom
    (a.name ~* '(test|recette|demo|\mdev\M)' or a.name ~ '[<>]' or trim(a.name) = '')
                                                            as est_test,
    a.authorization_grant_type                              as type_autorisation,
    split_part(u.email, '@', 2)                             as proprietaire_domaine,
    a.created                                               as date_creation
from {{ ref('stg_oauth_applications') }} as a
left join {{ ref('stg_oauth_applications_extra') }} as e on a.application_id = e.application_id
left join {{ ref('stg_users') }} as u on a.user_id = u.user_id
