SELECT
    COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_total_ht' as float), 0) as total_ht,

    COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_sustainable_ht' as float), 0) as sustainable_ht,
    COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_externality_performance_ht' as float), 0) as externality_performance_ht,
    COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_egalim_others_ht' as float), 0) as egalim_others_ht,

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
        COALESCE(CAST(declared_data -> 'teledeclaration' ->> 'value_autres_performance' as float), 0) as performance
