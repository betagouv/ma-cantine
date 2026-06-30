from rest_framework import serializers

from data.models import WasteMeasurement


CREATE_ONLY_FIELDS = ["creation_source"]


class WasteMeasurementSerializer(serializers.ModelSerializer):
    days_in_period = serializers.IntegerField(read_only=True)  # property
    total_yearly_waste_estimation = serializers.FloatField(read_only=True, allow_null=True)  # property

    class Meta:
        model = WasteMeasurement
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
            "creation_source",
            "creation_date",
            "modification_date",
        )
        read_only_fields = (
            "id",
            # "creation_source",
            "creation_date",
            "modification_date",
        )

    def get_fields(self):
        fields = super().get_fields()
        # some fields are only available on create (and hidden from the docs)
        for field in CREATE_ONLY_FIELDS:
            if self.instance is not None:
                fields.pop(field, None)
            else:
                fields[field].write_only = True
                fields[field].exclude_from_schema = True
        return fields
