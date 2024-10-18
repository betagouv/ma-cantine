from rest_framework import serializers
from rest_framework.fields import Field

from api.serializers.resourceaction import ResourceActionFullSerializer
from data.models import ResourceAction, WasteAction


class WagtailImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            "id": value.id,
            "image": value.file.url,
            "alt_text": value.title,
        }


class WasteActionSerializer(serializers.ModelSerializer):
    lead_image = WagtailImageSerializedField(required=False, allow_null=True)

    class Meta:
        model = WasteAction
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "title",
            "subtitle",
            "description",
            "effort",
            "waste_origins",
            "lead_image",
        )


class WasteActionWithActionsSerializer(WasteActionSerializer):
    actions = serializers.SerializerMethodField()

    class Meta(WasteActionSerializer.Meta):
        fields = WasteActionSerializer.Meta.fields + ("actions",)

    def get_actions(self, obj):
        """Only return actions for authenticated users + related to their canteens."""
        actions = ResourceAction.objects.none()
        user = self.context["request"].user
        if user.is_authenticated:
            actions = ResourceAction.objects.filter(resource=obj).for_user_canteens(user)
        serializer = ResourceActionFullSerializer(instance=actions, many=True)
        return serializer.data
