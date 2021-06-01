from rest_framework import serializers
from data.models import Canteen, Sector
from .diagnosis import DiagnosisSerializer


class PublicCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    diagnosis = DiagnosisSerializer(many=True, read_only=True, source="diagnosis_set")

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "diagnosis",
            "city",
            "postal_code",
            "sectors",
            "daily_meal_count",
        )


class FullCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Sector.objects.all()
    )
    diagnosis = DiagnosisSerializer(many=True, read_only=True, source="diagnosis_set")

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "city",
            "postal_code",
            "sectors",
            "published",
            "data_is_public",
            "daily_meal_count",
            "siret",
            "management_type",
            "diagnosis",
        )
