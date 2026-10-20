-- Une ligne par événement journalisé par l'application (EventLog) :
-- - API : écriture (POST, PUT, PATCH, DELETE) faite avec un jeton OAuth, réussie ou en échec
--   (jamais les GET) ; name = méthode et route au format OpenAPI ;
-- - IMPORT : import de fichier, réussi ou en échec ; name = type d'import.
-- Les détails de la colonne jsonb data sont éclatés en colonnes.

with source as (
    select * from {{ source('datawarehouse', 'event_logs_raw') }}
),

renamed as (
    select
        id                                                      as event_log_id,
        category,
        name,
        status,
        user_id,
        api_oauth2_application_id                               as application_id,
        canteen_id,
        creation_date,
        data ->> 'method'                                       as http_method,
        data ->> 'path'                                         as path,
        (data ->> 'status_code')::int                           as http_status_code,
        data ->> 'message'                                      as message,
        (data ->> 'count')::int                                 as row_count,
        (data ->> 'seconds')::numeric                           as duration_seconds,
        -- repris = reconstitué après coup (commandes eventlog_backfill_*) ou échec d'import
        -- migré depuis data_importfailure ; faux pour les événements journalisés en direct
        coalesce((data ->> 'backfilled')::boolean, false)
            or data ? 'import_failure_id'                       as is_backfilled,
        (data ->> 'import_type_uncertain')::boolean             as is_import_type_uncertain
    from source
)

select * from renamed
