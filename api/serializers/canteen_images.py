from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from data.models import CanteenImage


class CanteenImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = Base64ImageField()

    class Meta:
        model = CanteenImage
        fields = (
            "id",
            "image",
            "alt_text",
        )
