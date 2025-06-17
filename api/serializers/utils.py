def appro_to_percentages(representation, instance, remove_values=True):
    # first do the percentages relative to meat and fish totals
    # not removing these totals so that can then calculate the percent of those compared to global total
    meat_total = representation.get("value_meat_poultry_ht")
    if meat_total:
        field = "value_meat_poultry_egalim_ht"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / meat_total
        field = "value_meat_poultry_france_ht"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / meat_total

    fish_total = representation.get("value_fish_ht")
    if fish_total:
        field = "value_fish_egalim_ht"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / fish_total

    appro_field = (
        "value_total_ht",
        "value_bio_ht",
        "value_sustainable_ht",
        "value_externality_performance_ht",
        "value_egalim_others_ht",
    ) + COMPLETE_APPRO_FIELDS  # meat and fish totals included in COMPLETE
    total = representation.get("value_total_ht")

    for field in appro_field:
        new_field_name = f"percentage_{field}"
        if total and representation.get(field) is not None:
            representation[new_field_name] = representation[field] / total
        if remove_values:
            representation.pop(field, None)

    representation["percentage_value_total_ht"] = 1
    if remove_values:
        representation.pop("value_total_ht", None)
        representation.pop("value_meat_poultry_egalim_ht", None)
        representation.pop("value_meat_poultry_france_ht", None)
        representation.pop("value_fish_egalim_ht", None)

    return representation


COMPLETE_APPRO_FIELDS = (
    "value_total_ht",
    "value_meat_poultry_ht",
    "value_fish_ht",
    "value_viandes_volailles_bio",
    "value_produits_de_la_mer_bio",
    "value_fruits_et_legumes_bio",
    "value_charcuterie_bio",
    "value_produits_laitiers_bio",
    "value_boulangerie_bio",
    "value_boissons_bio",
    "value_autres_bio",
    "value_viandes_volailles_label_rouge",
    "value_produits_de_la_mer_label_rouge",
    "value_fruits_et_legumes_label_rouge",
    "value_charcuterie_label_rouge",
    "value_produits_laitiers_label_rouge",
    "value_boulangerie_label_rouge",
    "value_boissons_label_rouge",
    "value_autres_label_rouge",
    "value_viandes_volailles_aocaop_igp_stg",
    "value_produits_de_la_mer_aocaop_igp_stg",
    "value_fruits_et_legumes_aocaop_igp_stg",
    "value_charcuterie_aocaop_igp_stg",
    "value_produits_laitiers_aocaop_igp_stg",
    "value_boulangerie_aocaop_igp_stg",
    "value_boissons_aocaop_igp_stg",
    "value_autres_aocaop_igp_stg",
    "value_viandes_volailles_hve",
    "value_produits_de_la_mer_hve",
    "value_fruits_et_legumes_hve",
    "value_charcuterie_hve",
    "value_produits_laitiers_hve",
    "value_boulangerie_hve",
    "value_boissons_hve",
    "value_autres_hve",
    "value_viandes_volailles_peche_durable",
    "value_produits_de_la_mer_peche_durable",
    "value_fruits_et_legumes_peche_durable",
    "value_charcuterie_peche_durable",
    "value_produits_laitiers_peche_durable",
    "value_boulangerie_peche_durable",
    "value_boissons_peche_durable",
    "value_autres_peche_durable",
    "value_viandes_volailles_rup",
    "value_produits_de_la_mer_rup",
    "value_fruits_et_legumes_rup",
    "value_charcuterie_rup",
    "value_produits_laitiers_rup",
    "value_boulangerie_rup",
    "value_boissons_rup",
    "value_autres_rup",
    "value_viandes_volailles_fermier",
    "value_produits_de_la_mer_fermier",
    "value_fruits_et_legumes_fermier",
    "value_charcuterie_fermier",
    "value_produits_laitiers_fermier",
    "value_boulangerie_fermier",
    "value_boissons_fermier",
    "value_autres_fermier",
    "value_viandes_volailles_externalites",
    "value_produits_de_la_mer_externalites",
    "value_fruits_et_legumes_externalites",
    "value_charcuterie_externalites",
    "value_produits_laitiers_externalites",
    "value_boulangerie_externalites",
    "value_boissons_externalites",
    "value_autres_externalites",
    "value_viandes_volailles_commerce_equitable",
    "value_produits_de_la_mer_commerce_equitable",
    "value_fruits_et_legumes_commerce_equitable",
    "value_charcuterie_commerce_equitable",
    "value_produits_laitiers_commerce_equitable",
    "value_boulangerie_commerce_equitable",
    "value_boissons_commerce_equitable",
    "value_autres_commerce_equitable",
    "value_viandes_volailles_performance",
    "value_produits_de_la_mer_performance",
    "value_fruits_et_legumes_performance",
    "value_charcuterie_performance",
    "value_produits_laitiers_performance",
    "value_boulangerie_performance",
    "value_boissons_performance",
    "value_autres_performance",
    "value_viandes_volailles_non_egalim",
    "value_produits_de_la_mer_non_egalim",
    "value_fruits_et_legumes_non_egalim",
    "value_charcuterie_non_egalim",
    "value_produits_laitiers_non_egalim",
    "value_boulangerie_non_egalim",
    "value_boissons_non_egalim",
    "value_autres_non_egalim",
    "value_viandes_volailles_france",
    "value_produits_de_la_mer_france",
    "value_fruits_et_legumes_france",
    "value_charcuterie_france",
    "value_produits_laitiers_france",
    "value_boulangerie_france",
    "value_boissons_france",
    "value_autres_france",
    "value_viandes_volailles_short_distribution",
    "value_produits_de_la_mer_short_distribution",
    "value_fruits_et_legumes_short_distribution",
    "value_charcuterie_short_distribution",
    "value_produits_laitiers_short_distribution",
    "value_boulangerie_short_distribution",
    "value_boissons_short_distribution",
    "value_autres_short_distribution",
    "value_viandes_volailles_local",
    "value_produits_de_la_mer_local",
    "value_fruits_et_legumes_local",
    "value_charcuterie_local",
    "value_produits_laitiers_local",
    "value_boulangerie_local",
    "value_boissons_local",
    "value_autres_local",
)


def float_or_none(value):
    return float(value) if value else None
