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
),

canteens_spe as (
    select
        line_ministry                   as line_ministry_spe,
        creation_date
    from {{ ref('stg_canteens') }}
    where line_ministry is not null
      and line_ministry != ''
),

years as (
    select distinct year from teledeclarations
    where line_ministry is not null and line_ministry != ''
),

nb_cantines_inscrites as (
    select
        c.line_ministry_spe,
        y.year,
        count(*) as nb_cantines_inscrites
    from canteens_spe c
    cross join years y
    where c.creation_date <= make_date(y.year::int + 1, 4, 29)
    group by c.line_ministry_spe, y.year
)

select
    -- identifiers
    teledeclaration_id,
    canteen_id,
    teledeclarations.year                               as annee,
    teledeclaration_version                             as version,
    creation_date                                       as date_creation,
    modification_date                                   as date_modification,
    teledeclaration_date                                as date_teledeclaration,
    diagnostic_type,
    teledeclaration_mode,

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
    --satellite_canteens_count                            as cantine_nbre_cantines_satellites,
    line_ministry                                       as cantine_line_ministry,
    case
        when line_ministry in ('ecologie', 'mer')                             then 'MTE'
        when line_ministry in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
        when line_ministry in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
        when line_ministry in ('travail', 'sante')                            then 'Ministères sociaux'
        when line_ministry = 'autorites_independantes'                        then 'AAI'
        when line_ministry = 'administration_territoriale'                    then 'ATE'
        else line_ministry
    end                                                 as cantine_groupe_spe,
    is_filled                                           as cantine_is_filled,
    generated_from_groupe_diagnostic                    as cantine_generated_from_groupe_diagnostic,

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
    --valeur_bio,
    valeur_bio_dont_commerce_equitable,
    valeur_bio_agg,
    valeur_siqo_agg,
    valeur_externalites_performance_agg,
    valeur_egalim_autres_agg,
    valeur_egalim_autres_dont_commerce_equitable,
    valeur_egalim_agg,
    valeur_egalim_agg_v2,
    valeur_egalim_hors_bio_agg,
    valeur_siqo,
    valeur_externalites_performance,
    valeur_egalim_autres,
    valeur_viandes_volailles,
    valeur_produits_de_la_mer,
    valeur_viandes_volailles_egalim,
    valeur_produits_de_la_mer_egalim,
    valeur_viandes_et_poissons,
    valeur_viandes_et_poissons_egalim,

    -- origine France
    total_origine_france,
    valeur_viandes_volailles_france,
    valeur_charcuterie_france,
    valeur_produits_de_la_mer_france,
    valeur_fruits_et_legumes_france,
    valeur_produits_laitiers_france,
    valeur_boulangerie_france,
    valeur_boissons_france,
    valeur_autres_france,

    -- par famille — bio
    valeur_viandes_volailles_bio,
    valeur_produits_de_la_mer_bio,
    valeur_fruits_et_legumes_bio,
    valeur_charcuterie_bio,
    valeur_produits_laitiers_bio,
    valeur_boulangerie_bio,
    valeur_boissons_bio,
    valeur_autres_bio,

    -- par famille — label rouge
    valeur_viandes_volailles_label_rouge,
    valeur_produits_de_la_mer_label_rouge,
    valeur_fruits_et_legumes_label_rouge,
    valeur_charcuterie_label_rouge,
    valeur_produits_laitiers_label_rouge,
    valeur_boulangerie_label_rouge,
    valeur_boissons_label_rouge,
    valeur_autres_label_rouge,

    -- par famille — AOC/AOP/IGP/STG
    valeur_viandes_volailles_aocaop_igp_stg,
    valeur_produits_de_la_mer_aocaop_igp_stg,
    valeur_fruits_et_legumes_aocaop_igp_stg,
    valeur_charcuterie_aocaop_igp_stg,
    valeur_produits_laitiers_aocaop_igp_stg,
    valeur_boulangerie_aocaop_igp_stg,
    valeur_boissons_aocaop_igp_stg,
    valeur_autres_aocaop_igp_stg,

    -- par famille — HVE
    valeur_viandes_volailles_hve,
    valeur_produits_de_la_mer_hve,
    valeur_fruits_et_legumes_hve,
    valeur_charcuterie_hve,
    valeur_produits_laitiers_hve,
    valeur_boulangerie_hve,
    valeur_boissons_hve,
    valeur_autres_hve,

    -- par famille — pêche durable
    valeur_viandes_volailles_peche_durable,
    valeur_produits_de_la_mer_peche_durable,
    valeur_fruits_et_legumes_peche_durable,
    valeur_charcuterie_peche_durable,
    valeur_produits_laitiers_peche_durable,
    valeur_boulangerie_peche_durable,
    valeur_boissons_peche_durable,
    valeur_autres_peche_durable,

    -- par famille — RUP
    valeur_viandes_volailles_rup,
    valeur_produits_de_la_mer_rup,
    valeur_fruits_et_legumes_rup,
    valeur_charcuterie_rup,
    valeur_produits_laitiers_rup,
    valeur_boulangerie_rup,
    valeur_boissons_rup,
    valeur_autres_rup,

    -- par famille — commerce équitable
    valeur_viandes_volailles_commerce_equitable,
    valeur_produits_de_la_mer_commerce_equitable,
    valeur_fruits_et_legumes_commerce_equitable,
    valeur_charcuterie_commerce_equitable,
    valeur_produits_laitiers_commerce_equitable,
    valeur_boulangerie_commerce_equitable,
    valeur_boissons_commerce_equitable,
    valeur_autres_commerce_equitable,

    -- par famille — fermier
    valeur_viandes_volailles_fermier,
    valeur_produits_de_la_mer_fermier,
    valeur_fruits_et_legumes_fermier,
    valeur_charcuterie_fermier,
    valeur_produits_laitiers_fermier,
    valeur_boulangerie_fermier,
    valeur_boissons_fermier,
    valeur_autres_fermier,

    -- par famille — externalités
    valeur_viandes_volailles_externalites,
    valeur_produits_de_la_mer_externalites,
    valeur_fruits_et_legumes_externalites,
    valeur_charcuterie_externalites,
    valeur_produits_laitiers_externalites,
    valeur_boulangerie_externalites,
    valeur_boissons_externalites,
    valeur_autres_externalites,

    -- par famille — performance
    valeur_viandes_volailles_performance,
    valeur_produits_de_la_mer_performance,
    valeur_fruits_et_legumes_performance,
    valeur_charcuterie_performance,
    valeur_produits_laitiers_performance,
    valeur_boulangerie_performance,
    valeur_boissons_performance,
    valeur_autres_performance,

    -- par famille — non EGalim
    valeur_viandes_volailles_non_egalim,
    valeur_produits_de_la_mer_non_egalim,
    valeur_fruits_et_legumes_non_egalim,
    valeur_charcuterie_non_egalim,
    valeur_produits_laitiers_non_egalim,
    valeur_boulangerie_non_egalim,
    valeur_boissons_non_egalim,
    valeur_autres_non_egalim,

    -- par famille — circuit court
    valeur_viandes_volailles_circuit_court,
    valeur_produits_de_la_mer_circuit_court,
    valeur_fruits_et_legumes_circuit_court,
    valeur_charcuterie_circuit_court,
    valeur_produits_laitiers_circuit_court,
    valeur_boulangerie_circuit_court,
    valeur_boissons_circuit_court,
    valeur_autres_circuit_court,

    -- par famille — local
    valeur_viandes_volailles_local,
    valeur_produits_de_la_mer_local,
    valeur_fruits_et_legumes_local,
    valeur_charcuterie_local,
    valeur_produits_laitiers_local,
    valeur_boulangerie_local,
    valeur_boissons_local,
    valeur_autres_local,

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
    action_gaspi_reutilisation,

    -- tunnels de complétion
    tunnel_appro,
    tunnel_waste,
    tunnel_diversification,
    tunnel_plastic,
    tunnel_info,

    -- stats annuelles
    count(*) filter (where teledeclarations.year = 2025) over ()    as nb_teledeclarations_2025,

    -- SPE — dénominateur figé au 29 avril (utiliser MAX lors des agrégations Metabase)
    coalesce(nb_cantines_inscrites.nb_cantines_inscrites, 0)                as nb_cantines_inscrites_spe,

    -- SPE — objectifs EGalim (booléens : SUM = nb cantines atteignant l'objectif)
    (valeur_bio_agg / nullif(valeur_totale, 0) >= 0.20)                    as atteint_bio,
    (valeur_egalim_agg / nullif(valeur_totale, 0) >= 0.50)                 as atteint_egalim,
    (valeur_bio_agg / nullif(valeur_totale, 0) >= 0.20
        and valeur_egalim_agg / nullif(valeur_totale, 0) >= 0.50)          as atteint_bio_et_egalim,
    (valeur_viandes_et_poissons > 0
        and valeur_viandes_et_poissons_egalim
            / nullif(valeur_viandes_et_poissons, 0) >= 1.0)                as atteint_viandes_et_poissons_egalim,
    (valeur_bio_agg / nullif(valeur_totale, 0) >= 0.20
        and valeur_egalim_agg / nullif(valeur_totale, 0) >= 0.50
        and valeur_viandes_et_poissons > 0
        and valeur_viandes_et_poissons_egalim
            / nullif(valeur_viandes_et_poissons, 0) >= 1.0)                as atteint_3_objectifs,

    -- SPE — objectif végétarien
    (service_type != 'UNIQUE')                                             as choix_multiple,
    (service_type != 'UNIQUE'
        and vegetarian_weekly_recurrence = 'DAILY')                        as atteint_vege_quotidien,

    -- SPE — volet diversification protéines / menu végé rempli
    (tunnel_diversification = 'complet')                                   as td_volet_diversification_complet

from teledeclarations
left join ref_departements on ref_departements.code_departement = teledeclarations.department
left join ref_regions on ref_regions.code_region = teledeclarations.region
left join ref_epci on ref_epci.code_epci = teledeclarations.epci
left join ref_communes on ref_communes.code_insee_commune = teledeclarations.city_insee_code
left join nb_cantines_inscrites
    on nb_cantines_inscrites.line_ministry_spe = teledeclarations.line_ministry
    and nb_cantines_inscrites.year = teledeclarations.year
where 1=1
  and production_type != 'groupe'
  and teledeclaration_mode != 'SATELLITE_WITHOUT_APPRO'
  and (invalid_reason_list is null or invalid_reason_list::text = '[]')
