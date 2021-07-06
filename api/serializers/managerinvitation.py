from rest_framework import serializers
from data.models import ManagerInvitation


class ManagerInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManagerInvitation
        fields = (
            "id",
            "email",
        )
