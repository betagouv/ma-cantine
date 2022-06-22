from rest_framework import serializers
from data.models import Diagnostic
from decimal import Decimal
from .teledeclaration import ShortTeledeclarationSerializer

FIELDS = (
    "id",
    "year",
    "value_bio_ht",
    "value_sustainable_ht",
    "value_pat_ht",
    "value_total_ht",
    "value_label_rouge",
    "value_label_aoc_igp",
    "value_label_hve",
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
    "viandes_volailles_bio",
    "produits_de_la_mer_bio",
    "fruits_et_legumes_bio",
    "charcuterie_bio",
    "produits_laitiers_bio",
    "boulangerie_bio",
    "boissons_bio",
    "autres_bio",
    "viandes_volailles_label_rouge",
    "produits_de_la_mer_label_rouge",
    "fruits_et_legumes_label_rouge",
    "charcuterie_label_rouge",
    "produits_laitiers_label_rouge",
    "boulangerie_label_rouge",
    "boissons_label_rouge",
    "autres_label_rouge",
    "viandes_volailles_aocaop_igp_stg",
    "produits_de_la_mer_aocaop_igp_stg",
    "fruits_et_legumes_aocaop_igp_stg",
    "charcuterie_aocaop_igp_stg",
    "produits_laitiers_aocaop_igp_stg",
    "boulangerie_aocaop_igp_stg",
    "boissons_aocaop_igp_stg",
    "autres_aocaop_igp_stg",
    "viandes_volailles_hve",
    "produits_de_la_mer_hve",
    "fruits_et_legumes_hve",
    "charcuterie_hve",
    "produits_laitiers_hve",
    "boulangerie_hve",
    "boissons_hve",
    "autres_hve",
    "viandes_volailles_peche_durable",
    "produits_de_la_mer_peche_durable",
    "fruits_et_legumes_peche_durable",
    "charcuterie_peche_durable",
    "produits_laitiers_peche_durable",
    "boulangerie_peche_durable",
    "boissons_peche_durable",
    "autres_peche_durable",
    "viandes_volailles_rup",
    "produits_de_la_mer_rup",
    "fruits_et_legumes_rup",
    "charcuterie_rup",
    "produits_laitiers_rup",
    "boulangerie_rup",
    "boissons_rup",
    "autres_rup",
    "viandes_volailles_fermier",
    "produits_de_la_mer_fermier",
    "fruits_et_legumes_fermier",
    "charcuterie_fermier",
    "produits_laitiers_fermier",
    "boulangerie_fermier",
    "boissons_fermier",
    "autres_fermier",
    "viandes_volailles_externalites",
    "produits_de_la_mer_externalites",
    "fruits_et_legumes_externalites",
    "charcuterie_externalites",
    "produits_laitiers_externalites",
    "boulangerie_externalites",
    "boissons_externalites",
    "autres_externalites",
    "viandes_volailles_commerce_equitable",
    "produits_de_la_mer_commerce_equitable",
    "fruits_et_legumes_commerce_equitable",
    "charcuterie_commerce_equitable",
    "produits_laitiers_commerce_equitable",
    "boulangerie_commerce_equitable",
    "boissons_commerce_equitable",
    "autres_commerce_equitable",
    "viandes_volailles_performance",
    "produits_de_la_mer_performance",
    "fruits_et_legumes_performance",
    "charcuterie_performance",
    "produits_laitiers_performance",
    "boulangerie_performance",
    "boissons_performance",
    "autres_performance",
    "viandes_volailles_equivalents",
    "produits_de_la_mer_equivalents",
    "fruits_et_legumes_equivalents",
    "charcuterie_equivalents",
    "produits_laitiers_equivalents",
    "boulangerie_equivalents",
    "boissons_equivalents",
    "autres_equivalents",
    "viandes_volailles_france",
    "produits_de_la_mer_france",
    "fruits_et_legumes_france",
    "charcuterie_france",
    "produits_laitiers_france",
    "boulangerie_france",
    "boissons_france",
    "autres_france",
    "viandes_volailles_short_distribution",
    "produits_de_la_mer_short_distribution",
    "fruits_et_legumes_short_distribution",
    "charcuterie_short_distribution",
    "produits_laitiers_short_distribution",
    "boulangerie_short_distribution",
    "boissons_short_distribution",
    "autres_short_distribution",
    "viandes_volailles_local",
    "produits_de_la_mer_local",
    "fruits_et_legumes_local",
    "charcuterie_local",
    "produits_laitiers_local",
    "boulangerie_local",
    "boissons_local",
    "autres_local",
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
            value_sum = (bio or 0) + (sustainable or 0)
            if value_sum > total:
                raise serializers.ValidationError(
                    f"La somme des valeurs d'approvisionnement, {value_sum}, est plus que le total, {total}"
                )
        return data

    @staticmethod
    def return_value(serializer, data, field_name):
        if field_name in data:
            return data.get(field_name)
        elif serializer.instance and getattr(serializer.instance, field_name):
            return getattr(serializer.instance, field_name)


class FullDiagnosticSerializer(serializers.ModelSerializer):

    teledeclaration = ShortTeledeclarationSerializer(source="latest_teledeclaration")

    class Meta:
        model = Diagnostic
        fields = FIELDS + ("teledeclaration",)
        read_only_fields = fields
