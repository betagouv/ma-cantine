from rest_framework import serializers

from api.serializers.canteen import MinimalCanteenSerializer
from data.models import ResourceAction


class ResourceActionSerializer(serializers.ModelSerializer):
    canteen_id = serializers.IntegerField(required=True)

    class Meta:
        model = ResourceAction
        fields = (
            "canteen_id",
            "is_done",
        )


class ResourceActionWithCanteenSerializer(ResourceActionSerializer):
    canteen = MinimalCanteenSerializer(read_only=True)

    class Meta(ResourceActionSerializer.Meta):
        fields = ResourceActionSerializer.Meta.fields + ("canteen",)
