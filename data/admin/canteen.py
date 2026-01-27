from django import forms
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from data.admin.softdeletionadmin import SoftDeletionHistoryAdmin, SoftDeletionStatusFilter
from data.models import Canteen
from data.admin.utils import get_arrayfield_list_filter
from data.models.creation_source import CreationSource

last_year = timezone.now().date().year - 1


class CanteenForm(forms.ModelForm):
    production_type = forms.ChoiceField(
        choices=[
            choice
            for choice in Canteen.ProductionType.choices
            if choice[0] not in [Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING]
        ]
    )

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
    list_display = (
        "name",
        "siret_or_siren_unite_legale_display",
        "city",
        "télédéclarée",
        "groupe",
        "central_producer_siret",
        "management_type",
        "production_type",
        "source_des_données",
        "creation_date",
        "modification_date",
        "deleted",
    )
    list_filter = (
        PublicationStatusFilter,
        "management_type",
        "production_type",
        "economic_model",
        SoftDeletionStatusFilter,
        get_arrayfield_list_filter("sector_list", "Secteur"),
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

    form = CanteenForm
    # inlines = (UserInline, DiagnosticInline,)  # see get_inlines
    autocomplete_fields = ("groupe",)
    filter_vertical = ("managers",)
    fieldsets = (
        (None, {"fields": ("name", "siret", "siren_unite_legale")}),
        ("Informations géographiques", {"fields": Canteen.GEO_FIELDS}),
        (
            "Informations générales",
            {
                "fields": (
                    "daily_meal_count",
                    "yearly_meal_count",
                    "management_type",
                    "production_type",
                    "economic_model",
                    "sector_list",
                    "line_ministry",
                    "central_producer_siret",
                )
            },
        ),
        ("Informations groupe", {"fields": ("groupe", "satellites_display")}),
        (
            "Informations supplémentaires",
            {"fields": ("logo", "is_filled", "publication_status_display", "has_been_claimed")},
        ),
        ("Télédéclaration", {"fields": Canteen.TD_FIELDS}),
        (
            "Lien tracké lors de la création",
            {"fields": Canteen.MATOMO_FIELDS},
        ),
        ("Metadonnées", {"fields": Canteen.CREATION_META_FIELDS}),
        ("Supprimer la cantine", {"fields": ("deletion_date",)}),
    )
    readonly_fields = (
        "satellites_display",
        "is_filled",
        "publication_status_display",
        "has_been_claimed",
        *[field_name for field_name in Canteen.GEO_FIELDS if field_name not in ("city_insee_code",)],
        *Canteen.TD_FIELDS,
        *Canteen.MATOMO_FIELDS,
        *Canteen.CREATION_META_FIELDS,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("groupe")
        return qs

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_inlines(self, request, obj):
        # to avoid circular import error
        from data.admin.diagnostic import DiagnosticInline
        from data.admin.user import UserInline

        return (UserInline, DiagnosticInline)

    def save_model(self, request, obj, form, change):
        """
        - run validation (will be run on save())
        - set creation_source (on create)
        """
        if not change:
            obj.creation_source = CreationSource.ADMIN
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Siret (ou Siren)")
    def siret_or_siren_unite_legale_display(self, obj):
        return obj.siret_or_siren_unite_legale

    # TODO: update every year
    @admin.display(description="Télédéclarée (2025)")
    def télédéclarée(self, obj):
        return obj.declaration_donnees_2025

    télédéclarée.boolean = True

    @admin.display(description="Visible au public")
    def publication_status_display(self, obj):
        return dict(Canteen.PublicationStatus.choices).get(obj.publication_status_display_to_public)

    @admin.display(description="Restaurants satellites")
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
    readonly_fields = ("help",)
    extra = 0
    verbose_name_plural = "Cantines gérées"

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    @admin.display(description="Gestionnaire")
    def help(self, obj):
        return "Pour retirer le gestionnaire de la cantine cochez la case, puis sauvegardez la modification."
