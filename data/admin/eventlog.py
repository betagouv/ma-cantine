import json

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from data.models import EventLog, ImportType
from data.admin.utils import ReadOnlyAdminMixin


class EventLogNameListFilter(admin.SimpleListFilter):
    """
    Only shown once a category is selected, and only lists that category's names
    (avoids a SELECT DISTINCT on the whole table)
    """

    title = "nom"
    parameter_name = "name"

    def lookups(self, request, model_admin):
        category = request.GET.get("category__exact")
        if not category:
            return []
        if category == EventLog.Category.IMPORT:
            return ImportType.choices
        names = EventLog.objects.filter(category=category).order_by("name").values_list("name", flat=True).distinct()
        return [(name, name) for name in names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name=self.value())
        return queryset


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
    list_filter = ["creation_date", "category", EventLogNameListFilter, "status", "api_oauth2_application"]
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
    readonly_fields = ("data_pretty",)

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
            {"fields": ("data_pretty",)},
        ),
        (
            "Metadonnées",
            {"fields": ("creation_date", "modification_date")},
        ),
    )

    def user_with_link(self, obj):
        if not obj.user_id:
            return None
        url = reverse("admin:data_user_change", args=[obj.user_id])
        return format_html('<a href="{}">{}</a>', url, obj.user)

    user_with_link.short_description = EventLog._meta.get_field("user").verbose_name

    def message_short(self, obj):
        return obj.message_short

    message_short.short_description = "message"

    def data_pretty(self, obj):
        # format_html escapes the content (data can contain user input, API responses...)
        return format_html("<pre>{}</pre>", json.dumps(obj.data, indent=2, ensure_ascii=False))

    data_pretty.short_description = EventLog._meta.get_field("data").verbose_name
