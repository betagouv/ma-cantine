{{ config(materialized='table') }}

-- Indicateurs gaspillage alimentaire par (perimetre_key, annee)
-- Source : stg_waste_measurements JOIN stg_canteens (classification courante)
-- Inclut les périmètres line_ministry ET les sous-totaux groupe (UNION ALL)

with waste as (
    select * from {{ ref('stg_waste_measurements') }}
),

canteens as (
    select
        canteen_id,
        line_ministry
    from {{ ref('stg_canteens') }}
    where line_ministry is not null
      and line_ministry != ''
),

by_line_ministry as (
    select
        w.annee,
        c.line_ministry                                             as perimetre_key,
        count(distinct w.canteen_id)                               as nb_canteens_avec_mesure,
        sum(w.total_mass)                                          as total_mass_kg,
        sum(w.meal_count)                                          as total_meal_count
    from waste w
    join canteens c on c.canteen_id = w.canteen_id
    group by w.annee, c.line_ministry
),

by_groupe as (
    select
        annee,
        case
            when perimetre_key in ('ecologie', 'mer')                             then 'MTE'
            when perimetre_key in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre_key in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre_key in ('travail', 'sante')                            then 'Ministères sociaux'
        end                                                                        as perimetre_key,
        sum(nb_canteens_avec_mesure)                               as nb_canteens_avec_mesure,
        sum(total_mass_kg)                                         as total_mass_kg,
        sum(total_meal_count)                                      as total_meal_count
    from by_line_ministry
    where perimetre_key in (
        'ecologie', 'mer',
        'jeunesse', 'enseignement_superieur', 'sport',
        'justice_hors_pjj', 'justice_pjj',
        'travail', 'sante'
    )
    group by
        annee,
        case
            when perimetre_key in ('ecologie', 'mer')                             then 'MTE'
            when perimetre_key in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre_key in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre_key in ('travail', 'sante')                            then 'Ministères sociaux'
        end
),

all_perimetres as (
    select * from by_line_ministry
    union all
    select * from by_groupe
)

select
    annee,
    perimetre_key,
    nb_canteens_avec_mesure,
    total_mass_kg,
    total_meal_count,

    -- g/couvert (total_mass est en kg → ×1000)
    round(
        (total_mass_kg * 1000 / nullif(total_meal_count, 0))::numeric, 1
    )                                                              as gaspi_g_par_couvert,

    -- niveau ADEME
    case
        when total_meal_count is null or total_meal_count = 0     then null
        when total_mass_kg * 1000 / total_meal_count <= 47        then 'Niveau 3'
        when total_mass_kg * 1000 / total_meal_count <= 74        then 'Niveau 2'
        when total_mass_kg * 1000 / total_meal_count <= 95        then 'Niveau 1'
        else                                                           'Non atteint'
    end                                                            as niveau_ademe

from all_perimetres
