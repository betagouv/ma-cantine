from rest_framework import serializers
from data.models import Purchase
from drf_base64.fields import Base64FileField
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
            "created_by_import",
        )
        read_only_fields = (
            "id",
            "creation_date",
            "modification_date",
            "created_by_import",
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
    value_total_ht = PurchaseField()
    value_bio_ht = PurchaseField()
    value_sustainable_ht = PurchaseField()
    value_egalim_others_ht = PurchaseField()
    value_externality_performance_ht = PurchaseField()
    # meat and fish aggregates
    value_meat_poultry_ht = PurchaseField()
    value_meat_poultry_egalim_ht = PurchaseField()
    value_meat_poultry_france_ht = PurchaseField()
    value_fish_ht = PurchaseField()
    value_fish_egalim_ht = PurchaseField()
    # complex: by family and label
    value_viandes_volailles_bio = PurchaseField()
    value_produits_de_la_mer_bio = PurchaseField()
    value_fruits_et_legumes_bio = PurchaseField()
    value_charcuterie_bio = PurchaseField()
    value_produits_laitiers_bio = PurchaseField()
    value_boulangerie_bio = PurchaseField()
    value_boissons_bio = PurchaseField()
    value_autres_bio = PurchaseField()
    value_viandes_volailles_label_rouge = PurchaseField()
    value_produits_de_la_mer_label_rouge = PurchaseField()
    value_fruits_et_legumes_label_rouge = PurchaseField()
    value_charcuterie_label_rouge = PurchaseField()
    value_produits_laitiers_label_rouge = PurchaseField()
    value_boulangerie_label_rouge = PurchaseField()
    value_boissons_label_rouge = PurchaseField()
    value_autres_label_rouge = PurchaseField()
    value_viandes_volailles_aocaop_igp_stg = PurchaseField()
    value_produits_de_la_mer_aocaop_igp_stg = PurchaseField()
    value_fruits_et_legumes_aocaop_igp_stg = PurchaseField()
    value_charcuterie_aocaop_igp_stg = PurchaseField()
    value_produits_laitiers_aocaop_igp_stg = PurchaseField()
    value_boulangerie_aocaop_igp_stg = PurchaseField()
    value_boissons_aocaop_igp_stg = PurchaseField()
    value_autres_aocaop_igp_stg = PurchaseField()
    value_viandes_volailles_hve = PurchaseField()
    value_produits_de_la_mer_hve = PurchaseField()
    value_fruits_et_legumes_hve = PurchaseField()
    value_charcuterie_hve = PurchaseField()
    value_produits_laitiers_hve = PurchaseField()
    value_boulangerie_hve = PurchaseField()
    value_boissons_hve = PurchaseField()
    value_autres_hve = PurchaseField()
    value_viandes_volailles_peche_durable = PurchaseField()
    value_produits_de_la_mer_peche_durable = PurchaseField()
    value_fruits_et_legumes_peche_durable = PurchaseField()
    value_charcuterie_peche_durable = PurchaseField()
    value_produits_laitiers_peche_durable = PurchaseField()
    value_boulangerie_peche_durable = PurchaseField()
    value_boissons_peche_durable = PurchaseField()
    value_autres_peche_durable = PurchaseField()
    value_viandes_volailles_rup = PurchaseField()
    value_produits_de_la_mer_rup = PurchaseField()
    value_fruits_et_legumes_rup = PurchaseField()
    value_charcuterie_rup = PurchaseField()
    value_produits_laitiers_rup = PurchaseField()
    value_boulangerie_rup = PurchaseField()
    value_boissons_rup = PurchaseField()
    value_autres_rup = PurchaseField()
    value_viandes_volailles_fermier = PurchaseField()
    value_produits_de_la_mer_fermier = PurchaseField()
    value_fruits_et_legumes_fermier = PurchaseField()
    value_charcuterie_fermier = PurchaseField()
    value_produits_laitiers_fermier = PurchaseField()
    value_boulangerie_fermier = PurchaseField()
    value_boissons_fermier = PurchaseField()
    value_autres_fermier = PurchaseField()
    value_viandes_volailles_externalites = PurchaseField()
    value_produits_de_la_mer_externalites = PurchaseField()
    value_fruits_et_legumes_externalites = PurchaseField()
    value_charcuterie_externalites = PurchaseField()
    value_produits_laitiers_externalites = PurchaseField()
    value_boulangerie_externalites = PurchaseField()
    value_boissons_externalites = PurchaseField()
    value_autres_externalites = PurchaseField()
    value_viandes_volailles_commerce_equitable = PurchaseField()
    value_produits_de_la_mer_commerce_equitable = PurchaseField()
    value_fruits_et_legumes_commerce_equitable = PurchaseField()
    value_charcuterie_commerce_equitable = PurchaseField()
    value_produits_laitiers_commerce_equitable = PurchaseField()
    value_boulangerie_commerce_equitable = PurchaseField()
    value_boissons_commerce_equitable = PurchaseField()
    value_autres_commerce_equitable = PurchaseField()
    value_viandes_volailles_performance = PurchaseField()
    value_produits_de_la_mer_performance = PurchaseField()
    value_fruits_et_legumes_performance = PurchaseField()
    value_charcuterie_performance = PurchaseField()
    value_produits_laitiers_performance = PurchaseField()
    value_boulangerie_performance = PurchaseField()
    value_boissons_performance = PurchaseField()
    value_autres_performance = PurchaseField()
    value_viandes_volailles_france = PurchaseField()
    value_produits_de_la_mer_france = PurchaseField()
    value_fruits_et_legumes_france = PurchaseField()
    value_charcuterie_france = PurchaseField()
    value_produits_laitiers_france = PurchaseField()
    value_boulangerie_france = PurchaseField()
    value_boissons_france = PurchaseField()
    value_autres_france = PurchaseField()
    value_viandes_volailles_short_distribution = PurchaseField()
    value_produits_de_la_mer_short_distribution = PurchaseField()
    value_fruits_et_legumes_short_distribution = PurchaseField()
    value_charcuterie_short_distribution = PurchaseField()
    value_produits_laitiers_short_distribution = PurchaseField()
    value_boulangerie_short_distribution = PurchaseField()
    value_boissons_short_distribution = PurchaseField()
    value_autres_short_distribution = PurchaseField()
    value_viandes_volailles_local = PurchaseField()
    value_produits_de_la_mer_local = PurchaseField()
    value_fruits_et_legumes_local = PurchaseField()
    value_charcuterie_local = PurchaseField()
    value_produits_laitiers_local = PurchaseField()
    value_boulangerie_local = PurchaseField()
    value_boissons_local = PurchaseField()
    value_autres_local = PurchaseField()
    value_viandes_volailles_non_egalim = PurchaseField()
    value_produits_de_la_mer_non_egalim = PurchaseField()
    value_fruits_et_legumes_non_egalim = PurchaseField()
    value_charcuterie_non_egalim = PurchaseField()
    value_produits_laitiers_non_egalim = PurchaseField()
    value_boulangerie_non_egalim = PurchaseField()
    value_boissons_non_egalim = PurchaseField()
    value_autres_non_egalim = PurchaseField()


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
