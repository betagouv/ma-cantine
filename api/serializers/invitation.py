from rest_framework import serializers

from api.serializers.utils import ReadOnlySerializerMixin
from data.models import Invitation

from .canteen import MinimalCanteenSerializer


class InvitationSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    creation_canteen = MinimalCanteenSerializer()
    invited_canteen = MinimalCanteenSerializer()
    direction = serializers.CharField()  # annotated

    class Meta:
        model = Invitation
        fields = (
            "id",
            "category",
            "status",
            "creation_canteen",
            "invited_canteen",
            "direction",  # annotated
            "creation_date",
            "answer_date",
        )


class InvitationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = (
            "category",
            "creation_canteen",
            "invited_canteen",
        )
