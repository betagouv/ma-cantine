from django import forms
from django.contrib import admin
from data.models import PartnerType


class PartnerTypeForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


@admin.register(PartnerType)
class PartnerTypeAdmin(admin.ModelAdmin):

    form = PartnerTypeForm
    fields = ("name",)
    list_display = (
        "name",
        "creation_date",
    )
    list_filter = ("name",)
