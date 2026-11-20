from rest_framework import serializers

from data.models import SectorCategory


class SectorSerializer(serializers.Serializer):
    value = serializers.CharField()
    name = serializers.CharField()
    category = serializers.ChoiceField(choices=SectorCategory.choices)
    category_name = serializers.CharField()
    has_line_ministry = serializers.BooleanField()
