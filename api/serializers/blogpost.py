from rest_framework import serializers

from api.serializers import BlogPostAuthorSerializer
from data.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    author = BlogPostAuthorSerializer()
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = BlogPost
        fields = (
            "id",
            "creation_date",
            "modification_date",
            "title",
            "tagline",
            "body",
            "published",
            "display_date",
            "author",
            "tags",
        )
