from django import forms
from django.contrib import admin
from data.models import Canteen
from .diagnosis import DiagnosisInline


class CanteenForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


@admin.register(Canteen)
class CanteenAdmin(admin.ModelAdmin):

    form = CanteenForm
    inlines = (DiagnosisInline,)
    fields = (
        "name",
        "city",
        "postal_code",
        "daily_meal_count",
        "published",
        "data_is_public",
        "sectors",
        "managers",
    )
    list_display = (
        "name",
        "city",
        "published_state",
        "creation_date",
        "modification_date",
    )
    filter_vertical = (
        "sectors",
        "managers",
    )
    list_filter = ("name", "city")

    def published_state(self, obj):
        return "✅ Publié" if obj.published else "🔒 Non publié"
