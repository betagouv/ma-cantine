from rest_framework import serializers
from cms.models import WasteAction
from cms.serializers import ChoiceField, ChoiceArrayField


class WasteActionSerializer(serializers.ModelSerializer):
    effort = ChoiceField(choices=WasteAction.Effort.choices)
    waste_origin = ChoiceArrayField(choices=WasteAction.WasteOrigin.choices)

    class Meta:
        model = WasteAction
        fields = "__all__"
