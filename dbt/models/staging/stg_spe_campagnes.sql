-- Calendrier des campagnes de télédéclaration téléversé par la DGAL dans Metabase : une ligne
-- par année de données (campagne en n+1), dates d'ouverture, de clôture et de fin de correction.

with source as (
    select * from {{ source('datawarehouse', 'spe_campagnes') }}
),

renamed as (
    select
        annee_donnees::int                          as annee,
        annee_campagne::int                         as annee_campagne,
        date_ouverture,
        date_cloture,
        date_fin_correction,
        statut_dates
    from source
)

select * from renamed
