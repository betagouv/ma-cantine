from django import forms
from django.contrib import admin
from data.models import Canteen
from .diagnostic import DiagnosticInline
from .softdeletionadmin import SoftDeletionAdmin


class CanteenForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "siret": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


@admin.register(Canteen)
class CanteenAdmin(SoftDeletionAdmin):

    form = CanteenForm
    inlines = (DiagnosticInline,)
    fields = (
        "name",
        "main_image",
        "city",
        "department",
        "daily_meal_count",
        "data_is_public",
        "sectors",
        "managers",
        "siret",
        "management_type",
        "deletion_date",
    )
    list_display = (
        "name",
        "city",
        "published_state",
        "creation_date",
        "modification_date",
        "management_type",
        "supprimée",
    )
    filter_vertical = (
        "sectors",
        "managers",
    )
    list_filter = ("sectors", "city", "management_type")

    def published_state(self, obj):
        return "✅ Publié" if obj.data_is_public else "🔒 Non publié"

    def supprimée(self, obj):
        return "🗑️ Supprimée" if obj.deletion_date else ""
