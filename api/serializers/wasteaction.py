from rest_framework import serializers
from rest_framework.fields import Field

from api.serializers.resourceaction import ResourceActionWithCanteenSerializer
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
    actions = ResourceActionWithCanteenSerializer(many=True, read_only=True)

    class Meta(WasteActionSerializer.Meta):
        fields = WasteActionSerializer.Meta.fields + ("actions",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.pop("user", None)
        if user:
            self.fields["actions"].queryset = ResourceAction.objects.for_user(user)
        else:
            self.fields["actions"].queryset = ResourceAction.objects.none()
