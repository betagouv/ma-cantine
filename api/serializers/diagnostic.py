from rest_framework import serializers
from data.models import Diagnostic
from decimal import Decimal
from .teledeclaration import ShortTeledeclarationSerializer

FIELDS = (
    "id",
    "year",
    "diagnostic_type",
    "value_bio_ht",
    "value_sustainable_ht",
    "value_pat_ht",
    "value_total_ht",
    "value_label_rouge",
    "value_label_aoc_igp",
    "value_label_hve",
    "value_externality_performance_ht",
    "value_egalim_others_ht",
    "value_meat_poultry_ht",
    "value_meat_poultry_egalim_ht",
    "value_meat_poultry_france_ht",
    "value_fish_ht",
    "value_fish_egalim_ht",
    "has_waste_diagnostic",
    "has_waste_plan",
    "waste_actions",
    "other_waste_action",
    "has_donation_agreement",
    "has_waste_measures",
    "bread_leftovers",
    "served_leftovers",
    "unserved_leftovers",
    "side_leftovers",
    "donation_frequency",
    "donation_quantity",
    "donation_food_type",
    "other_waste_comments",
    "has_diversification_plan",
    "diversification_plan_actions",
    "vegetarian_weekly_recurrence",
    "vegetarian_menu_type",
    "vegetarian_menu_bases",
    "cooking_plastic_substituted",
    "serving_plastic_substituted",
    "plastic_bottles_substituted",
    "plastic_tableware_substituted",
    "communication_supports",
    "other_communication_support",
    "communication_support_url",
    "communicates_on_food_plan",
    "communicates_on_food_quality",
    "communication_frequency",
    "creation_date",
    "modification_date",
    # detailed value fields
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


class PublicDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        read_only_fields = ("id",)
        fields = FIELDS + (
            "creation_mtm_source",
            "creation_mtm_campaign",
            "creation_mtm_medium",
        )

    def __init__(self, *args, **kwargs):
        action = kwargs.pop("action", None)
        super().__init__(*args, **kwargs)
        if action != "create":
            self.fields.pop("creation_mtm_source")
            self.fields.pop("creation_mtm_campaign")
            self.fields.pop("creation_mtm_medium")

    def validate(self, data):
        total = self.return_value(self, data, "value_total_ht")
        if total is not None and isinstance(total, Decimal):
            bio = self.return_value(self, data, "value_bio_ht")
            sustainable = self.return_value(self, data, "value_sustainable_ht")
            externality_performance = self.return_value(self, data, "value_externality_performance_ht")
            egalim_others = self.return_value(self, data, "value_egalim_others_ht")
            value_sum = (bio or 0) + (sustainable or 0) + (externality_performance or 0) + (egalim_others or 0)
            if value_sum > total:
                raise serializers.ValidationError(
                    f"La somme des valeurs d'approvisionnement, {value_sum}, est plus que le total, {total}"
                )
            # TODO: test meat and fish too?
        return data

    @staticmethod
    def return_value(serializer, data, field_name):
        if field_name in data:
            return data.get(field_name)
        elif serializer.instance and getattr(serializer.instance, field_name):
            return getattr(serializer.instance, field_name)


class FullDiagnosticSerializer(serializers.ModelSerializer):

    teledeclaration = ShortTeledeclarationSerializer(source="latest_submitted_teledeclaration")

    class Meta:
        model = Diagnostic
        fields = FIELDS + ("teledeclaration",)
        read_only_fields = fields
