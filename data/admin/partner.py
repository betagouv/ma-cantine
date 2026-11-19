from django import forms
from django.contrib import admin

from data.admin.utils import get_arrayfield_list_filter
from data.models import Partner


class PartnerForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "short_description": forms.Textarea(attrs={"cols": 55, "rows": 2}),
            "contact_name": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "contact_message": forms.Textarea(attrs={"cols": 55, "rows": 2}),
        }


@admin.action(description="Publier partenaires")
def publish(modeladmin, request, queryset):
    queryset.update(published=True)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "published_state",
        "creation_date",
        "modification_date",
    )
    list_filter = ("published", get_arrayfield_list_filter("type_list", "Type d'acteur"), "sector_categories")
    actions = [publish]

    form = PartnerForm
    fields = (
        "name",
        "categories",
        "short_description",
        "long_description",
        "image",
        "website",
        "type_list",
        "national",
        "departments",
        "sector_categories",
        "gratuity_option",
        "economic_model",
        "published",
        "contact_name",
        "contact_email",
        "contact_message",
        "contact_phone_number",
    )

    def published_state(self, obj):
        return "✅ Publié" if obj.published else "🔒 Non publié"
