from django.contrib import admin

from data.admin.utils import ReadOnlyAdminMixin
from data.models import WasteAction


@admin.register(WasteAction)
class WasteActionAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "effort",
        "waste_origins",
        "creation_date",
        "modification_date",
    )
