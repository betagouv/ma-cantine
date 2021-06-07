from rest_framework import serializers
from data.models import Diagnostic


class DiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        read_only_fields = ("id",)
        fields = (
            "id",
            "year",
            "value_bio_ht",
            "value_fair_trade_ht",
            "value_sustainable_ht",
            "value_total_ht",
            "has_waste_diagnostic",
            "has_waste_plan",
            "waste_actions",
            "has_donation_agreement",
            "has_diversification_plan",
            "vegetarian_weekly_recurrence",
            "vegetarian_menu_type",
            "cooking_plastic_substituted",
            "serving_plastic_substituted",
            "plastic_bottles_substituted",
            "plastic_tableware_substituted",
            "communication_supports",
            "communication_support_url",
            "communicates_on_food_plan",
        )
