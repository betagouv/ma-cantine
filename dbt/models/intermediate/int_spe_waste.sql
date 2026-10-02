{{ config(materialized='table') }}

-- Indicateurs gaspillage alimentaire par (perimetre_key, annee)
-- Agrégation de int_spe_waste_by_canteen (qui porte les filtres et le niveau ADEME)
-- Inclut les périmètres line_ministry ET les sous-totaux groupe (UNION ALL)

with by_canteen as (
    select * from {{ ref('int_spe_waste_by_canteen') }}
),

by_line_ministry as (
    select
        annee,
        line_ministry                                                    as perimetre_key,
        count(canteen_id)                                                as nb_canteens_avec_mesure,
        sum(total_mass_kg)                                               as total_mass_kg,
        sum(total_meal_count)                                            as total_meal_count,
        count(case when niveau_ademe = 'Niveau 3'    then 1 end)        as nb_niveau_3,
        count(case when niveau_ademe = 'Niveau 2'    then 1 end)        as nb_niveau_2,
        count(case when niveau_ademe = 'Niveau 1'    then 1 end)        as nb_niveau_1,
        count(case when niveau_ademe = 'Non atteint' then 1 end)        as nb_non_atteint
    from by_canteen
    group by annee, line_ministry
),

by_groupe as (
    select
        annee,
        case
            when perimetre_key in ('ecologie', 'mer')                             then 'MTE'
            when perimetre_key in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre_key in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre_key in ('travail', 'sante')                            then 'Ministères sociaux'
            when perimetre_key in ('interieur', 'administration_territoriale')    then 'Périmètre intérieur'
        end                                                                        as perimetre_key,
        sum(nb_canteens_avec_mesure)                                               as nb_canteens_avec_mesure,
        sum(total_mass_kg)                                                         as total_mass_kg,
        sum(total_meal_count)                                                      as total_meal_count,
        sum(nb_niveau_3)                                                           as nb_niveau_3,
        sum(nb_niveau_2)                                                           as nb_niveau_2,
        sum(nb_niveau_1)                                                           as nb_niveau_1,
        sum(nb_non_atteint)                                                        as nb_non_atteint
    from by_line_ministry
    where perimetre_key in (
        'ecologie', 'mer',
        'jeunesse', 'enseignement_superieur', 'sport',
        'justice_hors_pjj', 'justice_pjj',
        'travail', 'sante',
        'interieur', 'administration_territoriale'
    )
    group by
        annee,
        case
            when perimetre_key in ('ecologie', 'mer')                             then 'MTE'
            when perimetre_key in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre_key in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre_key in ('travail', 'sante')                            then 'Ministères sociaux'
            when perimetre_key in ('interieur', 'administration_territoriale')    then 'Périmètre intérieur'
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
    nb_niveau_3,
    nb_niveau_2,
    nb_niveau_1,
    nb_non_atteint,

    -- g/couvert agrégé (total_mass est en kg → ×1000)
    round(
        (total_mass_kg * 1000 / nullif(total_meal_count, 0))::numeric, 1
    )                                                                    as gaspi_g_par_couvert

from all_perimetres
