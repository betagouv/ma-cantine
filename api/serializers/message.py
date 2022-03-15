from rest_framework import serializers
from data.models import Message
from django.core.validators import validate_email


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "destination_canteen",
            "sender_name",
            "sender_email",
            "body",
        )

    def validate(self, attrs):
        validate_email(attrs["sender_email"])
        return super().validate(attrs)
