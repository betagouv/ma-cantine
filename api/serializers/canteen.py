from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from data.models import Canteen, Sector
from .diagnostic import DiagnosticSerializer
from .user import CanteenManagerSerializer
from .managerinvitation import ManagerInvitationSerializer


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
            "city_insee_code",
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
    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = ManagerInvitationSerializer(
        many=True, read_only=True, source="managerinvitation_set"
    )

    class Meta:
        model = Canteen
        fields = (
            "id",
            "name",
            "city",
            "city_insee_code",
            "postal_code",
            "sectors",
            "publication_status",
            "daily_meal_count",
            "siret",
            "management_type",
            "production_type",
            "diagnostics",
            "department",
            "main_image",
            "managers",
            "manager_invitations"
        )


class ManagingTeamSerializer(serializers.ModelSerializer):

    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = ManagerInvitationSerializer(
        many=True, read_only=True, source="managerinvitation_set"
    )

    class Meta:
        model = Canteen
        fields = (
            "id",
            "managers",
            "manager_invitations"
        )
