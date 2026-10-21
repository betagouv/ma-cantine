from django.template.defaultfilters import linebreaks_filter
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
            "gratuity_option",
            "economic_model",
        )


class PartnerContactSerializer(serializers.ModelSerializer):
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
            "sector_categories",
            "gratuity_option",
            "economic_model",
            "contact_name",
            "contact_email",
            "contact_message",
            "contact_phone_number",
        )

    def validate_long_description(self, value):
        """
        The public form sends plain text, but the field is rendered as HTML (rich text, editable in the admin):
        escape it (avoid a stored-XSS) and keep the line breaks as <p> & <br>
        """
        if not value:
            return value
        return linebreaks_filter(value, autoescape=True)
