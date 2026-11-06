-- Référentiel des tutelles SPE téléversé par la DGAL dans Metabase (table des cibles) :
-- une ligne par tutelle (perimetre_key = code dbt de ministere_tutelle), sa définition la plus
-- récente. Seuls le libellé, le pôle ministériel et l'ordre d'affichage sont lus : les valeurs
-- de cible sont lues directement par les questions Metabase.

with source as (
    select * from {{ source('datawarehouse', 'spe_cibles') }}
),

renamed as (
    select distinct on (perimetre_key)
        perimetre_key,
        perimetre_lib,
        pole_ministeriel,
        sort_order                                  as ordre_affichage
    from source
    where niveau = 'tutelle'
    order by perimetre_key, annee_donnees desc
)

select * from renamed
