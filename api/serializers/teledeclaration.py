from rest_framework import serializers

from data.models import Teledeclaration


class ShortTeledeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "status",
        )
        read_only_fields = fields


class OpenDataTeledeclarationSerializer(serializers.ModelSerializer):

    value_total_ht = serializers.SerializerMethodField()
    value_bio_ht = serializers.SerializerMethodField()
    diagnostic_type = serializers.SerializerMethodField()

    class Meta:
        model = Teledeclaration

        fields = ("id", "canteen_id", "creation_date", "value_total_ht", "value_bio_ht", "diagnostic_type")
        read_only_fields = fields

    def get_value_total_ht(self, obj):
        if "value_total_ht" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["value_total_ht"]

    def get_value_bio_ht(self, obj):
        if "value_bio_ht" in obj.declared_data["teledeclaration"]:
            return obj.declared_data["teledeclaration"]["value_bio_ht"]

    def get_diagnostic_type(self, obj):
        try:
            obj.declared_data["teledeclaration"]["diagnostic_type"]
        except Exception:
            return None
