from rest_framework import serializers
from data.models import Diagnostic
from decimal import Decimal
from .teledeclaration import ShortTeledeclarationSerializer

FIELDS = (
    "id",
    "year",
    "value_bio_ht",
    "value_fair_trade_ht",
    "value_sustainable_ht",
    "value_pat_ht",
    "value_total_ht",
    "has_waste_diagnostic",
    "has_waste_plan",
    "waste_actions",
    "other_waste_action",
    "has_donation_agreement",
    "has_waste_measures",
    "bread_leftovers",
    "served_leftovers",
    "unserved_leftovers",
    "side_leftovers",
    "donation_frequency",
    "donation_quantity",
    "donation_food_type",
    "other_waste_comments",
    "has_diversification_plan",
    "diversification_plan_actions",
    "vegetarian_weekly_recurrence",
    "vegetarian_menu_type",
    "vegetarian_menu_bases",
    "cooking_plastic_substituted",
    "serving_plastic_substituted",
    "plastic_bottles_substituted",
    "plastic_tableware_substituted",
    "communication_supports",
    "other_communication_support",
    "communication_support_url",
    "communicates_on_food_plan",
    "communicates_on_food_quality",
    "communication_frequency",
    "creation_date",
    "modification_date",
)


class PublicDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        read_only_fields = ("id",)
        fields = FIELDS

    def validate(self, data):
        total = self.return_value(self, data, "value_total_ht")
        if total is not None and isinstance(total, Decimal):
            bio = self.return_value(self, data, "value_bio_ht")
            sustainable = self.return_value(self, data, "value_sustainable_ht")
            fair_trade = self.return_value(self, data, "value_fair_trade_ht")
            value_sum = bio + sustainable + fair_trade
            if value_sum > total:
                raise serializers.ValidationError(
                    f"La somme des valeurs d'approvisionnement, {value_sum}, est plus que le total, {total}"
                )
        return data

    @staticmethod
    def return_value(serializer, data, field_name):
        if data.get(field_name):
            return data.get(field_name)
        elif serializer.instance and getattr(serializer.instance, field_name):
            return getattr(serializer.instance, field_name)


class FullDiagnosticSerializer(serializers.ModelSerializer):
    teledeclaration = ShortTeledeclarationSerializer(source="latest_teledeclaration")

    class Meta:
        model = Diagnostic
        fields = FIELDS + ("teledeclaration",)
        read_only_fields = fields
