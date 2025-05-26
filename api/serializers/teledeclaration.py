from rest_framework import serializers

from data.models import Teledeclaration


class ShortTeledeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "status",
        )
        read_only_fields = fields


class TeledeclarationAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "declared_data",
            "creation_date",
            "modification_date",
            "year",
            "canteen_siret",
            "canteen_siren_unite_legale",
            "value_total_ht",
            "value_bio_ht_agg",
            "value_sustainable_ht_agg",
            "value_externality_performance_ht_agg",
            "value_egalim_others_ht_agg",
            "yearly_meal_count",
            "meal_price",
            "status",
            "applicant_id",
            "canteen_id",
            "diagnostic_id",
            "teledeclaration_mode",
        )
        read_only_fields = fields


class TeledeclarationOpenDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "declared_data",
            "creation_date",
            "modification_date",
            "year",
            "canteen_siret",
            "canteen_siren_unite_legale",
            "value_total_ht",
            "value_bio_ht_agg",
            "value_sustainable_ht_agg",
            "value_externality_performance_ht_agg",
            "value_egalim_others_ht_agg",
            "yearly_meal_count",
            "meal_price",
            "status",
            "applicant_id",
            "canteen_id",
            "diagnostic_id",
            "teledeclaration_mode",
        )
        read_only_fields = fields
