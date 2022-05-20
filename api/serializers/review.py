from rest_framework import serializers
from data.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "rating",
            "suggestion",
            "page",
            "hasCanteen",
            "hasDiagnostic",
        )
