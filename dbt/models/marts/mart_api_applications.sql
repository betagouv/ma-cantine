-- Une ligne par application OAuth2 (logiciel client de l'API), utilisée ou non.
-- Connexions = jetons obtenus ou renouvelés (int_api_connexions) ; écritures = requêtes
-- d'écriture API réussies (EventLog). Une application jamais utilisée garde sa ligne,
-- avec des comptes à 0. Le statut (actif, inactif…) reste calculé dans les cartes.

with connexions as (
    select
        application_id,
        min(date_connexion)                                 as premiere_connexion,
        max(date_connexion)                                 as derniere_connexion,
        count(distinct user_id)                             as nb_utilisateurs,
        -- couples (utilisateur, jour de Paris) distincts
        count(distinct row(user_id, (date_connexion at time zone 'Europe/Paris')::date))
                                                            as nb_jours_connexion
    from {{ ref('int_api_connexions') }}
    group by application_id
),

ecritures as (
    select
        application_id,
        count(*)                                            as nb_ecritures,
        count(distinct user_id)                             as nb_utilisateurs_ayant_ecrit,
        max(creation_date)                                  as derniere_ecriture
    from {{ ref('stg_event_logs') }}
    where category = 'API'
      and status = 'SUCCESS'
      and application_id is not null
    group by application_id
)

select
    a.application_id,
    a.application_nom,
    a.editeur,
    a.est_a_qualifier,
    a.est_test,
    a.type_autorisation,
    a.proprietaire_domaine,
    a.date_creation,
    c.premiere_connexion,
    c.derniere_connexion,
    coalesce(c.nb_utilisateurs, 0)                          as nb_utilisateurs,
    coalesce(c.nb_jours_connexion, 0)                       as nb_jours_connexion,
    coalesce(e.nb_ecritures, 0)                             as nb_ecritures,
    coalesce(e.nb_utilisateurs_ayant_ecrit, 0)              as nb_utilisateurs_ayant_ecrit,
    e.derniere_ecriture
from {{ ref('int_api_applications') }} as a
left join connexions as c on a.application_id = c.application_id
left join ecritures as e on a.application_id = e.application_id
