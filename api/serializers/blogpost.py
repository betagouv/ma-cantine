from rest_framework import serializers
from data.models import BlogPost
from .user import BlogPostAuthor


class BlogPostSerializer(serializers.ModelSerializer):

    author = BlogPostAuthor()
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
