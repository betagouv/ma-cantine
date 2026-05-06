-- Source actuelle : diagnostics_raw (filtré sur les télédéclarations soumises)
-- Source précédente : table teledeclarations (export ETL manuel)
-- Seul ce fichier a été modifié lors du changement de source.
-- Les noms de colonnes exposés restent identiques → mart_teledeclarations inchangé.
-- Les infos cantine viennent du canteen_snapshot (JSON), pas d'une jointure.

with diagnostics as (
    select * from {{ ref('stg_diagnostics') }}
    where teledeclaration_id is not null
      and status = 'SUBMITTED'
),

renamed as (
    select
        -- identifiers
        teledeclaration_id,
        canteen_id,
        year,
        teledeclaration_version,
        creation_source,
        diagnostic_type,
        teledeclaration_mode,

        -- canteen info (extraite du canteen_snapshot JSON)
        canteen_snapshot::jsonb ->> 'name'                              as cantine_name,
        canteen_snapshot::jsonb ->> 'siret'                             as siret,
        canteen_snapshot::jsonb ->> 'siren_unite_legale'                as siren_unite_legale,
        (canteen_snapshot::jsonb ->> 'daily_meal_count')::float         as daily_meal_count,
        (canteen_snapshot::jsonb ->> 'yearly_meal_count')::float        as yearly_meal_count,
        canteen_snapshot::jsonb ->> 'management_type'                   as management_type,
        canteen_snapshot::jsonb ->> 'production_type'                   as production_type,
        canteen_snapshot::jsonb ->> 'economic_model'                    as economic_model,
        canteen_snapshot::jsonb ->> 'line_ministry'                     as line_ministry,
        (canteen_snapshot::jsonb ->> 'line_ministry') is not null       as spe,
        (canteen_snapshot::jsonb ->> 'is_filled')::boolean              as is_filled,
        (canteen_snapshot::jsonb ->> 'production_type') = 'central'     as genere_par_cuisine_centrale,

        -- secteur / catégorie (depuis sector_list dans le snapshot)
        case
            when jsonb_array_length(canteen_snapshot::jsonb -> 'sector_list') > 1 then 'Secteurs multiples'
            else (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1]
        end                                                             as secteur,
        case
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'administration%' then 'Administration'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'entreprise%'     then 'Entreprise'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'education%'      then 'Enseignement'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'sante%'          then 'Santé'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'social%'         then 'Social / Médico-social'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'loisir%'         then 'Loisirs'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] is not null            then 'Autres'
        end                                                             as categorie,

        -- satellites (depuis satellites_snapshot si disponible)
        case
            when satellites_snapshot is not null
            then jsonb_array_length(satellites_snapshot::jsonb)
        end                                                             as satellite_canteens_count,

        -- geo (department et region disponibles dans le snapshot, lib non disponibles sans jointure)
        canteen_snapshot::jsonb ->> 'department'                        as department,
        null::text                                                      as department_lib,
        canteen_snapshot::jsonb ->> 'region'                            as region,
        null::text                                                      as region_lib,
        canteen_snapshot::jsonb ->> 'city_insee_code'                   as city_insee_code,
        canteen_snapshot::jsonb ->> 'epci'                              as epci,
        canteen_snapshot::jsonb ->> 'epci_lib'                          as epci_lib,
        array_to_string(
            array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'pat_list')),
            ', '
        )                                                               as pat_list,
        null::integer                                                   as nbre_cantines_region,
        null::text                                                      as objectif_zone_geo,

        -- teledeclaration metadata
        creation_date,
        modification_date,
        teledeclaration_date,
        applicant_snapshot::jsonb ->> 'email'                           as applicant_email,

        -- declarations history (non disponible dans le snapshot)
        null::boolean                                                   as declaration_donnees_2021,
        null::boolean                                                   as declaration_donnees_2022,
        null::boolean                                                   as declaration_donnees_2023,
        null::boolean                                                   as declaration_donnees_2024,
        null::boolean                                                   as declaration_donnees_2025,

        -- appro — valeurs (cast text → float systématique)
        valeur_totale::float,
        valeur_bio::float,
        valeur_bio_dont_commerce_equitable::float,
        valeur_bio_agg::float,
        valeur_siqo_agg::float,
        valeur_externalites_performance_agg::float,
        valeur_egalim_autres_agg::float,
        valeur_egalim_autres_dont_commerce_equitable::float,
        valeur_egalim_agg::float,
        coalesce(valeur_bio::float, 0::float)
        + coalesce(valeur_siqo::float, 0::float)
        + coalesce(valeur_externalites_performance::float, 0::float)
        + coalesce(valeur_egalim_autres::float, 0::float)               as valeur_egalim_agg_v2,
        valeur_egalim_hors_bio_agg::float,
        valeur_siqo::float,
        valeur_externalites_performance::float,
        valeur_egalim_autres::float,
        valeur_viandes_volailles::float,
        valeur_produits_de_la_mer::float,
        valeur_viandes_volailles_egalim::float,
        valeur_produits_de_la_mer_egalim::float,
        coalesce(valeur_viandes_volailles::float, 0::float)
            + coalesce(valeur_produits_de_la_mer::float, 0::float)                   as valeur_viandes_et_poissons,
        coalesce(valeur_viandes_volailles_egalim::float, 0::float)
            + coalesce(valeur_produits_de_la_mer_egalim::float, 0::float)            as valeur_viandes_et_poissons_egalim,

        -- origine France
        coalesce(valeur_viandes_volailles_france::float, 0)
        + coalesce(valeur_charcuterie_france::float, 0)
        + coalesce(valeur_produits_de_la_mer_france::float, 0)
        + coalesce(valeur_fruits_et_legumes_france::float, 0)
        + coalesce(valeur_produits_laitiers_france::float, 0)
        + coalesce(valeur_boulangerie_france::float, 0)
        + coalesce(valeur_boissons_france::float, 0)
        + coalesce(valeur_autres_france::float, 0)                          as total_origine_france,
        valeur_viandes_volailles_france::float,
        valeur_charcuterie_france::float,
        valeur_produits_de_la_mer_france::float,
        valeur_fruits_et_legumes_france::float,
        valeur_produits_laitiers_france::float,
        valeur_boulangerie_france::float,
        valeur_boissons_france::float,
        valeur_autres_france::float,

        -- par famille — bio
        valeur_viandes_volailles_bio::float,
        valeur_produits_de_la_mer_bio::float,
        valeur_fruits_et_legumes_bio::float,
        valeur_charcuterie_bio::float,
        valeur_produits_laitiers_bio::float,
        valeur_boulangerie_bio::float,
        valeur_boissons_bio::float,
        valeur_autres_bio::float,

        -- par famille — label rouge
        valeur_viandes_volailles_label_rouge::float,
        valeur_produits_de_la_mer_label_rouge::float,
        valeur_fruits_et_legumes_label_rouge::float,
        valeur_charcuterie_label_rouge::float,
        valeur_produits_laitiers_label_rouge::float,
        valeur_boulangerie_label_rouge::float,
        valeur_boissons_label_rouge::float,
        valeur_autres_label_rouge::float,

        -- par famille — AOC/AOP/IGP/STG
        valeur_viandes_volailles_aocaop_igp_stg::float,
        valeur_produits_de_la_mer_aocaop_igp_stg::float,
        valeur_fruits_et_legumes_aocaop_igp_stg::float,
        valeur_charcuterie_aocaop_igp_stg::float,
        valeur_produits_laitiers_aocaop_igp_stg::float,
        valeur_boulangerie_aocaop_igp_stg::float,
        valeur_boissons_aocaop_igp_stg::float,
        valeur_autres_aocaop_igp_stg::float,

        -- par famille — HVE
        valeur_viandes_volailles_hve::float,
        valeur_produits_de_la_mer_hve::float,
        valeur_fruits_et_legumes_hve::float,
        valeur_charcuterie_hve::float,
        valeur_produits_laitiers_hve::float,
        valeur_boulangerie_hve::float,
        valeur_boissons_hve::float,
        valeur_autres_hve::float,

        -- par famille — pêche durable
        valeur_viandes_volailles_peche_durable::float,
        valeur_produits_de_la_mer_peche_durable::float,
        valeur_fruits_et_legumes_peche_durable::float,
        valeur_charcuterie_peche_durable::float,
        valeur_produits_laitiers_peche_durable::float,
        valeur_boulangerie_peche_durable::float,
        valeur_boissons_peche_durable::float,
        valeur_autres_peche_durable::float,

        -- par famille — RUP
        valeur_viandes_volailles_rup::float,
        valeur_produits_de_la_mer_rup::float,
        valeur_fruits_et_legumes_rup::float,
        valeur_charcuterie_rup::float,
        valeur_produits_laitiers_rup::float,
        valeur_boulangerie_rup::float,
        valeur_boissons_rup::float,
        valeur_autres_rup::float,

        -- par famille — commerce équitable
        valeur_viandes_volailles_commerce_equitable::float,
        valeur_produits_de_la_mer_commerce_equitable::float,
        valeur_fruits_et_legumes_commerce_equitable::float,
        valeur_charcuterie_commerce_equitable::float,
        valeur_produits_laitiers_commerce_equitable::float,
        valeur_boulangerie_commerce_equitable::float,
        valeur_boissons_commerce_equitable::float,
        valeur_autres_commerce_equitable::float,

        -- par famille — fermier
        valeur_viandes_volailles_fermier::float,
        valeur_produits_de_la_mer_fermier::float,
        valeur_fruits_et_legumes_fermier::float,
        valeur_charcuterie_fermier::float,
        valeur_produits_laitiers_fermier::float,
        valeur_boulangerie_fermier::float,
        valeur_boissons_fermier::float,
        valeur_autres_fermier::float,

        -- par famille — externalités
        valeur_viandes_volailles_externalites::float,
        valeur_produits_de_la_mer_externalites::float,
        valeur_fruits_et_legumes_externalites::float,
        valeur_charcuterie_externalites::float,
        valeur_produits_laitiers_externalites::float,
        valeur_boulangerie_externalites::float,
        valeur_boissons_externalites::float,
        valeur_autres_externalites::float,

        -- par famille — performance
        valeur_viandes_volailles_performance::float,
        valeur_produits_de_la_mer_performance::float,
        valeur_fruits_et_legumes_performance::float,
        valeur_charcuterie_performance::float,
        valeur_produits_laitiers_performance::float,
        valeur_boulangerie_performance::float,
        valeur_boissons_performance::float,
        valeur_autres_performance::float,

        -- par famille — non EGalim
        valeur_viandes_volailles_non_egalim::float,
        valeur_produits_de_la_mer_non_egalim::float,
        valeur_fruits_et_legumes_non_egalim::float,
        valeur_charcuterie_non_egalim::float,
        valeur_produits_laitiers_non_egalim::float,
        valeur_boulangerie_non_egalim::float,
        valeur_boissons_non_egalim::float,
        valeur_autres_non_egalim::float,

        -- par famille — circuit court
        valeur_viandes_volailles_circuit_court::float,
        valeur_produits_de_la_mer_circuit_court::float,
        valeur_fruits_et_legumes_circuit_court::float,
        valeur_charcuterie_circuit_court::float,
        valeur_produits_laitiers_circuit_court::float,
        valeur_boulangerie_circuit_court::float,
        valeur_boissons_circuit_court::float,
        valeur_autres_circuit_court::float,

        -- par famille — local
        valeur_viandes_volailles_local::float,
        valeur_produits_de_la_mer_local::float,
        valeur_fruits_et_legumes_local::float,
        valeur_charcuterie_local::float,
        valeur_produits_laitiers_local::float,
        valeur_boulangerie_local::float,
        valeur_boissons_local::float,
        valeur_autres_local::float,

        -- ratios (déjà calculés dans diagnostics_raw)
        pourcentage_bio::float,
        pourcentage_egalim::float,
        pourcentage_egalim_hors_bio::float,
        case
            when valeur_viandes_volailles::float > 0
            then valeur_viandes_volailles_egalim::float / valeur_viandes_volailles::float
        end                                                             as ratio_viandes_volailles_egalim,
        case
            when valeur_produits_de_la_mer::float > 0
            then valeur_produits_de_la_mer_egalim::float / valeur_produits_de_la_mer::float
        end                                                             as ratio_produits_de_la_mer_egalim,
        objectifs_egalim_atteints,

        -- diversification
        service_type,
        vegetarian_weekly_recurrence,
        vegetarian_menu_type,

        -- gaspillage
        has_waste_diagnostic,
        has_waste_plan,
        -- waste_actions est un array → extraction des actions individuelles par matching
        waste_actions::text ilike '%inscription%'                       as action_gaspi_inscription,
        waste_actions::text ilike '%sensibilisation%'                   as action_gaspi_sensibilisation,
        waste_actions::text ilike '%formation%'                         as action_gaspi_formation,
        waste_actions::text ilike '%distribution%'                      as action_gaspi_distribution,
        waste_actions::text ilike '%portions%'                          as action_gaspi_portions,
        waste_actions::text ilike '%reutilisation%'                     as action_gaspi_reutilisation,

        invalid_reason_list

    from diagnostics
)

select * from renamed
