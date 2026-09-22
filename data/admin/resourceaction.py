from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from data.admin.utils import ReadOnlyAdminMixin
from data.models import ResourceAction


@admin.register(ResourceAction)
class ResourceActionAdmin(ReadOnlyAdminMixin, SimpleHistoryAdmin):
    list_display = (
        "resource",
        "canteen",
        "is_done",
        "is_favorite",
        "creation_date",
        "modification_date",
    )
