from rest_framework import serializers

from data.models import SectorM2M


# remember to update TD version if you update this
class SectorM2MSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="get_category_display")

    class Meta:
        model = SectorM2M
        fields = (
            "id",
            "name",
            "category",
            "category_name",
            "has_line_ministry",
        )
