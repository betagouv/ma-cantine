{{ config(materialized='table') }}

with teledeclarations as (
    select * from {{ ref('stg_teledeclarations') }}
),

ref_departements as (
    select * from {{ ref('ref_departements') }}
),

ref_regions as (
    select * from {{ ref('ref_regions') }}
),

ref_epci as (
    select * from {{ ref('ref_epci') }}
),

ref_communes as (
    select * from {{ ref('ref_communes') }}
),

ref_pats as (
    select * from {{ ref('ref_pats') }}
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
    teledeclarations.department                         as cantine_departement,
    ref_departements.lib_departement                    as cantine_lib_departement,
    teledeclarations.region                             as cantine_region,
    ref_regions.lib_region                              as cantine_lib_region,
    teledeclarations.city_insee_code                    as cantine_code_insee_commune,
    ref_communes.lib_commune                            as cantine_lib_commune,
    teledeclarations.epci                               as cantine_epci,
    coalesce(ref_epci.lib_epci, teledeclarations.epci_lib) as cantine_lib_epci,
    teledeclarations.pat_list                           as cantine_pat_liste,
    -- libellés PAT reconstruits depuis ref_pats (pat_lib_list absent du snapshot)
    (
        select string_agg(rp.lib_pat, ', ' order by rp.lib_pat)
        from regexp_split_to_table(teledeclarations.pat_list, ', ') as p(code_pat)
        join ref_pats rp on rp.code_pat = p.code_pat
    )                                                   as cantine_pat_lib_liste,
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
left join ref_departements on ref_departements.code_departement = teledeclarations.department
left join ref_regions on ref_regions.code_region = teledeclarations.region
left join ref_epci on ref_epci.code_epci = teledeclarations.epci
left join ref_communes on ref_communes.code_insee_commune = teledeclarations.city_insee_code
where valeur_totale is not null
  and valeur_bio is not null
  and production_type != 'groupe'
  and (invalid_reason_list is null or invalid_reason_list::text = '[]')
