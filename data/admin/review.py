from django.contrib import admin
from data.models import Review
from .utils import ReadOnlyAdminMixin


@admin.register(Review)
class ReviewAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    fields = (
        "rating",
        "suggestion",
        "page",
        "creation_date",
        "user",
    )
    read_only_fields = fields
    list_display = (
        "page",
        "rating",
        "creation_date",
        "suggestion",
        "user",
    )
    list_filter = (
        "rating",
        "page",
    )
