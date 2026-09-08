from django.contrib.auth import get_user_model
from rest_framework import serializers

from data.models import ManagerInvitation
from data.models.canteen import Canteen


class CanteenManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
        )
        read_only_fields = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
        )


class CanteenManagerInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerInvitation
        fields = ("email",)
        read_only_fields = ("email",)


class ManagingTeamSerializer(serializers.ModelSerializer):
    managers = CanteenManagerSerializer(many=True, read_only=True)
    manager_invitations = CanteenManagerInvitationSerializer(source="managerinvitation_set", many=True, read_only=True)

    class Meta:
        model = Canteen
        fields = ("id", "managers", "manager_invitations")
