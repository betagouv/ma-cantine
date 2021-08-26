from rest_framework import serializers
from data.models import Teledeclaration


class ShortTeledeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        read_only_fields = ("id",)
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "status",
        )
