from rest_framework import serializers

from api.serializers.utils import ReadOnlySerializerMixin
from data.models import Teledeclaration


class ShortTeledeclarationSerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "status",
        )
