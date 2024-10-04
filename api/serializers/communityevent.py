from rest_framework import serializers

from data.models import CommunityEvent


class CommunityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityEvent
        fields = (
            "id",
            "title",
            "tagline",
            "start_date",
            "end_date",
            "link",
        )
