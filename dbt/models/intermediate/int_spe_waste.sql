{{ config(materialized='table') }}

-- Indicateurs gaspillage alimentaire par (perimetre_key, annee)
-- Source : stg_waste_measurements JOIN stg_teledeclarations (cantines ayant télédéclaré uniquement)
-- Inclut les périmètres line_ministry ET les sous-totaux groupe (UNION ALL)
-- Le niveau ADEME est calculé par cantine avant agrégation (évite les moyennes de ratios)

with waste as (
    select * from {{ ref('stg_waste_measurements') }}
),

-- Restreint aux cantines ayant effectivement télédéclaré pour l'année concernée
-- Applique les mêmes exclusions que les marts SPE (EPA en ATE, SIRETs exclus)
canteens as (
    select distinct
        canteen_id,
        line_ministry,
        year
    from {{ ref('stg_teledeclarations') }}
    where line_ministry is not null
      and line_ministry != ''
      and production_type not in ('groupe', 'central', 'central_serving')
      and teledeclaration_mode != 'SATELLITE_WITHOUT_APPRO'
      and (invalid_reason_list is null or invalid_reason_list::text = '[]')
      and (secteur != 'administration_etablissement_public' or line_ministry != 'administration_territoriale')
      and siret not in ('21400312100172', '26760171400087')
      and line_ministry != 'transformation'
),

-- Agrégation par cantine : une cantine peut avoir plusieurs mesures sur l'année
by_canteen as (
    select
        w.annee,
        c.line_ministry,
        w.canteen_id,
        sum(w.total_mass)                                               as total_mass_kg,
        sum(w.meal_count)                                               as total_meal_count,
        case
            when sum(w.meal_count) is null or sum(w.meal_count) = 0    then null
            when sum(w.total_mass) * 1000 / sum(w.meal_count) <= 47    then 'Niveau 3'
            when sum(w.total_mass) * 1000 / sum(w.meal_count) <= 74    then 'Niveau 2'
            when sum(w.total_mass) * 1000 / sum(w.meal_count) <= 95    then 'Niveau 1'
            else                                                             'Non atteint'
        end                                                             as niveau_ademe
    from waste w
    join canteens c on c.canteen_id = w.canteen_id and c.year = w.annee
    group by w.annee, c.line_ministry, w.canteen_id
    having
        sum(w.meal_count) > 0
        and (sum(w.total_mass) * 1000 / sum(w.meal_count)) >= 10
        and (sum(w.total_mass) * 1000 / sum(w.meal_count)) <= 500
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
