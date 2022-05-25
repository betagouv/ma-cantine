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


class MiniReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("hasCanteen", "hasDiagnostic")
