{{ config(materialized='table') }}

-- Dénominateurs SPE : nb cantines inscrites au 29 avril de l'année n+1
-- Une ligne par (perimetre, type_perimetre, annee)
-- type_perimetre = 'line_ministry' | 'groupe'
-- La population (cantine × année) vient de int_spe_canteens_inscrites : les cantines
-- supprimées après la date de référence restent comptées.

with by_line_ministry as (
    select
        line_ministry               as perimetre,
        'line_ministry'             as type_perimetre,
        annee,
        count(*)                    as nb_inscrites
    from {{ ref('int_spe_canteens_inscrites') }}
    group by line_ministry, annee
),

by_groupe as (
    select
        case
            when perimetre in ('ecologie', 'mer')                             then 'MTE'
            when perimetre in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre in ('travail', 'sante')                            then 'Ministères sociaux'
            when perimetre in ('interieur', 'administration_territoriale')    then 'Périmètre intérieur'
        end                         as perimetre,
        'groupe'                    as type_perimetre,
        annee,
        sum(nb_inscrites)           as nb_inscrites
    from by_line_ministry
    where perimetre in (
        'ecologie', 'mer',
        'jeunesse', 'enseignement_superieur', 'sport',
        'justice_hors_pjj', 'justice_pjj',
        'travail', 'sante',
        'interieur', 'administration_territoriale'
    )
    group by 1, annee
)

select * from by_line_ministry
union all
select * from by_groupe
