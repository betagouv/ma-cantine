from drf_base64.fields import Base64FileField
from rest_framework import serializers

from api.serializers.utils import PurchaseField, choice_list_to_choices
from data.models import Purchase


class PurchaseOldSerializer(serializers.ModelSerializer):
    canteen = serializers.PrimaryKeyRelatedField(read_only=True)
    provider = serializers.CharField(source="fournisseur", required=False, allow_blank=True)
    family = serializers.ChoiceField(
        source="famille_produits", choices=Purchase.Family.choices, required=False, allow_blank=True
    )
    characteristics = serializers.MultipleChoiceField(
        source="caracteristiques", choices=Purchase.Characteristic.choices, required=False, allow_blank=True
    )
    price_ht = serializers.DecimalField(source="prix_ht", max_digits=20, decimal_places=2, required=False)
    invoice_file = Base64FileField(source="facture", required=False, allow_null=True)
    local_definition = serializers.ChoiceField(
        source="definition_local", choices=Purchase.Local.choices, required=False, allow_blank=True
    )

    class Meta:
        model = Purchase
        fields = (
            "id",
            "canteen",
            "date",
            "description",
            # TODO: update once we finish the translation to French
            "provider",  # "fournisseur",
            "family",  # "famille_produits",
            "characteristics",  # "caracteristiques",
            "price_ht",  # "prix_ht",
            "invoice_file",  # "facture",
            "local_definition",  # "definition_local",
            "import_source",
            "creation_source",
            "creation_date",
            "modification_date",
        )
        read_only_fields = (
            "id",
            "creation_date",
            "modification_date",
        )

    # TODO: remove once we finish the translation to French
    @staticmethod
    def _normalize_characteristics(validated_data):
        characteristics = validated_data.get("caracteristiques")
        if isinstance(characteristics, set):
            ordered_characteristics = [choice for choice, _label in Purchase.Characteristic.choices]
            validated_data["caracteristiques"] = [
                choice for choice in ordered_characteristics if choice in characteristics
            ]

    def create(self, validated_data):
        self._normalize_characteristics(validated_data)

        if "canteen" not in validated_data:
            return super().create(validated_data)

        validated_data["canteen_id"] = validated_data.pop("canteen").id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._normalize_characteristics(validated_data)
        return super().update(instance, validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    canteen = serializers.PrimaryKeyRelatedField(read_only=True)
    # caracteristiques is split into 4 fields
    categories_egalim = serializers.MultipleChoiceField(
        choices=choice_list_to_choices(Purchase.CHARACTERISTIC_LABELS_EGALIM)
    )
    origine = serializers.ChoiceField(
        choices=choice_list_to_choices(Purchase.CHARACTERISTIC_LABELS_ORIGINE),
        required=False,
    )
    est_local = serializers.BooleanField(required=False)
    est_circuit_court = serializers.BooleanField(required=False)
    creation_source = serializers.CharField(read_only=True)
    import_source = serializers.CharField(read_only=True)
    creation_date = serializers.DateTimeField(read_only=True)
    modification_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Purchase
        fields = (
            "id",
            "canteen",
            "description",
            "fournisseur",
            "date",
            "prix_ht",
            "famille_produits",
            "categories_egalim",
            "origine",
            "est_local",
            "est_circuit_court",
            "definition_local",
            # "facture",
            "creation_source",
            "import_source",
            "creation_date",
            "modification_date",
        )

    def to_representation(self, instance):
        """
        Useful for read operations (returning data)
        """
        representation = super().to_representation(instance)
        representation["categories_egalim"] = [
            characteristic
            for characteristic in (instance.caracteristiques or [])
            if characteristic in Purchase.CHARACTERISTIC_LABELS_EGALIM
        ]
        representation["origine"] = next(
            (
                characteristic
                for characteristic in (instance.caracteristiques or [])
                if characteristic in Purchase.CHARACTERISTIC_LABELS_ORIGINE
            ),
            "",
        )
        representation["est_local"] = any(
            characteristic == Purchase.Characteristic.LOCAL for characteristic in (instance.caracteristiques or [])
        )
        representation["est_circuit_court"] = any(
            characteristic == Purchase.Characteristic.CIRCUIT_COURT
            for characteristic in (instance.caracteristiques or [])
        )
        return representation

    def to_internal_value(self, data):
        """
        Useful for write operations (creating/updating data)
        """
        internal_value = super().to_internal_value(data)

        caracteristiques = []

        caracteristiques.extend(internal_value.pop("categories_egalim", []))

        origine = internal_value.pop("origine", "")
        if origine:
            caracteristiques.append(origine)

        if internal_value.pop("est_local", False):
            caracteristiques.append(Purchase.Characteristic.LOCAL)

        if internal_value.pop("est_circuit_court", False):
            caracteristiques.append(Purchase.Characteristic.CIRCUIT_COURT)

        internal_value["caracteristiques"] = caracteristiques
        return internal_value


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


# NB: these names reflect the names in the diagnostic model
class PurchasePercentageSummarySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    percentage_valeur_totale = serializers.FloatField(required=False)
    percentage_valeur_bio = serializers.FloatField(required=False)
    percentage_valeur_siqo = serializers.FloatField(required=False)
    percentage_valeur_externalites_performance = serializers.FloatField(required=False)
    percentage_valeur_egalim_autres = serializers.FloatField(required=False)
    percentage_valeur_viandes_volailles_egalim = serializers.FloatField(required=False)
    percentage_valeur_viandes_volailles_france = serializers.FloatField(required=False)
    percentage_valeur_produits_de_la_mer_egalim = serializers.FloatField(required=False)
    percentage_valeur_produits_de_la_mer_france = serializers.FloatField(required=False)
    last_purchase_date = serializers.DateField(required=False)


class PurchaseExportSerializer(serializers.ModelSerializer):
    canteen = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Purchase
        fields = (
            "date",
            "canteen",
            "description",
            "fournisseur",
            "famille_produits_display",
            "caracteristiques_display",
            "prix_ht",
        )
        read_only_fields = fields
