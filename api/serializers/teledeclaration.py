from rest_framework import serializers


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
