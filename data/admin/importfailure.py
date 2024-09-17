from django.contrib import admin

from data.models import ImportFailure

from .utils import ReadOnlyAdminMixin


@admin.register(ImportFailure)
class ImportFailureAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "creation_date",
        "user",
        "import_type",
    )

    def has_delete_permission(self, request, obj=None):
        return True

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__username",
        "creation_date",
    )

    list_filter = ["creation_date", "import_type"]
