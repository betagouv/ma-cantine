import json

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from data.admin.utils import ReadOnlyAdminMixin
from data.models import Teledeclaration


class TeledeclarationForm(forms.ModelForm):
    class Meta:
        widgets = {
            "declared_data": forms.Textarea(attrs={"cols": 60, "rows": 5}),
        }

    # thanks to https://github.com/jazzband/django-simple-history/issues/853#issuecomment-1105754544
    change_reason = forms.CharField(
        label="Raison de modification",
        help_text="100 caractères max",
        max_length=100,
        widget=forms.TextInput(attrs={"size": "70"}),
    )


class TeledeclarationInline(admin.TabularInline):
    model = Teledeclaration
    show_change_link = True
    can_delete = False
    fields = ("year", "creation_date", "status", "applicant")
    readonly_fields = fields
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Teledeclaration)
class TeledeclarationAdmin(ReadOnlyAdminMixin, SimpleHistoryAdmin):
    form = TeledeclarationForm
    list_display = (
        "canteen_name",
        "year",
        "applicant",
        "creation_date",
        "status",
    )
    history_list_display = ["authentication_method"]
    list_filter = ("year", "status")
    fields = (
        "canteen",
        "canteen_siret",
        "year",
        "applicant",
        "diagnostic",
        "creation_date",
        "status",
        "modification_date",
        "value_totale",
        "value_bio_agg",
        "value_siqo_agg",
        "value_externalites_performance_agg",
        "value_egalim_autres_agg",
        "meal_price",
        "yearly_meal_count",
        "declared_data_pretty",
        "teledeclaration_mode",
        "change_reason",
    )
    # want to be able to modify status
    readonly_fields = (
        "canteen",
        "canteen_siret",
        "year",
        "applicant",
        "diagnostic",
        "creation_date",
        "modification_date",
        "value_totale",
        "value_bio_agg",
        "value_siqo_agg",
        "value_externalites_performance_agg",
        "value_egalim_autres_agg",
        "meal_price",
        "yearly_meal_count",
        "declared_data_pretty",
        "teledeclaration_mode",
    )
    search_fields = (
        "canteen__name",
        "canteen__siret",
        "canteen__siren_unite_legale",
        "applicant__username",
        "applicant__email",
    )

    def declared_data_pretty(self, obj):
        data = json.dumps(obj.declared_data, indent=2)
        return mark_safe(f"<pre>{data}</pre>")

    def canteen_name(self, obj):
        return obj.declared_data["canteen"]["name"]

    # overriding mixin
    def has_change_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        obj._change_reason = form.cleaned_data["change_reason"]
        super().save_model(request, obj, form, change)
