from django import forms
from django.contrib import admin
from data.models import Partner


class PartnerForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "short_description": forms.Textarea(attrs={"cols": 55, "rows": 2}),
        }


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):

    form = PartnerForm
    fields = (
        "name",
        "categories",
        "short_description",
        "long_description",
        "image",
        "website",
        "types",
        "departments",
        "national",
        "free",
        "economic_model",
        "published",
    )
    filter_vertical = ("types",)
    list_display = (
        "name",
        "published_state",
        "creation_date",
        "modification_date",
    )
    list_filter = ("published",)

    def published_state(self, obj):
        return "✅ Publié" if obj.published else "🔒 Non publié"
