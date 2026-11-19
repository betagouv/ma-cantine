from rest_framework import serializers


class PartnerTypeSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
