{{ config(materialized='table') }}

-- 1 ligne par (canteen_id, annee) ayant au moins une mesure de gaspillage
-- Données de masse issues de stg_waste_measurements (déjà agrégées par année civile)
-- Niveau ADEME calculé sur la base du ratio total_mass / meal_count agrégé

with waste as (
    select * from {{ ref('stg_waste_measurements') }}
),

canteens as (
    select
        canteen_id,
        siret,
        cantine_name,
        line_ministry,
        management_type,
        production_type,
        daily_meal_count,
        yearly_meal_count,
        sector_list,
        department,
        department_lib,
        region,
        region_lib,
        epci,
        epci_lib
    from {{ ref('stg_canteens') }}
)

select
    w.canteen_id,
    w.annee,
    c.siret,
    c.cantine_name,
    c.line_ministry,
    c.management_type,
    c.production_type,
    c.daily_meal_count,
    c.yearly_meal_count,
    c.sector_list,
    c.department,
    c.department_lib,
    c.region,
    c.region_lib,
    c.epci,
    c.epci_lib,

    -- mesures
    w.nb_mesures,
    w.meal_count                                                        as total_meal_count,
    w.total_mass                                                        as total_mass_kg,

    -- détail par flux
    w.preparation_total_mass,
    w.preparation_edible_mass,
    w.preparation_inedible_mass,
    w.unserved_total_mass,
    w.unserved_edible_mass,
    w.unserved_inedible_mass,
    w.leftovers_total_mass,
    w.leftovers_edible_mass,
    w.leftovers_inedible_mass,

    -- ratio agrégé (g/couvert)
    round(
        (w.total_mass * 1000 / nullif(w.meal_count, 0))::numeric, 1
    )                                                                   as gaspi_g_par_couvert,

    -- niveau ADEME selon barème 47 / 74 / 95 g/couvert
    case
        when w.meal_count is null or w.meal_count = 0                  then null
        when w.total_mass * 1000 / w.meal_count <= 47                  then 'Niveau 3'
        when w.total_mass * 1000 / w.meal_count <= 74                  then 'Niveau 2'
        when w.total_mass * 1000 / w.meal_count <= 95                  then 'Niveau 1'
        else                                                                 'Non atteint'
    end                                                                 as niveau_ademe

from waste w
left join canteens c on c.canteen_id = w.canteen_id
where w.meal_count > 0
  and (w.total_mass * 1000 / w.meal_count) between 10 and 500
