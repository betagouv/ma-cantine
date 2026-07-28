from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from data.models import Canteen, CanteenImage


class CanteenLogoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    logo = Base64ImageField()

    class Meta:
        model = Canteen
        fields = (
            "id",
            "logo",
        )


class CanteenImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = CanteenImage
        fields = (
            "id",
            "image",
            "alt_text",
        )
