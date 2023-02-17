from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from data.models import Canteen, Teledeclaration
from .diagnostic import DiagnosticInline
from .canteensector import CanteenSectorInline
from .softdeletionadmin import SoftDeletionAdmin, SoftDeletionStatusFilter


class CanteenForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "siret": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "import_source": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "central_producer_siret": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city_insee_code": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "publication_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "quality_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "waste_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "diversification_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "plastics_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "information_comments": forms.Textarea(attrs={"cols": 70, "rows": 3}),
            "creation_mtm_source": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_campaign": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_medium": forms.Textarea(attrs={"cols": 55, "rows": 1}),
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
    inlines = (
        DiagnosticInline,
        CanteenSectorInline,
    )
    fields = (
        "name",
        "siret",
        "creation_date",
        "import_source",
        "logo",
        "city",
        "department",
        "city_insee_code",
        "postal_code",
        "daily_meal_count",
        "yearly_meal_count",
        "satellite_canteens_count",
        "economic_model",
        "line_ministry",
        "managers",
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
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
        "email_no_diagnostic_first_reminder",
        "deletion_date",
    )
    readonly_fields = (
        "creation_date",
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
    )
    list_display = (
        "name",
        "city",
        "publication_status",
        "télédéclarée",
        "creation_date",
        "modification_date",
        "source_des_données",
        "management_type",
        "supprimée",
    )
    filter_vertical = ("managers",)
    list_filter = (
        "publication_status",
        "management_type",
        "production_type",
        "economic_model",
        SoftDeletionStatusFilter,
        "region",
        "department",
        "import_source",
    )
    search_fields = (
        "name",
        "siret",
    )
    if getattr(settings, "ENVIRONMENT", "") != "prod":
        actions = [publish, unpublish]

    def télédéclarée(self, obj):
        if Teledeclaration.objects.filter(
            canteen=obj, year=(timezone.now().year - 1), status=Teledeclaration.TeledeclarationStatus.SUBMITTED
        ).exists():
            return "📩 Télédéclarée"
        return ""

    def source_des_données(self, obj):
        return obj.import_source

    def supprimée(self, obj):
        return "🗑️ Supprimée" if obj.deletion_date else ""


class CanteenInline(admin.TabularInline):
    model = Canteen.managers.through
    readonly_fields = ("canteen", "active")
    extra = 0
    verbose_name_plural = "Cantines gérées"

    def has_add_permission(self, request, obj):
        return False

    def active(self, obj):
        return "🗑️ Supprimée par l'utilisateur" if obj.canteen.deletion_date else "✔️"
