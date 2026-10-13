from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from data.models import EventLog
from data.admin.utils import ReadOnlyAdminMixin


@admin.register(EventLog)
class EventLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "creation_date",  # clickable link to change page
        "category",
        "name",
        "status",
        "user_with_link",  # clickable link to user change page
        "api_oauth2_application",
        "message_short",
    )
    list_filter = ["creation_date", "category", "status", "api_oauth2_application"]
    list_select_related = ["user", "api_oauth2_application"]
    search_fields = (
        "name",
        "user__id",
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__username",
    )
    search_help_text = "La recherche est faite sur les champs : nom, utilisateur (ID, nom, prénom, email)"

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "category",
                    "name",
                    "status",
                    "user",
                    "api_oauth2_application",
                ),
            },
        ),
        (
            "Données",
            {"fields": ("data",)},
        ),
        (
            "Metadonnées",
            {"fields": ("creation_date",)},
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return True

    def user_with_link(self, obj):
        if not obj.user_id:
            return None
        url = reverse("admin:data_user_change", args=[obj.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.user)

    user_with_link.short_description = EventLog._meta.get_field("user").verbose_name

    def message_short(self, obj):
        return obj.message_short

    message_short.short_description = "message"
