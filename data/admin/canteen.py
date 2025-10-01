from django import forms
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from data.models import Canteen
from data.utils import CreationSource

from .diagnostic import DiagnosticInline
from .softdeletionadmin import SoftDeletionHistoryAdmin, SoftDeletionStatusFilter

last_year = timezone.now().date().year - 1


class CanteenForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "city": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "siret": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "siren_unite_legale": forms.Textarea(attrs={"cols": 35, "rows": 1}),
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


class PublicationStatusFilter(admin.SimpleListFilter):
    title = "visible au public ?"

    parameter_name = "visible"

    def lookups(self, request, model_admin):
        return Canteen.PublicationStatus.choices

    def queryset(self, request, queryset):
        if self.value() == Canteen.PublicationStatus.DRAFT:
            return queryset.publicly_hidden()
        elif self.value() == Canteen.PublicationStatus.PUBLISHED:
            return queryset.publicly_visible()
        else:
            return queryset


@admin.register(Canteen)
class CanteenAdmin(SoftDeletionHistoryAdmin):
    form = CanteenForm
    inlines = (DiagnosticInline,)
    fields = (
        "name",
        "siret",
        "siren_unite_legale",
        "creation_date",
        "creation_source",
        "import_source",
        "logo",
        "city",
        "city_insee_code",
        "postal_code",
        "epci",
        "epci_lib",
        "pat_list",
        "pat_lib_list",
        "department",
        "department_lib",
        "region",
        "region_lib",
        "daily_meal_count",
        "yearly_meal_count",
        "satellite_canteens_count",
        "satellites_display",
        "economic_model",
        "sectors",
        "line_ministry",
        "publication_status_display",
        "managers",
        "claimed_by",
        "has_been_claimed",
        "management_type",
        "production_type",
        "central_producer_siret",
        "declaration_donnees_2021",
        "declaration_donnees_2022",
        "declaration_donnees_2023",
        "declaration_donnees_2024",
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
        "epci",
        "epci_lib",
        "pat_list",
        "pat_lib_list",
        "department",
        "department_lib",
        "region",
        "region_lib",
        "creation_date",
        "creation_source",
        "publication_status_display",
        "declaration_donnees_2021",
        "declaration_donnees_2022",
        "declaration_donnees_2023",
        "declaration_donnees_2024",
        "télédéclarée",
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
        "claimed_by",
        "has_been_claimed",
        "satellites_display",
    )
    list_display = (
        "name",
        "siret_or_siren_unite_legale_display",
        "city",
        "télédéclarée",
        "central_producer_siret",
        "production_type",
        "creation_date",
        "modification_date",
        "source_des_données",
        "management_type",
        "deleted",
    )
    filter_vertical = (
        "sectors",
        "managers",
    )
    list_filter = (
        PublicationStatusFilter,
        "management_type",
        "production_type",
        "economic_model",
        SoftDeletionStatusFilter,
        "sectors",
        "region",
        "department",
        "import_source",
    )
    search_fields = (
        "id",
        "name",
        "siret__istartswith",
        "siren_unite_legale__istartswith",
        "central_producer_siret__istartswith",
    )
    search_help_text = "La recherche est faite sur les champs : ID, nom, siret, siren de l'unité légale, siret de la cuisine centrale."

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("teledeclaration_set")
        return qs

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creation_source = CreationSource.ADMIN
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Siret (ou Siren)")
    def siret_or_siren_unite_legale_display(self, obj):
        return obj.siret_or_siren_unite_legale

    @admin.display(description=f"Télédéclarée ({last_year})")
    def télédéclarée(self, obj):
        return obj.get_declaration_donnees_year_display(last_year)

    @admin.display(description="Visible au public")
    def publication_status_display(self, obj):
        return dict(Canteen.PublicationStatus.choices).get(obj.publication_status_display_to_public)

    @admin.display(description="Cantines satellites")
    def satellites_display(self, obj):
        satellites_list = ""
        for satellite in obj.satellites:
            satellites_list += f"<a href='/admin/data/canteen/{satellite.id}/change'>{satellite.name} - {satellite.siret_or_siren_unite_legale}</a><br/>"
        return format_html(satellites_list)

    def source_des_données(self, obj):
        return obj.import_source


class CanteenInline(admin.TabularInline):
    model = Canteen.managers.through
    autocomplete_fields = ("canteen",)
    readonly_fields = ("active", "help")
    extra = 0
    verbose_name_plural = "Cantines gérées"

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    @admin.display(description="Est active")
    def active(self, obj):
        return "🗑️ Supprimée par l'utilisateur" if obj.canteen.deletion_date else "✔️"

    @admin.display(description="Gestionnaire")
    def help(self, obj):
        return "Pour retirer le gestionnaire de la cantine cochez la case, puis sauvegardez la modification."
