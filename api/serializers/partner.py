from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from data.models import Partner


class PartnerShortSerializer(serializers.ModelSerializer):
    types = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Partner
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "name",
            "categories",
            "short_description",
            "image",
            "types",
            "departments",
            "national",
            "gratuity_option",
            "economic_model",
        )


class PartnerSerializer(serializers.ModelSerializer):
    types = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Partner
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "name",
            "categories",
            "short_description",
            "long_description",
            "image",
            "website",
            "types",
            "departments",
            "national",
            "free",
            "economic_model",
        )
