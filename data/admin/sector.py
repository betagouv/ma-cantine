from django import forms
from django.contrib import admin

from data.models import Sector


class SectorForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    form = SectorForm
    fields = (
        "name",
        "category",
        "has_line_ministry",
        "creation_date",
    )
    readonly_fields = ("creation_date",)
    list_display = (
        "name",
        "category",
        "has_line_ministry",
        "creation_date",
    )
    list_filter = ("category", "has_line_ministry")
