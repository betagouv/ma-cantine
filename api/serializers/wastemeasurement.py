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

    def validate(self, data):
        if data["period_start_date"] >= data["period_end_date"]:
            raise serializers.ValidationError({"period_start_date": ["La date doit être avant la date de fin"]})
        self._check_dates_against_existing_measurements(data)
        return data

    def _check_dates_against_existing_measurements(self, data):
        start_date = data["period_start_date"]
        measurement_containing_start_date = WasteMeasurement.objects.filter(
            period_start_date__lt=start_date, period_end_date__gt=start_date
        )
        if measurement_containing_start_date.exists():
            wm = measurement_containing_start_date.first()
            raise serializers.ValidationError(
                {
                    "period_start_date": [
                        f"Il existe déjà une mesure pour la période {wm.period_start_date} à {wm.period_end_date}. Veuillez modifier la mesure existante ou corriger la date."
                    ]
                }
            )
        end_date = data["period_end_date"]
        measurement_containing_end_date = WasteMeasurement.objects.filter(
            period_start_date__lt=end_date, period_end_date__gt=end_date
        )
        if measurement_containing_end_date.exists():
            wm = measurement_containing_end_date.first()
            raise serializers.ValidationError(
                {
                    "period_end_date": [
                        f"Il existe déjà une mesure pour la période {wm.period_start_date} à {wm.period_end_date}. Veuillez modifier la mesure existante ou corriger la date."
                    ]
                }
            )

        measurements_within_period = WasteMeasurement.objects.filter(
            period_start_date__gt=start_date, period_end_date__lt=end_date
        )
        if measurements_within_period.exists():
            wm_count = measurements_within_period.count()
            measure_count_str = "une mesure" if wm_count == 1 else f"{wm_count} mesures"
            raise serializers.ValidationError(
                f"Il existe déjà {measure_count_str} dans la période {start_date} à {end_date}. Veuillez modifier les mesures existantes ou corriger les dates de la période."
            )
