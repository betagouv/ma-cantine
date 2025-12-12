from rest_framework import serializers

from data.models import Teledeclaration


class ShortTeledeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teledeclaration
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "status",
        )
        read_only_fields = fields


class CampaignDatesSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    teledeclaration_start_date = serializers.DateTimeField()
    teledeclaration_end_date = serializers.DateTimeField()
    correction_start_date = serializers.DateTimeField(allow_null=True)
    correction_end_date = serializers.DateTimeField(allow_null=True)
    rapport_parlement_url = serializers.URLField(allow_null=True)


class CampaignDatesFullSerializer(CampaignDatesSerializer):
    # additional fields
    in_teledeclaration = serializers.BooleanField()
    in_correction = serializers.BooleanField()
