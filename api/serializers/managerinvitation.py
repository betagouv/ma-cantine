from rest_framework import serializers

from data.models import ManagerInvitation


class ManagerInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerInvitation
        fields = ("email",)
        read_only_fields = ("email",)
