from rest_framework import serializers
from data.models import Purchase
from drf_base64.fields import Base64FileField


class PurchaseSerializer(serializers.ModelSerializer):

    canteen = serializers.PrimaryKeyRelatedField(read_only=True)
    invoice_file = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = Purchase
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "canteen",
            "date",
            "provider",
            "category",
            "characteristics",
            "price_ht",
            "invoice_file",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        if "canteen" not in validated_data:
            return super().create(validated_data)

        validated_data["canteen_id"] = validated_data.pop("canteen").id
        return super().create(validated_data)
