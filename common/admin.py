from django import forms
from common.cache.admin import CacheAdmin  # needed to help Django discover the models in the subfolders  # noqa
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple


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
