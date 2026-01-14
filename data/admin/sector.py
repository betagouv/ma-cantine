from django.contrib import admin

from data.models import SectorM2M


@admin.register(SectorM2M)
class SectorM2MAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "has_line_ministry",
        "creation_date",
    )
    list_filter = ("category", "has_line_ministry")

    fields = (
        "name",
        "category",
        "has_line_ministry",
        "creation_date",
        "modification_date",
    )
    readonly_fields = ("creation_date", "modification_date")

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
