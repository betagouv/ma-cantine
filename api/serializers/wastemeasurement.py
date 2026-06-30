from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer

from data.models import WasteMeasurement
from api.serializers.utils import set_help_text_from_verbose_name


REQUIRED_FIELDS = ["period_start_date", "period_end_date"]
WRITE_ONLY_FIELDS = ["creation_source"]
READ_ONLY_FIELDS = ["id", "creation_date", "modification_date"]


@set_help_text_from_verbose_name
@extend_schema_serializer(exclude_fields=WRITE_ONLY_FIELDS)
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

    def get_fields(self):
        fields = super().get_fields()
        # some fields are required
        for field in REQUIRED_FIELDS:
            fields[field].required = True
            fields[field].allow_null = False
            fields[field].allow_blank = False
        # some fields are only available on create
        # and hidden from the docs (see extend_schema_serializer)
        for field in WRITE_ONLY_FIELDS:
            fields[field].write_only = True
        # some fields are readonly
        for field in READ_ONLY_FIELDS:
            fields[field].read_only = True
        return fields
