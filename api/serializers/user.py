from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_base64.fields import Base64ImageField


class LoggedUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = get_user_model()
        read_only_fields = (
            "id",
            "username",
            "is_staff",
        )
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_staff",
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
