from django import forms
from django.contrib import admin
from data.models import Partner


class PartnerForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "short_description": forms.Textarea(attrs={"cols": 55, "rows": 1}),
        }


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):

    form = PartnerForm
    fields = (
        "name",
        "short_description",
        "long_description",
        "image",
        "types",
        "departments",
        "national",
        "free",
        "economic_model",
    )
    filter_vertical = ("types",)
    list_display = (
        "name",
        "creation_date",
        "modification_date",
    )
