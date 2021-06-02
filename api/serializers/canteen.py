from rest_framework import serializers
from data.models import Canteen, Sector
from .diagnostic import DiagnosticSerializer


class PublicCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    diagnostics = DiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "diagnostics",
            "city",
            "postal_code",
            "sectors",
            "daily_meal_count",
        )


class FullCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Sector.objects.all()
    )
    diagnostics = DiagnosticSerializer(many=True, read_only=True, source="diagnostic_set")

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
            "diagnostics",
        )
