from rest_framework import serializers
from data.models import WasteMeasurement


class WasteMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteMeasurement
        read_only_fields = ("id",)
        fields = ("id", "canteen_id")
