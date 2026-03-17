with source as (
    select * from {{ source('datawarehouse', 'diagnostics_raw') }}
),

renamed as (
    select
        id                                          as diagnostic_id,
        canteen_id,
        year,
        creation_date,
        modification_date,
        creation_source,
        diagnostic_type,
        central_kitchen_diagnostic_mode,
        status,
        teledeclaration_date,
        teledeclaration_mode,
        teledeclaration_version,
        teledeclaration_id,
        applicant_id,
        canteen_snapshot,
        satellites_snapshot,
        applicant_snapshot,

        -- ── APPRO ─────────────────────────────────────────────────────────────

        -- totaux globaux
        valeur_totale,
        valeur_bio,
        valeur_bio_dont_commerce_equitable,
        valeur_fair_trade,
        valeur_siqo,
        valeur_pat,
        valeur_externalites_performance,
        valeur_egalim_autres,
        valeur_egalim_autres_dont_commerce_equitable,

        -- totaux agrégés (cuisines centrales)
        valeur_bio_agg,
        valeur_siqo_agg,
        valeur_externalites_performance_agg,
        valeur_egalim_autres_agg,
        valeur_egalim_hors_bio_agg,
        valeur_egalim_agg,

        -- labels transversaux (diagnostic SIMPLE)
        valeur_label_rouge,
        valeur_label_aoc_igp,
        valeur_label_hve,

        -- par famille — totaux
        valeur_viandes_volailles,
        valeur_viandes_volailles_egalim,
        valeur_produits_de_la_mer,
        valeur_produits_de_la_mer_egalim,

        -- par famille — bio
        valeur_viandes_volailles_bio,
        valeur_viandes_volailles_bio_dont_commerce_equitable,
        valeur_produits_de_la_mer_bio,
        valeur_produits_de_la_mer_bio_dont_commerce_equitable,
        valeur_fruits_et_legumes_bio,
        valeur_fruits_et_legumes_bio_dont_commerce_equitable,
        valeur_charcuterie_bio,
        valeur_charcuterie_bio_dont_commerce_equitable,
        valeur_produits_laitiers_bio,
        valeur_produits_laitiers_bio_dont_commerce_equitable,
        valeur_boulangerie_bio,
        valeur_boulangerie_bio_dont_commerce_equitable,
        valeur_boissons_bio,
        valeur_boissons_bio_dont_commerce_equitable,
        valeur_autres_bio,
        valeur_autres_bio_dont_commerce_equitable,

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

        -- par famille — France
        valeur_viandes_volailles_france,
        valeur_produits_de_la_mer_france,
        valeur_fruits_et_legumes_france,
        valeur_charcuterie_france,
        valeur_produits_laitiers_france,
        valeur_boulangerie_france,
        valeur_boissons_france,
        valeur_autres_france,

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

        -- ── ANTI-GASPI ────────────────────────────────────────────────────────
        has_waste_diagnostic,
        has_waste_plan,
        waste_actions,
        other_waste_action,
        other_waste_comments,
        has_donation_agreement,
        has_waste_measures,
        total_leftovers,
        duration_leftovers_measurement,
        bread_leftovers,
        served_leftovers,
        unserved_leftovers,
        side_leftovers,
        donation_frequency,
        donation_quantity,
        donation_food_type,

        -- ── DIVERSIFICATION ───────────────────────────────────────────────────
        has_diversification_plan,
        diversification_plan_actions,
        service_type,
        vegetarian_weekly_recurrence,
        vegetarian_menu_type,
        vegetarian_menu_bases,

        -- ── PLASTIQUES ────────────────────────────────────────────────────────
        cooking_plastic_substituted,
        serving_plastic_substituted,
        plastic_bottles_substituted,
        plastic_tableware_substituted,

        -- ── INFORMATION ───────────────────────────────────────────────────────
        communication_supports,
        other_communication_support,
        communication_support_url,
        communicates_on_food_plan,
        communicates_on_food_quality,
        communication_frequency,

        -- campaign tracking
        creation_mtm_source,
        creation_mtm_campaign,
        creation_mtm_medium,

        -- ── RÉSULTATS CALCULÉS ────────────────────────────────────────────────
        pourcentage_bio,
        pourcentage_egalim,
        pourcentage_egalim_hors_bio,
        objectifs_egalim_atteints,
        invalid_reason_list,

        -- completion tunnels
        tunnel_appro,
        tunnel_waste,
        tunnel_diversification,
        tunnel_plastic,
        tunnel_info
        
    from source
)

select * from renamed