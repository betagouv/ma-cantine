from drf_base64.fields import Base64FileField
from rest_framework import serializers

from data.models import Purchase

from .utils import appro_to_percentages


class PurchaseSerializer(serializers.ModelSerializer):
    canteen = serializers.PrimaryKeyRelatedField(read_only=True)
    invoice_file = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = Purchase
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "canteen",
            "date",
            "description",
            "provider",
            "family",
            "characteristics",
            "price_ht",
            "invoice_file",
            "local_definition",
            "import_source",
            "creation_source",
        )
        read_only_fields = (
            "id",
            "creation_date",
            "modification_date",
        )

    def create(self, validated_data):
        if "canteen" not in validated_data:
            return super().create(validated_data)

        validated_data["canteen_id"] = validated_data.pop("canteen").id
        return super().create(validated_data)


class PurchaseField(serializers.DecimalField):
    def __init__(self):
        super().__init__(max_digits=20, decimal_places=2, required=False)


# NB: these names reflect the names in the diagnostic model
class PurchaseSummarySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    valeur_totale = PurchaseField()
    valeur_bio = PurchaseField()
    valeur_bio_dont_commerce_equitable = PurchaseField()
    valeur_siqo = PurchaseField()
    valeur_egalim_autres = PurchaseField()
    valeur_egalim_autres_dont_commerce_equitable = PurchaseField()
    valeur_externalites_performance = PurchaseField()
    # meat and fish aggregates
    valeur_viandes_volailles = PurchaseField()
    valeur_viandes_volailles_egalim = PurchaseField()
    valeur_produits_de_la_mer = PurchaseField()
    valeur_produits_de_la_mer_egalim = PurchaseField()
    # complex: by family and label
    valeur_viandes_volailles_bio = PurchaseField()
    valeur_viandes_volailles_bio_dont_commerce_equitable = PurchaseField()
    valeur_produits_de_la_mer_bio = PurchaseField()
    valeur_produits_de_la_mer_bio_dont_commerce_equitable = PurchaseField()
    valeur_fruits_et_legumes_bio = PurchaseField()
    valeur_fruits_et_legumes_bio_dont_commerce_equitable = PurchaseField()
    valeur_charcuterie_bio = PurchaseField()
    valeur_charcuterie_bio_dont_commerce_equitable = PurchaseField()
    valeur_produits_laitiers_bio = PurchaseField()
    valeur_produits_laitiers_bio_dont_commerce_equitable = PurchaseField()
    valeur_boulangerie_bio = PurchaseField()
    valeur_boulangerie_bio_dont_commerce_equitable = PurchaseField()
    valeur_boissons_bio = PurchaseField()
    valeur_boissons_bio_dont_commerce_equitable = PurchaseField()
    valeur_autres_bio = PurchaseField()
    valeur_autres_bio_dont_commerce_equitable = PurchaseField()
    valeur_viandes_volailles_label_rouge = PurchaseField()
    valeur_produits_de_la_mer_label_rouge = PurchaseField()
    valeur_fruits_et_legumes_label_rouge = PurchaseField()
    valeur_charcuterie_label_rouge = PurchaseField()
    valeur_produits_laitiers_label_rouge = PurchaseField()
    valeur_boulangerie_label_rouge = PurchaseField()
    valeur_boissons_label_rouge = PurchaseField()
    valeur_autres_label_rouge = PurchaseField()
    valeur_viandes_volailles_aocaop_igp_stg = PurchaseField()
    valeur_produits_de_la_mer_aocaop_igp_stg = PurchaseField()
    valeur_fruits_et_legumes_aocaop_igp_stg = PurchaseField()
    valeur_charcuterie_aocaop_igp_stg = PurchaseField()
    valeur_produits_laitiers_aocaop_igp_stg = PurchaseField()
    valeur_boulangerie_aocaop_igp_stg = PurchaseField()
    valeur_boissons_aocaop_igp_stg = PurchaseField()
    valeur_autres_aocaop_igp_stg = PurchaseField()
    valeur_viandes_volailles_hve = PurchaseField()
    valeur_produits_de_la_mer_hve = PurchaseField()
    valeur_fruits_et_legumes_hve = PurchaseField()
    valeur_charcuterie_hve = PurchaseField()
    valeur_produits_laitiers_hve = PurchaseField()
    valeur_boulangerie_hve = PurchaseField()
    valeur_boissons_hve = PurchaseField()
    valeur_autres_hve = PurchaseField()
    valeur_viandes_volailles_peche_durable = PurchaseField()
    valeur_produits_de_la_mer_peche_durable = PurchaseField()
    valeur_fruits_et_legumes_peche_durable = PurchaseField()
    valeur_charcuterie_peche_durable = PurchaseField()
    valeur_produits_laitiers_peche_durable = PurchaseField()
    valeur_boulangerie_peche_durable = PurchaseField()
    valeur_boissons_peche_durable = PurchaseField()
    valeur_autres_peche_durable = PurchaseField()
    valeur_viandes_volailles_rup = PurchaseField()
    valeur_produits_de_la_mer_rup = PurchaseField()
    valeur_fruits_et_legumes_rup = PurchaseField()
    valeur_charcuterie_rup = PurchaseField()
    valeur_produits_laitiers_rup = PurchaseField()
    valeur_boulangerie_rup = PurchaseField()
    valeur_boissons_rup = PurchaseField()
    valeur_autres_rup = PurchaseField()
    valeur_viandes_volailles_commerce_equitable = PurchaseField()
    valeur_produits_de_la_mer_commerce_equitable = PurchaseField()
    valeur_fruits_et_legumes_commerce_equitable = PurchaseField()
    valeur_charcuterie_commerce_equitable = PurchaseField()
    valeur_produits_laitiers_commerce_equitable = PurchaseField()
    valeur_boulangerie_commerce_equitable = PurchaseField()
    valeur_boissons_commerce_equitable = PurchaseField()
    valeur_autres_commerce_equitable = PurchaseField()
    valeur_viandes_volailles_fermier = PurchaseField()
    valeur_produits_de_la_mer_fermier = PurchaseField()
    valeur_fruits_et_legumes_fermier = PurchaseField()
    valeur_charcuterie_fermier = PurchaseField()
    valeur_produits_laitiers_fermier = PurchaseField()
    valeur_boulangerie_fermier = PurchaseField()
    valeur_boissons_fermier = PurchaseField()
    valeur_autres_fermier = PurchaseField()
    valeur_viandes_volailles_externalites = PurchaseField()
    valeur_produits_de_la_mer_externalites = PurchaseField()
    valeur_fruits_et_legumes_externalites = PurchaseField()
    valeur_charcuterie_externalites = PurchaseField()
    valeur_produits_laitiers_externalites = PurchaseField()
    valeur_boulangerie_externalites = PurchaseField()
    valeur_boissons_externalites = PurchaseField()
    valeur_autres_externalites = PurchaseField()
    valeur_viandes_volailles_performance = PurchaseField()
    valeur_produits_de_la_mer_performance = PurchaseField()
    valeur_fruits_et_legumes_performance = PurchaseField()
    valeur_charcuterie_performance = PurchaseField()
    valeur_produits_laitiers_performance = PurchaseField()
    valeur_boulangerie_performance = PurchaseField()
    valeur_boissons_performance = PurchaseField()
    valeur_autres_performance = PurchaseField()
    valeur_viandes_volailles_non_egalim = PurchaseField()
    valeur_produits_de_la_mer_non_egalim = PurchaseField()
    valeur_fruits_et_legumes_non_egalim = PurchaseField()
    valeur_charcuterie_non_egalim = PurchaseField()
    valeur_produits_laitiers_non_egalim = PurchaseField()
    valeur_boulangerie_non_egalim = PurchaseField()
    valeur_boissons_non_egalim = PurchaseField()
    valeur_autres_non_egalim = PurchaseField()
    valeur_viandes_volailles_france = PurchaseField()
    valeur_produits_de_la_mer_france = PurchaseField()
    valeur_fruits_et_legumes_france = PurchaseField()
    valeur_charcuterie_france = PurchaseField()
    valeur_produits_laitiers_france = PurchaseField()
    valeur_boulangerie_france = PurchaseField()
    valeur_boissons_france = PurchaseField()
    valeur_autres_france = PurchaseField()
    valeur_viandes_volailles_circuit_court = PurchaseField()
    valeur_produits_de_la_mer_circuit_court = PurchaseField()
    valeur_fruits_et_legumes_circuit_court = PurchaseField()
    valeur_charcuterie_circuit_court = PurchaseField()
    valeur_produits_laitiers_circuit_court = PurchaseField()
    valeur_boulangerie_circuit_court = PurchaseField()
    valeur_boissons_circuit_court = PurchaseField()
    valeur_autres_circuit_court = PurchaseField()
    valeur_viandes_volailles_local = PurchaseField()
    valeur_produits_de_la_mer_local = PurchaseField()
    valeur_fruits_et_legumes_local = PurchaseField()
    valeur_charcuterie_local = PurchaseField()
    valeur_produits_laitiers_local = PurchaseField()
    valeur_boulangerie_local = PurchaseField()
    valeur_boissons_local = PurchaseField()
    valeur_autres_local = PurchaseField()


class PurchasePercentageSummarySerializer(PurchaseSummarySerializer):
    last_purchase_date = serializers.DateField(required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return appro_to_percentages(representation, instance)


class PurchaseExportSerializer(serializers.ModelSerializer):
    canteen = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Purchase
        fields = (
            "date",
            "canteen",
            "description",
            "provider",
            "readable_family",
            "readable_characteristics",
            "price_ht",
        )
        read_only_fields = fields
