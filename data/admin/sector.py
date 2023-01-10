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
        "category",
        "name",
        "has_line_ministry",
    )
    list_display = (
        "name",
        "category",
        "creation_date",
    )
    list_filter = ("category",)
