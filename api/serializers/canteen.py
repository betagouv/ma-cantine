from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from data.models import Canteen, Sector
from .diagnostic import DiagnosticSerializer
from .user import CanteenManager


class PublicCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    diagnostics = DiagnosticSerializer(
        many=True, read_only=True, source="diagnostic_set"
    )
    main_image = Base64ImageField(required=False, allow_null=True)

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
            "department",
            "main_image",
        )


class FullCanteenSerializer(serializers.ModelSerializer):

    sectors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Sector.objects.all(), required=False
    )
    diagnostics = DiagnosticSerializer(
        many=True, read_only=True, source="diagnostic_set"
    )
    main_image = Base64ImageField(required=False, allow_null=True)
    managers = CanteenManager(many=True)

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "city",
            "postal_code",
            "sectors",
            "data_is_public",
            "daily_meal_count",
            "siret",
            "management_type",
            "diagnostics",
            "department",
            "main_image",
            "managers",
        )
