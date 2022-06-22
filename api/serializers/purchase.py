from rest_framework import serializers
from data.models import Purchase
from drf_base64.fields import Base64FileField


class PurchaseSerializer(serializers.ModelSerializer):

    canteen = serializers.PrimaryKeyRelatedField(read_only=True)
    invoice_file = Base64FileField(required=False, allow_null=True)
    price_ht = serializers.DecimalField(localize=True, max_digits=20, decimal_places=2)

    class Meta:
        model = Purchase
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "canteen",
            "date",
            "description",
            "provider",
            "family",
            "characteristics",
            "price_ht",
            "invoice_file",
            "local_definition",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        if "canteen" not in validated_data:
            return super().create(validated_data)

        validated_data["canteen_id"] = validated_data.pop("canteen").id
        return super().create(validated_data)


class PurchaseSummarySerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    bio = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    sustainable = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    hve = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    aoc_aop_igp = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    rouge = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)


class PurchaseExportSerializer(serializers.ModelSerializer):
    canteen = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Purchase
        fields = (
            "date",
            "canteen",
            "description",
            "provider",
            "readable_family",
            "readable_characteristics",
            "price_ht",
        )
        read_only_fields = fields
