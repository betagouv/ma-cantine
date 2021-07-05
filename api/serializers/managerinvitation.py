from rest_framework import serializers
from data.models import ManagerInvitation
from .canteen import FullCanteenSerializer


class ManagerInvitationSerializer(serializers.ModelSerializer):

    canteen = FullCanteenSerializer()

    class Meta:
        model = ManagerInvitation
        fields = (
            "id",
            "email",
            "canteen",
        )
