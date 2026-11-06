-- Corrections du périmètre SPE téléversées par la DGAL dans Metabase : une ligne par SIRET.
-- SIRET exclu du périmètre État (exclure), ou forcé sur une tutelle (ministere_force, code dbt
-- de ministere_tutelle).

with source as (
    select * from {{ source('datawarehouse', 'spe_corrections_perimetre') }}
),

renamed as (
    select
        -- typé en entier au téléversement : zéros de tête perdus
        lpad(siret::text, 14, '0')                  as siret,
        nullif(line_ministry_force, '')             as ministere_force,
        coalesce(exclure, false)                    as exclure,
        motif
    from source
)

select * from renamed
