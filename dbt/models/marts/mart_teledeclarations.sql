{{ config(materialized='table') }}

with teledeclarations as (
    select * from {{ ref('stg_teledeclarations') }}
)

select
    -- identifiers
    teledeclaration_id,
    canteen_id,
    year                                                as annee,
    teledeclaration_version                             as version,
    teledeclaration_date                                as date_teledeclaration,
    diagnostic_type,

    -- canteen info
    cantine_name                                        as cantine_nom,
    siret                                               as cantine_siret,
    siren_unite_legale                                  as cantine_siren_unite_legale,
    daily_meal_count                                    as cantine_nbre_repas_jour,
    yearly_meal_count                                   as cantine_nbre_repas_an,
    management_type                                     as cantine_type_gestion,
    production_type                                     as cantine_type_production,
    economic_model                                      as cantine_modele_economique,
    secteur                                             as cantine_secteur,
    categorie                                           as cantine_categorie,
    satellite_canteens_count                            as cantine_nbre_cantines_satellites,
    line_ministry                                       as cantine_ministere_tutelle,
    spe                                                 as cantine_spe,
    is_filled                                           as cantine_is_filled,
    genere_par_cuisine_centrale                         as cantine_genere_par_cuisine_centrale,

    -- geo
    department                                          as cantine_departement,
    department_lib                                      as cantine_lib_departement,
    region                                              as cantine_region,
    region_lib                                          as cantine_lib_region,
    city_insee_code                                     as cantine_code_insee_commune,
    nbre_cantines_region                                as cantine_nbre_cantines_region,
    objectif_zone_geo                                   as cantine_objectif_zone_geo,

    -- contact
    applicant_email                                     as email_gestionnaire,

    -- declarations history
    declaration_donnees_2021                            as cantine_declaration_donnees_2021,
    declaration_donnees_2022                            as cantine_declaration_donnees_2022,
    declaration_donnees_2023                            as cantine_declaration_donnees_2023,
    declaration_donnees_2024                            as cantine_declaration_donnees_2024,
    declaration_donnees_2025                            as cantine_declaration_donnees_2025,

    -- appro — valeurs
    valeur_totale,
    valeur_bio,
    valeur_egalim_agg                                   as valeur_egalim_avec_bio,
    valeur_egalim_hors_bio_agg                          as valeur_egalim_sans_bio,
    valeur_siqo,
    valeur_externalites_performance,
    valeur_egalim_autres,
    valeur_viandes_volailles,
    valeur_produits_de_la_mer,
    valeur_viandes_volailles_egalim,
    valeur_produits_de_la_mer_egalim,
    valeur_viandes_et_poissons,
    valeur_viandes_et_poissons_egalim,

    -- origine France (partiellement null jusqu'à migration vers diagnostics_raw)
    valeur_viandes_volailles_france,
    valeur_charcuterie_france,
    valeur_produits_de_la_mer_france,
    valeur_fruits_et_legumes_france,
    valeur_produits_laitiers_france,
    valeur_boulangerie_france,
    valeur_boissons_france,
    valeur_autres_france,

    -- ratios
    pourcentage_bio,
    pourcentage_egalim,
    pourcentage_egalim_hors_bio,
    ratio_viandes_volailles_egalim,
    ratio_produits_de_la_mer_egalim,
    objectifs_egalim_atteints,

    -- diversification
    service_type                                        as type_service,
    vegetarian_weekly_recurrence                        as recurrence_vege,
    vegetarian_menu_type                                as type_menu_vege,

    -- gaspillage
    has_waste_diagnostic                                as diag_gaspi,
    has_waste_plan                                      as plan_action_gaspi,
    action_gaspi_inscription,
    action_gaspi_sensibilisation,
    action_gaspi_formation,
    action_gaspi_distribution,
    action_gaspi_portions,
    action_gaspi_reutilisation

from teledeclarations
where valeur_totale is not null
  and valeur_bio is not null
  and production_type != 'groupe'
  and (invalid_reason_list is null or invalid_reason_list::text = '[]')
