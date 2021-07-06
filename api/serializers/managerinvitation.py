from rest_framework import serializers
from data.models import ManagerInvitation


class ManagerInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManagerInvitation
        read_only_fields = (
            "email",
        )
        fields = (
            "email",
        )
