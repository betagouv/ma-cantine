from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from common.utils import send_mail
import urllib.parse
from data.models import Canteen, Teledeclaration
from .diagnostic import DiagnosticInline
from .softdeletionadmin import SoftDeletionAdmin, SoftDeletionStatusFilter


class CanteenForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "siret": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "central_producer_siret": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city_insee_code": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "publication_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "quality_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "waste_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "diversification_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "plastics_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "information_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
        }


@admin.action(description="Publier cantines")
def publish(modeladmin, request, queryset):
    queryset.update(publication_status=Canteen.PublicationStatus.PUBLISHED)


@admin.action(description="Marquer cantines non publiées")
def unpublish(modeladmin, request, queryset):
    queryset.update(publication_status=Canteen.PublicationStatus.DRAFT)


@admin.register(Canteen)
class CanteenAdmin(SoftDeletionAdmin):

    form = CanteenForm
    inlines = (DiagnosticInline,)
    fields = (
        "name",
        "logo",
        "city",
        "department",
        "city_insee_code",
        "postal_code",
        "daily_meal_count",
        "satellite_canteens_count",
        "economic_model",
        "sectors",
        "line_ministry",
        "managers",
        "siret",
        "management_type",
        "production_type",
        "central_producer_siret",
        "publication_status",
        "publication_comments",
        "quality_comments",
        "waste_comments",
        "diversification_comments",
        "plastics_comments",
        "information_comments",
        "deletion_date",
    )
    list_display = (
        "name",
        "city",
        "publication_status",
        "télédéclarée",
        "creation_date",
        "modification_date",
        "management_type",
        "supprimée",
    )
    filter_vertical = (
        "sectors",
        "managers",
    )
    list_filter = (
        "publication_status",
        "sectors",
        "management_type",
        "production_type",
        SoftDeletionStatusFilter,
        "region",
        "department",
    )
    search_fields = ("name",)
    if getattr(settings, "ENVIRONMENT", "") != "prod":
        actions = [publish, unpublish]

    def télédéclarée(self, obj):
        if Teledeclaration.objects.filter(
            canteen=obj, year=(timezone.now().year - 1), status=Teledeclaration.TeledeclarationStatus.SUBMITTED
        ).exists():
            return "📩 Télédéclarée"
        return ""

    def supprimée(self, obj):
        return "🗑️ Supprimée" if obj.deletion_date else ""

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and "publication_status" in form.changed_data and obj.publication_status == "published":
            protocol = "https" if settings.SECURE else "http"
            canteenUrlComponent = urllib.parse.quote(f"{obj.id}--{obj.name}")
            context = {
                "canteen": obj.name,
                "canteenUrl": f"{protocol}://{settings.HOSTNAME}/nos-cantines/{canteenUrlComponent}",
            }
            contact_list = [user.email for user in obj.managers.all()]
            contact_list.append(settings.CONTACT_EMAIL)
            send_mail(
                subject=f"Votre cantine « {obj.name} » est publiée",
                template="canteen_published",
                context=context,
                to=contact_list,
                fail_silently=True,
            )


class CanteenInline(admin.TabularInline):
    model = Canteen.managers.through
    readonly_fields = ("canteen", "active")
    extra = 0
    verbose_name_plural = "Cantines gérées"

    def has_add_permission(self, request, obj):
        return False

    def active(self, obj):
        return "🗑️ Supprimée par l'utilisateur" if obj.canteen.deletion_date else "✔️"
