import json

from django import forms
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe

from common.models import CommandLog
from common.cache.admin import CacheAdmin  # needed to help Django discover the models in the subfolders  # noqa
from data.admin.utils import ReadOnlyAdminMixin


User = get_user_model()
admin.site.unregister(Group)


class GroupAdminForm(forms.ModelForm):
    """
    Custom Group admin
    - to allow managing users directly
    - taken from https://stackoverflow.com/a/39648244
    """

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name=User._meta.verbose_name, is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super().save()
        self.save_m2m()
        return instance


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "permissions_count", "users_count")
    search_fields = ("name",)

    form = GroupAdminForm
    filter_horizontal = ("permissions",)
    fields = ("name", "permissions", "users")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("permissions", "user_set")
        return qs

    @admin.display(description="Permissions")
    def permissions_count(self, obj):
        return obj.permissions.count()

    @admin.display(description="Utilisateurs")
    def users_count(self, obj):
        return obj.user_set.count()


@admin.register(CommandLog)
class CommandLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "command_name",
        "status",
        "start_date",
        "duration_display",
        "creation_date",
    )
    list_filter = ("command_name", "status")
    search_fields = ("command_name",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "command_name",
                    "input_data_pretty",
                )
            },
        ),
        (
            "Résultat",
            {
                "fields": (
                    "status",
                    "start_date",
                    "end_date",
                    "duration_display",
                    "output_data",
                )
            },
        ),
        (
            "Métadonnées",
            {"fields": (*CommandLog.CREATION_META_FIELDS,)},
        ),
    )

    @admin.display(description="Durée")
    def duration_display(self, obj):
        if obj.duration is None:
            return "-"
        return f"{obj.duration:.2f} s"

    def input_data_pretty(self, obj):
        data = json.dumps(obj.input_data, indent=2)
        return mark_safe(f"<pre>{data}</pre>")

    input_data_pretty.short_description = CommandLog._meta.get_field("input_data").verbose_name
