from rest_framework import serializers

from data.models import ResourceAction


class ResourceActionSerializer(serializers.ModelSerializer):
    resource_id = serializers.IntegerField(read_only=True)
    canteen_id = serializers.IntegerField(required=True)

    class Meta:
        model = ResourceAction
        fields = (
            "resource_id",
            "canteen_id",
            "is_done",
        )


class ResourceActionFullSerializer(ResourceActionSerializer):
    resource = serializers.SerializerMethodField(read_only=True)
    canteen = serializers.SerializerMethodField(read_only=True)

    class Meta(ResourceActionSerializer.Meta):
        fields = ResourceActionSerializer.Meta.fields + (
            "resource",
            "canteen",
        )

    def get_resource(self, obj):
        from .wasteaction import WasteActionSerializer

        return WasteActionSerializer(obj.resource).data

    def get_canteen(self, obj):
        from .canteen import MinimalCanteenSerializer

        return MinimalCanteenSerializer(obj.canteen).data
