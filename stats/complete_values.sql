with
starting_data as (
    select (value_bio_ht)/value_total_ht * 100 as p_bio, id
    from data_diagnostic
    where value_total_ht > 0
),
    td_2022
    as (
        SELECT * from data_teledeclaration
        where year = 2022 and status = 'SUBMITTED'
    ),
    td_simple_values
    as (
        SELECT
            id,
            canteen_id,
            CAST(declared_data -> 'teledeclaration' ->> 'value_total_ht' as float) as total,
            CAST(declared_data -> 'teledeclaration' ->> 'value_bio_ht' as float) as bio,
            CAST(declared_data -> 'teledeclaration' ->> 'value_sustainable_ht' as float) as sustainable,
            CAST(declared_data -> 'teledeclaration' ->> 'value_externality_performance_ht' as float) as externality,
            CAST(declared_data -> 'teledeclaration' ->> 'value_egalim_others_ht' as float) as other_egalim,
declared_data -> 'teledeclaration' ->> 'diagnostic_type' as diagnostic_type
        from td_2022
    ),
    no_null_bio
    as (
        SELECT * from td_simple_values
        where bio is not null
    ),
    some_non_null_egalim_hors_bio
    as (
        SELECT * from td_simple_values
        where sustainable is not null or externality is not null or other_egalim is not null
    ),
    sector_td_2022
    as (
        SELECT *
        from
            data_canteen_sectors
            left join data_sector on data_canteen_sectors.sector_id = data_sector.id
            left join td_simple_values on data_canteen_sectors.canteen_id = td_simple_values.canteen_id
        where
            td_simple_values.id is not null and
            bio is not null and
            (sustainable is not null or externality is not null or other_egalim is not null)
    ),
    td_raw_values
    as (
        SELECT *,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_total_ht' as float), 0) as total_ht,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_bio_ht' as float), 0) as bio_ht,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_sustainable_ht' as float), 0) as sustainable_ht,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_externality_performance_ht' as float), 0) as externality_performance_ht,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_egalim_others_ht' as float), 0) as egalim_others_ht,

            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_bio_ht' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_bio' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_bio' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_bio' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_bio' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_bio' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_bio' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_bio' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_bio' as float), 0) as bio,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_label_rouge' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_label_rouge' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_label_rouge' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_label_rouge' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_label_rouge' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_label_rouge' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_label_rouge' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_label_rouge' as float), 0) as label_rouge,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_aocaop_igp_stg' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_aocaop_igp_stg' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_aocaop_igp_stg' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_aocaop_igp_stg' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_aocaop_igp_stg' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_aocaop_igp_stg' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_aocaop_igp_stg' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_aocaop_igp_stg' as float), 0) as aocaop_igp_stg,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_hve' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_hve' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_hve' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_hve' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_hve' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_hve' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_hve' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_hve' as float), 0) as hve,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_peche_durable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_peche_durable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_peche_durable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_peche_durable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_peche_durable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_peche_durable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_peche_durable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_peche_durable' as float), 0) as peche_durable,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_rup' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_rup' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_rup' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_rup' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_rup' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_rup' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_rup' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_rup' as float), 0) as rup,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_fermier' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_fermier' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_fermier' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_fermier' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_fermier' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_fermier' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_fermier' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_fermier' as float), 0) as fermier,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_externalites' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_externalites' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_externalites' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_externalites' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_externalites' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_externalites' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_externalites' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_externalites' as float), 0) as externalites,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_commerce_equitable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_commerce_equitable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_commerce_equitable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_commerce_equitable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_commerce_equitable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_commerce_equitable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_commerce_equitable' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_commerce_equitable' as float), 0) as commerce_equitable,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_performance' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_performance' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_performance' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_performance' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_performance' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_performance' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_performance' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_performance' as float), 0) as performance,
            COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_viandes_volailles_non_egalim' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_de_la_mer_non_egalim' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_fruits_et_legumes_non_egalim' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_charcuterie_non_egalim' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_produits_laitiers_non_egalim' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boulangerie_non_egalim' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_boissons_non_egalim' as float), 0) +
                COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_non_egalim' as float), 0) as non_egalim
    ) from data_teledeclaration where year = 2022 and status = 'SUBMITTED'
