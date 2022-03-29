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
    fields = ("name", "category")
    list_display = (
        "name",
        "creation_date",
    )
    list_filter = ("name",)
