from django.contrib import admin

from data.models import WasteAction

from .utils import ReadOnlyAdminMixin


@admin.register(WasteAction)
class WasteActionAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "effort",
        "waste_origins",
        "creation_date",
        "modification_date",
    )
