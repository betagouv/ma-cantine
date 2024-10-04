from rest_framework import serializers

from data.models import WasteMeasurement


class WasteMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteMeasurement
        read_only_fields = ("id",)
        fields = (
            "id",
            "canteen_id",
            "period_start_date",
            "period_end_date",
            "days_in_period",
            "meal_count",
            "total_mass",
            "total_yearly_waste_estimation",
            "is_sorted_by_source",
            "preparation_total_mass",
            "preparation_is_sorted",
            "preparation_edible_mass",
            "preparation_inedible_mass",
            "unserved_total_mass",
            "unserved_is_sorted",
            "unserved_edible_mass",
            "unserved_inedible_mass",
            "leftovers_total_mass",
            "leftovers_is_sorted",
            "leftovers_edible_mass",
            "leftovers_inedible_mass",
        )
