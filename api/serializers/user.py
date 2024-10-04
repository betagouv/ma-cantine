from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .review import MiniReviewSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "avatar",
        )
        read_only_fields = fields


class LoggedUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    reviews = MiniReviewSerializer(many=True, read_only=True, source="review_set")

    class Meta:
        model = get_user_model()
        read_only_fields = (
            "id",
            "username",
            "is_staff",
            "has_mtm_data",
        )
        fields = (
            "id",
            "email",
            "phone_number",
            "username",
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


class CanteenManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        read_only_fields = (
            "email",
            "first_name",
            "last_name",
        )
        fields = (
            "email",
            "first_name",
            "last_name",
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
