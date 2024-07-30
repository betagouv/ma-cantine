from rest_framework import serializers
from cms.models import WasteAction
from cms.serializers import ChoiceField, ChoiceArrayField, ImageSerializedField
from wagtail.images.api.fields import ImageRenditionField


class WasteActionSerializer(serializers.ModelSerializer):
    effort = ChoiceField(choices=WasteAction.Effort.choices)
    waste_origin = ChoiceArrayField(choices=WasteAction.WasteOrigin.choices)
    lead_image = ImageSerializedField()

    class Meta:
        model = WasteAction
        fields = "__all__"
