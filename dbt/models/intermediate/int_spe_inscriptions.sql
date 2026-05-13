{{ config(materialized='table') }}

-- Dénominateurs SPE : nb cantines inscrites au 29 avril de l'année n+1
-- Une ligne par (perimetre, type_perimetre, annee)
-- type_perimetre = 'line_ministry' | 'groupe'

with canteens_spe as (
    select
        line_ministry,
        creation_date
    from {{ ref('stg_canteens') }}
    where line_ministry is not null
      and line_ministry != ''
),

years as (
    select distinct year as annee
    from {{ ref('stg_teledeclarations') }}
    where line_ministry is not null
      and line_ministry != ''
),

by_line_ministry as (
    select
        c.line_ministry             as perimetre,
        'line_ministry'             as type_perimetre,
        y.annee,
        count(*)                    as nb_inscrites
    from canteens_spe c
    cross join years y
    where c.creation_date <= make_date(y.annee::int + 1, 4, 29)
    group by c.line_ministry, y.annee
),

by_groupe as (
    select
        case
            when perimetre in ('ecologie', 'mer')                             then 'MTE'
            when perimetre in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre in ('travail', 'sante')                            then 'Ministères sociaux'
        end                         as perimetre,
        'groupe'                    as type_perimetre,
        annee,
        sum(nb_inscrites)           as nb_inscrites
    from by_line_ministry
    where perimetre in (
        'ecologie', 'mer',
        'jeunesse', 'enseignement_superieur', 'sport',
        'justice_hors_pjj', 'justice_pjj',
        'travail', 'sante'
    )
    group by 1, annee
)

select * from by_line_ministry
union all
select * from by_groupe
