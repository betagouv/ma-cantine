from django.contrib import admin
from data.models import ImportError
from .utils import ReadOnlyAdminMixin


@admin.register(ImportError)
class ImportErrorAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "creation_date",
        "user",
        "import_type",
    )
