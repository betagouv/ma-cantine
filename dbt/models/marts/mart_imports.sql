-- Une ligne par tentative d'import de fichier (événement IMPORT), réussie ou en échec.
-- Les types d'import sont regroupés par famille : les noms d'échecs anciens (PURCHASE,
-- CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE, DIAGNOSTIC_SIMPLE) n'ont pas d'équivalent côté succès.
-- jour = date de l'import à l'heure de Paris.

with imports as (
    select * from {{ ref('stg_event_logs') }}
    where category = 'IMPORT'
)

select
    i.event_log_id,
    i.creation_date                                         as date_import,
    (i.creation_date at time zone 'Europe/Paris')::date     as jour,
    i.name                                                  as type_import,
    case
        when i.name like 'PURCHASE%' then 'Achats'
        when i.name = 'CANTEEN_MANAGERS' then 'Gestionnaires'
        when i.name = 'CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE' then 'Bilans'   -- ancien type mixte (jusqu'au 02/2025)
        when i.name like 'CANTEEN%' then 'Cantines'
        when i.name like 'DIAGNOSTIC%' or i.name like 'CC%' then 'Bilans'
        else 'Autre'
    end                                                     as famille_import,
    i.status = 'SUCCESS'                                    as est_reussi,
    -- motif d'échec regroupé, repris de la carte 3811 ; null pour un import réussi
    case
        when i.status = 'SUCCESS' then null
        when i.message ~ '^L''import du fichier CSV a échoué' then 'Erreur générique à l''import'
        when i.message ~ '^La première ligne du fichier doit contenir' then 'En-tête : noms de colonnes incorrects'
        when i.message ~ '^Echec lors de la validation du header' then 'En-tête : rejeté par Validata'
        when i.message ~ '^Echec lors de la demande de validation' then 'Validata indisponible'
        when i.message ~ '^Echec lors de la validation du fichier' then 'Contenu : rejeté par Validata'
        when i.message ~ '^Ce fichier est (au|du) format' then 'Format : Excel au lieu de CSV'
        when i.message ~ '(UnicodeDecodeError|decode\(\) argument|character maps)' then 'Encodage du fichier (pas UTF-8)'
        when i.message ~ '^Ce fichier a déjà été utilisé' then 'Fichier déjà importé'
        when i.message ~ '^Ce fichier est trop grand' then 'Fichier trop volumineux'
        when i.message ~ 'new-line character' then 'CSV mal formé (retours à la ligne)'
        when i.message ~ '^Échec lors de la lecture du fichier' then 'Lecture du fichier impossible (erreur technique)'
        else 'Autre'
    end                                                     as motif_echec,
    substring(i.message from 'schema ([A-Za-z_]+)\.json')   as schema_validata,
    i.message,
    i.row_count                                             as nb_lignes,
    i.duration_seconds                                      as duree_secondes,
    i.user_id,
    coalesce(u.is_staff or u.is_dev, false)                 as utilisateur_est_equipe,
    i.canteen_id,
    i.is_backfilled                                         as est_repris,
    i.is_import_type_uncertain                              as type_import_incertain
from imports as i
left join {{ ref('stg_users') }} as u on i.user_id = u.user_id
