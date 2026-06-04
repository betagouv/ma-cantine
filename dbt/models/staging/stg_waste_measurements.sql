{{ config(materialized='table') }}

-- 1 ligne par (canteen_id, annee)
-- Année attribuée d'après period_start_date
-- Toutes les masses sont additionnées sur l'année civile

with source as (
    select * from {{ source('datawarehouse', 'waste_measurements_raw') }}
),

renamed as (
    select
        canteen_id,
        extract(year from period_start_date)::int          as annee,

        -- couverts
        sum(meal_count::numeric)                           as meal_count,

        -- masse totale
        sum(total_mass::numeric)                           as total_mass,

        -- préparation
        sum(preparation_total_mass::numeric)               as preparation_total_mass,
        sum(preparation_edible_mass::numeric)              as preparation_edible_mass,
        sum(preparation_inedible_mass::numeric)            as preparation_inedible_mass,

        -- non-servi
        sum(unserved_total_mass::numeric)                  as unserved_total_mass,
        sum(unserved_edible_mass::numeric)                 as unserved_edible_mass,
        sum(unserved_inedible_mass::numeric)               as unserved_inedible_mass,

        -- restes assiette
        sum(leftovers_total_mass::numeric)                 as leftovers_total_mass,
        sum(leftovers_edible_mass::numeric)                as leftovers_edible_mass,
        sum(leftovers_inedible_mass::numeric)              as leftovers_inedible_mass,

        -- nombre de mesures agrégées (utile pour la qualité des données)
        count(*)                                           as nb_mesures

    from source
    group by canteen_id, extract(year from period_start_date)::int
)

select * from renamed
