from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .review import MiniReviewSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    # NOTE: the `username` field was removed from the model, but is kept as an always-null stub
    username = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "avatar",
        )
        read_only_fields = fields

    def get_username(self, obj):
        return None


class LoggedUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    reviews = MiniReviewSerializer(many=True, read_only=True, source="review_set")

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "avatar",
            "is_staff",
            "is_dev",
            "is_elected_official",
            "job",
            "other_job_description",
            "source",
            "other_source_description",
            "has_mtm_data",
            "reviews",
            "mcp_organizations",
            "departments",
        )
        read_only_fields = (
            "id",
            "is_staff",
            "has_mtm_data",
        )


class BlogPostAuthor(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "avatar",
        )
