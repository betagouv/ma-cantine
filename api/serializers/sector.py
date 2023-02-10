from rest_framework import serializers
from data.models import Sector


# remember to update TD version if you update this
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = (
            "id",
            "name",
            "category",
            "has_line_ministry",
        )
