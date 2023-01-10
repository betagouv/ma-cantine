from rest_framework import serializers
from data.models import Purchase
from drf_base64.fields import Base64FileField


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
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        if "canteen" not in validated_data:
            return super().create(validated_data)

        validated_data["canteen_id"] = validated_data.pop("canteen").id
        return super().create(validated_data)


class PurchaseField(serializers.DecimalField):
    def __init__(self):
        super().__init__(max_digits=20, decimal_places=2, required=False)


class PurchaseSummarySerializer(serializers.Serializer):
    total = PurchaseField()
    bio = PurchaseField()
    sustainable = PurchaseField()
    hve = PurchaseField()
    aoc_aop_igp = PurchaseField()
    rouge = PurchaseField()
    # meat and fish aggregates
    meat_poultry_total = PurchaseField()
    meat_poultry_egalim = PurchaseField()
    meat_poultry_france = PurchaseField()
    fish_total = PurchaseField()
    fish_egalim = PurchaseField()
    # complex: by family and label
    viandes_volailles_bio = PurchaseField()
    produits_de_la_mer_bio = PurchaseField()
    fruits_et_legumes_bio = PurchaseField()
    charcuterie_bio = PurchaseField()
    produits_laitiers_bio = PurchaseField()
    boulangerie_bio = PurchaseField()
    boissons_bio = PurchaseField()
    autres_bio = PurchaseField()
    viandes_volailles_label_rouge = PurchaseField()
    produits_de_la_mer_label_rouge = PurchaseField()
    fruits_et_legumes_label_rouge = PurchaseField()
    charcuterie_label_rouge = PurchaseField()
    produits_laitiers_label_rouge = PurchaseField()
    boulangerie_label_rouge = PurchaseField()
    boissons_label_rouge = PurchaseField()
    autres_label_rouge = PurchaseField()
    viandes_volailles_aocaop_igp_stg = PurchaseField()
    produits_de_la_mer_aocaop_igp_stg = PurchaseField()
    fruits_et_legumes_aocaop_igp_stg = PurchaseField()
    charcuterie_aocaop_igp_stg = PurchaseField()
    produits_laitiers_aocaop_igp_stg = PurchaseField()
    boulangerie_aocaop_igp_stg = PurchaseField()
    boissons_aocaop_igp_stg = PurchaseField()
    autres_aocaop_igp_stg = PurchaseField()
    viandes_volailles_hve = PurchaseField()
    produits_de_la_mer_hve = PurchaseField()
    fruits_et_legumes_hve = PurchaseField()
    charcuterie_hve = PurchaseField()
    produits_laitiers_hve = PurchaseField()
    boulangerie_hve = PurchaseField()
    boissons_hve = PurchaseField()
    autres_hve = PurchaseField()
    viandes_volailles_peche_durable = PurchaseField()
    produits_de_la_mer_peche_durable = PurchaseField()
    fruits_et_legumes_peche_durable = PurchaseField()
    charcuterie_peche_durable = PurchaseField()
    produits_laitiers_peche_durable = PurchaseField()
    boulangerie_peche_durable = PurchaseField()
    boissons_peche_durable = PurchaseField()
    autres_peche_durable = PurchaseField()
    viandes_volailles_rup = PurchaseField()
    produits_de_la_mer_rup = PurchaseField()
    fruits_et_legumes_rup = PurchaseField()
    charcuterie_rup = PurchaseField()
    produits_laitiers_rup = PurchaseField()
    boulangerie_rup = PurchaseField()
    boissons_rup = PurchaseField()
    autres_rup = PurchaseField()
    viandes_volailles_fermier = PurchaseField()
    produits_de_la_mer_fermier = PurchaseField()
    fruits_et_legumes_fermier = PurchaseField()
    charcuterie_fermier = PurchaseField()
    produits_laitiers_fermier = PurchaseField()
    boulangerie_fermier = PurchaseField()
    boissons_fermier = PurchaseField()
    autres_fermier = PurchaseField()
    viandes_volailles_externalites = PurchaseField()
    produits_de_la_mer_externalites = PurchaseField()
    fruits_et_legumes_externalites = PurchaseField()
    charcuterie_externalites = PurchaseField()
    produits_laitiers_externalites = PurchaseField()
    boulangerie_externalites = PurchaseField()
    boissons_externalites = PurchaseField()
    autres_externalites = PurchaseField()
    viandes_volailles_commerce_equitable = PurchaseField()
    produits_de_la_mer_commerce_equitable = PurchaseField()
    fruits_et_legumes_commerce_equitable = PurchaseField()
    charcuterie_commerce_equitable = PurchaseField()
    produits_laitiers_commerce_equitable = PurchaseField()
    boulangerie_commerce_equitable = PurchaseField()
    boissons_commerce_equitable = PurchaseField()
    autres_commerce_equitable = PurchaseField()
    viandes_volailles_performance = PurchaseField()
    produits_de_la_mer_performance = PurchaseField()
    fruits_et_legumes_performance = PurchaseField()
    charcuterie_performance = PurchaseField()
    produits_laitiers_performance = PurchaseField()
    boulangerie_performance = PurchaseField()
    boissons_performance = PurchaseField()
    autres_performance = PurchaseField()
    viandes_volailles_france = PurchaseField()
    produits_de_la_mer_france = PurchaseField()
    fruits_et_legumes_france = PurchaseField()
    charcuterie_france = PurchaseField()
    produits_laitiers_france = PurchaseField()
    boulangerie_france = PurchaseField()
    boissons_france = PurchaseField()
    autres_france = PurchaseField()
    viandes_volailles_short_distribution = PurchaseField()
    produits_de_la_mer_short_distribution = PurchaseField()
    fruits_et_legumes_short_distribution = PurchaseField()
    charcuterie_short_distribution = PurchaseField()
    produits_laitiers_short_distribution = PurchaseField()
    boulangerie_short_distribution = PurchaseField()
    boissons_short_distribution = PurchaseField()
    autres_short_distribution = PurchaseField()
    viandes_volailles_local = PurchaseField()
    produits_de_la_mer_local = PurchaseField()
    fruits_et_legumes_local = PurchaseField()
    charcuterie_local = PurchaseField()
    produits_laitiers_local = PurchaseField()
    boulangerie_local = PurchaseField()
    boissons_local = PurchaseField()
    autres_local = PurchaseField()
    viandes_volailles_non_egalim = PurchaseField()
    produits_de_la_mer_non_egalim = PurchaseField()
    fruits_et_legumes_non_egalim = PurchaseField()
    charcuterie_non_egalim = PurchaseField()
    produits_laitiers_non_egalim = PurchaseField()
    boulangerie_non_egalim = PurchaseField()
    boissons_non_egalim = PurchaseField()
    autres_non_egalim = PurchaseField()


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
