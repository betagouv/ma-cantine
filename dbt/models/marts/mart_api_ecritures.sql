-- Une ligne par requête d'écriture API (POST, PUT, PATCH, DELETE) faite par un logiciel,
-- c'est-à-dire avec une application OAuth2, réussie ou en échec.
-- jour = date de la requête à l'heure de Paris.

with evenements as (
    select
        *,
        split_part(name, ' ', 1)                            as methode,
        split_part(name, ' ', 2)                            as route
    from {{ ref('stg_event_logs') }}
    where category = 'API'
      -- Règle validée le 20/10/2026 : seules les requêtes avec une application OAuth comptent.
      -- La reprise de l'historique a recopié creation_source, faux pour les achats et le
      -- gaspillage, et y a mis les bilans de satellites générés depuis un groupe (sans
      -- application). En direct, toute requête journalisée a une application.
      and application_id is not null
),

qualifiees as (
    select
        *,
        case
            when route like '%/diagnostics/%' then 'Bilans'
            when route like '%/purchases/%' then 'Achats'
            when route like '%/wasteMeasurements/%' then 'Évaluations gaspillage'
            when route in ('/api/v1/canteens/', '/api/v1/canteens/{id}') then 'Cantines'
            else 'Autre'   -- satellites, gestionnaires, logo… (aucune au 20/10)
        end                                                 as type_donnees,
        case
            when route like '%/teledeclaration/create' then 'Télédéclaration'
            when route like '%/teledeclaration/cancel' then 'Annulation de télédéclaration'
            when methode = 'POST' then 'Création'
            when methode in ('PATCH', 'PUT') then 'Modification'
            when methode = 'DELETE' then 'Suppression'
        end                                                 as action
    from evenements
)

select
    q.event_log_id,
    q.creation_date                                         as date_ecriture,
    (q.creation_date at time zone 'Europe/Paris')::date     as jour,
    q.route,
    q.type_donnees,
    q.action,
    -- objet visé quand on le connaît ; null pour une création de bilan, d'achat ou
    -- d'évaluation (route de collection)
    case
        -- création de cantine : le middleware renseigne la cantine créée
        when q.type_donnees = 'Cantines' and q.action = 'Création' then q.canteen_id
        -- routes en {id} : même position dans le chemin que {id} dans la route
        else (string_to_array(q.path, '/'))[array_position(string_to_array(q.route, '/'), '{id}')]::bigint
    end                                                     as objet_id,
    q.status = 'SUCCESS'                                    as est_reussie,
    q.http_status_code                                      as code_http,
    q.message,
    q.application_id,
    a.application_nom,
    a.editeur,
    a.est_test,
    q.user_id,
    coalesce(u.is_staff or u.is_dev, false)                 as utilisateur_est_equipe,
    q.canteen_id,
    q.is_backfilled                                         as est_repris
from qualifiees as q
left join {{ ref('int_api_applications') }} as a on q.application_id = a.application_id
left join {{ ref('stg_users') }} as u on q.user_id = u.user_id
