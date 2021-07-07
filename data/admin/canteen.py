from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from data.models import Canteen
from .diagnostic import DiagnosticInline
from .softdeletionadmin import SoftDeletionAdmin


class CanteenForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "siret": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city_insee_code": forms.Textarea(attrs={"cols": 35, "rows": 1}),
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
        "city_insee_code",
        "postal_code",
        "daily_meal_count",
        "sectors",
        "managers",
        "siret",
        "management_type",
        "production_type",
        "publication_status",
        "deletion_date",
    )
    list_display = (
        "name",
        "city",
        "publication_status",
        "creation_date",
        "modification_date",
        "management_type",
        "supprimée",
    )
    filter_vertical = (
        "sectors",
        "managers",
    )
    list_filter = ("publication_status", "sectors", "management_type", "production_type", "city")

    def supprimée(self, obj):
        return "🗑️ Supprimée" if obj.deletion_date else ""

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and "publication_status" in form.changed_data and obj.publication_status == "published":
            protocol = "https" if settings.SECURE else "http"
            canteens_url = "{}://{}/nos-cantines/".format(protocol, settings.HOSTNAME)
            contact_list = [user.email for user in obj.managers.all()]
            contact_list.append(settings.CONTACT_EMAIL)
            send_mail(
                f"Votre cantine « {obj.name} » est publiée",
                # TODO: improve template
                f"""La cantine « {obj.name} » est publiée.\n
                La cantine est maintenant visible ici : {canteens_url}""",
                settings.DEFAULT_FROM_EMAIL,
                contact_list,
                fail_silently=True,
            )

