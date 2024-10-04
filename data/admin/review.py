from django.contrib import admin

from data.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = (
        "rating",
        "suggestion",
        "page",
        "hasCanteen",
        "hasDiagnostic",
        "creation_date",
        "user",
    )
    readonly_fields = fields
    list_display = (
        "user",
        "page",
        "hasCanteen",
        "hasDiagnostic",
        "rating",
        "creation_date",
        "suggestion",
    )
    list_filter = (
        "rating",
        "page",
    )
