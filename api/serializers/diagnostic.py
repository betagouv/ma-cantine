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
        )
