from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from data.models import ImportFailure
from data.admin.utils import ReadOnlyAdminMixin


@admin.register(ImportFailure)
class ImportFailureAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "creation_date",
        "user_with_link",
        "import_type",
        "details",
    )
    list_filter = ["creation_date", "import_type"]
    search_fields = (
        "user__id",
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__username",
        "creation_date",
    )
    search_help_text = "La recherche est faite sur les champs : utilisateur (ID, nom, prénom, email)"

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "user",
                    "import_type",
                    "file",
                    "details",
                ),
            },
        ),
        (
            "Metadonnées",
            {"fields": ("creation_date",)},
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return True

    def user_with_link(self, obj):
        url = reverse("admin:data_user_change", args=[obj.user_id])
        return format_html(f'<a href="{url}">{obj.user}</a>')

    user_with_link.short_description = ImportFailure._meta.get_field("user").verbose_name
