from rest_framework import serializers
from data.models import WasteAction


class WasteActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteAction
        fields = "__all__"
