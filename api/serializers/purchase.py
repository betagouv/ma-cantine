from rest_framework import serializers
from data.models import Purchase
from drf_base64.fields import Base64FileField


class PurchaseSerializer(serializers.ModelSerializer):

    canteen = serializers.PrimaryKeyRelatedField(read_only=True)
    invoice_file = Base64FileField(required=False, allow_null=True)
    price_ht = serializers.DecimalField(localize=True, max_digits=20, decimal_places=2)

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


class PurchaseSummarySerializer(serializers.Serializer):
    def dec_field():
        return serializers.DecimalField(max_digits=20, decimal_places=2, required=False)

    total = dec_field()
    bio = dec_field()
    sustainable = dec_field()
    hve = dec_field()
    aoc_aop_igp = dec_field()
    rouge = dec_field()
    # complex: by family and label
    viandes_volailles_bio = dec_field()
    produits_de_la_mer_bio = dec_field()
    fruits_et_legumes_bio = dec_field()
    charcuterie_bio = dec_field()
    produits_laitiers_bio = dec_field()
    boulangerie_bio = dec_field()
    boissons_bio = dec_field()
    autres_bio = dec_field()
    viandes_volailles_label_rouge = dec_field()
    produits_de_la_mer_label_rouge = dec_field()
    fruits_et_legumes_label_rouge = dec_field()
    charcuterie_label_rouge = dec_field()
    produits_laitiers_label_rouge = dec_field()
    boulangerie_label_rouge = dec_field()
    boissons_label_rouge = dec_field()
    autres_label_rouge = dec_field()
    viandes_volailles_aocaop_igp_stg = dec_field()
    produits_de_la_mer_aocaop_igp_stg = dec_field()
    fruits_et_legumes_aocaop_igp_stg = dec_field()
    charcuterie_aocaop_igp_stg = dec_field()
    produits_laitiers_aocaop_igp_stg = dec_field()
    boulangerie_aocaop_igp_stg = dec_field()
    boissons_aocaop_igp_stg = dec_field()
    autres_aocaop_igp_stg = dec_field()
    viandes_volailles_hve = dec_field()
    produits_de_la_mer_hve = dec_field()
    fruits_et_legumes_hve = dec_field()
    charcuterie_hve = dec_field()
    produits_laitiers_hve = dec_field()
    boulangerie_hve = dec_field()
    boissons_hve = dec_field()
    autres_hve = dec_field()
    viandes_volailles_peche_durable = dec_field()
    produits_de_la_mer_peche_durable = dec_field()
    fruits_et_legumes_peche_durable = dec_field()
    charcuterie_peche_durable = dec_field()
    produits_laitiers_peche_durable = dec_field()
    boulangerie_peche_durable = dec_field()
    boissons_peche_durable = dec_field()
    autres_peche_durable = dec_field()
    viandes_volailles_rup = dec_field()
    produits_de_la_mer_rup = dec_field()
    fruits_et_legumes_rup = dec_field()
    charcuterie_rup = dec_field()
    produits_laitiers_rup = dec_field()
    boulangerie_rup = dec_field()
    boissons_rup = dec_field()
    autres_rup = dec_field()
    viandes_volailles_fermier = dec_field()
    produits_de_la_mer_fermier = dec_field()
    fruits_et_legumes_fermier = dec_field()
    charcuterie_fermier = dec_field()
    produits_laitiers_fermier = dec_field()
    boulangerie_fermier = dec_field()
    boissons_fermier = dec_field()
    autres_fermier = dec_field()
    viandes_volailles_externalites = dec_field()
    produits_de_la_mer_externalites = dec_field()
    fruits_et_legumes_externalites = dec_field()
    charcuterie_externalites = dec_field()
    produits_laitiers_externalites = dec_field()
    boulangerie_externalites = dec_field()
    boissons_externalites = dec_field()
    autres_externalites = dec_field()
    viandes_volailles_commerce_equitable = dec_field()
    produits_de_la_mer_commerce_equitable = dec_field()
    fruits_et_legumes_commerce_equitable = dec_field()
    charcuterie_commerce_equitable = dec_field()
    produits_laitiers_commerce_equitable = dec_field()
    boulangerie_commerce_equitable = dec_field()
    boissons_commerce_equitable = dec_field()
    autres_commerce_equitable = dec_field()
    viandes_volailles_performance = dec_field()
    produits_de_la_mer_performance = dec_field()
    fruits_et_legumes_performance = dec_field()
    charcuterie_performance = dec_field()
    produits_laitiers_performance = dec_field()
    boulangerie_performance = dec_field()
    boissons_performance = dec_field()
    autres_performance = dec_field()
    viandes_volailles_france = dec_field()
    produits_de_la_mer_france = dec_field()
    fruits_et_legumes_france = dec_field()
    charcuterie_france = dec_field()
    produits_laitiers_france = dec_field()
    boulangerie_france = dec_field()
    boissons_france = dec_field()
    autres_france = dec_field()
    viandes_volailles_short_distribution = dec_field()
    produits_de_la_mer_short_distribution = dec_field()
    fruits_et_legumes_short_distribution = dec_field()
    charcuterie_short_distribution = dec_field()
    produits_laitiers_short_distribution = dec_field()
    boulangerie_short_distribution = dec_field()
    boissons_short_distribution = dec_field()
    autres_short_distribution = dec_field()
    viandes_volailles_local = dec_field()
    produits_de_la_mer_local = dec_field()
    fruits_et_legumes_local = dec_field()
    charcuterie_local = dec_field()
    produits_laitiers_local = dec_field()
    boulangerie_local = dec_field()
    boissons_local = dec_field()
    autres_local = dec_field()


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
