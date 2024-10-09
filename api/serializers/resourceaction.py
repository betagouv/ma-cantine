from rest_framework import serializers

from data.models import ResourceAction


class ResourceActionSerializer(serializers.ModelSerializer):
    canteen_id = serializers.IntegerField(required=True)

    class Meta:
        model = ResourceAction
        fields = (
            "canteen_id",
            "is_done",
        )
