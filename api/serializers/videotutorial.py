from rest_framework import serializers
from data.models import VideoTutorial


class VideoTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTutorial
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "title",
            "description",
            "published",
            "video",
            "subtitles",
            "categories",
            "thumbnail",
        )
