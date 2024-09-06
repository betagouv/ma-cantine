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
            "meal_count",
            "total_mass",
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
        self._validate_dates(data)
        return data

    def _validate_dates(self, data):
        has_start_date = "period_start_date" in data
        has_end_date = "period_end_date" in data
        start_date = data["period_start_date"] if has_start_date else self.instance.period_start_date
        end_date = data["period_end_date"] if has_end_date else self.instance.period_end_date

        if has_start_date and start_date >= end_date:
            raise serializers.ValidationError(
                {"period_start_date": ["La date de début doit être avant la date de fin"]}
            )
        elif has_end_date and end_date <= start_date:
            raise serializers.ValidationError({"period_end_date": ["La date de fin doit être après la date de début"]})

        other_measurements = WasteMeasurement.objects
        if self.instance and self.instance.id:
            other_measurements = other_measurements.exclude(id=self.instance.id)

        if has_start_date:
            measurement_containing_start_date = other_measurements.filter(
                period_start_date__lte=start_date, period_end_date__gte=start_date
            )
            if measurement_containing_start_date.exists():
                wm = measurement_containing_start_date.first()
                raise serializers.ValidationError(
                    {
                        "period_start_date": [
                            f"Il existe déjà une autre mesure pour la période {wm.period_start_date} à {wm.period_end_date}. Veuillez modifier la mesure existante ou corriger la date de début."
                        ]
                    }
                )

        if has_end_date:
            measurement_containing_end_date = other_measurements.filter(
                period_start_date__lte=end_date, period_end_date__gte=end_date
            )
            if measurement_containing_end_date.exists():
                wm = measurement_containing_end_date.first()
                raise serializers.ValidationError(
                    {
                        "period_end_date": [
                            f"Il existe déjà une autre mesure pour la période {wm.period_start_date} à {wm.period_end_date}. Veuillez modifier la mesure existante ou corriger la date de fin."
                        ]
                    }
                )

        if has_start_date or has_end_date:
            measurements_within_period = other_measurements.filter(
                period_start_date__gte=start_date, period_end_date__lte=end_date
            )
            if measurements_within_period.exists():
                wm_count = measurements_within_period.count()
                measure_count_str = "une autre mesure" if wm_count == 1 else f"{wm_count} autres mesures"
                raise serializers.ValidationError(
                    f"Il existe déjà {measure_count_str} dans la période {start_date} à {end_date}. Veuillez modifier les mesures existantes ou corriger les dates de la période."
                )
