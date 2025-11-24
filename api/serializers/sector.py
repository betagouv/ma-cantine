from rest_framework import serializers

from data.models import SectorM2M, Sector, SectorCategory


class SectorSerializer(serializers.Serializer):
    value = serializers.CharField()
    name = serializers.CharField()
    category = serializers.ChoiceField(choices=SectorCategory.choices)
    category_name = serializers.CharField()
    has_line_ministry = serializers.BooleanField()


# remember to update TD version if you update this
class SectorM2MSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="get_category_display")

    class Meta:
        model = SectorM2M  # TODO: use Sector enum instead
        fields = (
            "id",
            "value",
            "name",
            "category",
            "category_name",
            "has_line_ministry",
        )

    def get_value(self, obj):
        return next(value for value, label in Sector.choices if label == obj.name.replace("’", "'"))
