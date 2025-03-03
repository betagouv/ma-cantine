from rest_framework import serializers

from data.models import Sector


# remember to update TD version if you update this
class SectorSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="get_category_display")

    class Meta:
        model = Sector
        fields = (
            "id",
            "name",
            "category",
            "category_name",
            "has_line_ministry",
        )
