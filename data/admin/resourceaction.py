from django.contrib import admin

from data.models import ResourceAction

from .utils import ReadOnlyAdminMixin


@admin.register(ResourceAction)
class ResourceActionAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "resource",
        "canteen",
        "user",
        "is_done",
        "is_not_interested",
        "is_favorite",
        "creation_date",
        "modification_date",
    )
