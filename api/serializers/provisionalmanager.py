from rest_framework import serializers
from data.models import ProvisionalManager
from .canteen import FullCanteenSerializer


class ProvisionalManagerSerializer(serializers.ModelSerializer):

    canteen = FullCanteenSerializer()

    class Meta:
        model = ProvisionalManager
        fields = (
            "id",
            "email",
            "canteen",
        )
