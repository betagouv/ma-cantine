from django import forms
from django.contrib import admin
from data.models import Teledeclaration


class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TeledeclarationForm(forms.ModelForm):
    class Meta:
        widgets = {
            "fields": forms.Textarea(attrs={"cols": 60, "rows": 5}),
        }


class TeledeclarationInline(admin.TabularInline):
    model = Teledeclaration
    show_change_link = False
    can_delete = False
    fields = ("year", "creation_date", "status", "applicant")
    readonly_fields = fields
    extra = 0


@admin.register(Teledeclaration)
class TeledeclarationAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):

    form = TeledeclarationForm
    list_display = (
        "canteen_name",
        "year",
        "creation_date",
        "status",
    )
    list_filter = ("year", "status")
    fields = (
        "year",
        "creation_date",
        "status",
        "fields",
    )

    def canteen_name(self, obj):
        return obj.fields["canteen"]["name"]
