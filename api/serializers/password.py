from django.contrib.auth import password_validation
from rest_framework import serializers


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password_1 = serializers.CharField(
        max_length=128, write_only=True, required=True
    )
    new_password_2 = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Votre ancien mot de passe est incorrect. Veuillez le rectifier."
            )
        return value

    def validate(self, data):
        if data["new_password_1"] != data["new_password_2"]:
            raise serializers.ValidationError(
                "Les deux mots de passe ne correspondent pas."
            )
        password_validation.validate_password(
            data["new_password_1"], self.context["request"].user
        )
        return data

    def save(self, **kwargs):
        password = self.validated_data["new_password_1"]
        user = self.context["request"].user
        user.set_password(password)
        user.save()
        return user
