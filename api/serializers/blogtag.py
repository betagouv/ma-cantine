from rest_framework import serializers
from data.models import BlogTag


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = (
            "id",
            "name",
        )
        read_only_fields = fields
