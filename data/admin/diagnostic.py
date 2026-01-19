import json

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from data.models import Diagnostic
from data.models.creation_source import CreationSource
from .teledeclaration import TeledeclarationInline


class DiagnosticForm(forms.ModelForm):
    class Meta:
        widgets = {
            "other_waste_action": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "other_waste_comments": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "donation_food_type": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "other_communication_support": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "creation_mtm_source": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_campaign": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_medium": forms.Textarea(attrs={"cols": 55, "rows": 1}),
        }


class DiagnosticInline(admin.TabularInline):
    model = Diagnostic
    show_change_link = True
    fields = ("year", "diagnostic_type", "status", "creation_date", "modification_date")
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Diagnostic)
class DiagnosticAdmin(SimpleHistoryAdmin):
    list_display = (
        "canteen_name",
        "year",
        "diagnostic_type",
        "status",
        "creation_date",
        "modification_date",
    )
    list_filter = ("year", "diagnostic_type", "status", "creation_source")
    search_fields = (
        "id",
        "canteen__name",
        "canteen__siret",
        "canteen__siren_unite_legale",
    )
    search_help_text = "La recherche est faite sur les champs : ID, nom de la cantine, siret, siren de l'unité légale"

    form = DiagnosticForm
    inlines = (TeledeclarationInline,)
    autocomplete_fields = ("canteen",)
    fieldsets = (
        (
            "",
            {
                "fields": (
                    "canteen",
                    "year",
                    "diagnostic_type",
                    "central_kitchen_diagnostic_mode",
                    "status",
                )
            },
        ),
        (
            "Plus de produits de qualité et durables dans nos assiettes",
            {
                "fields": (
                    "tunnel_appro",
                    *Diagnostic.SIMPLE_APPRO_FIELDS,
                )
            },
        ),
        (
            "Lutte contre le gaspillage alimentaire et dons alimentaires",
            {
                "fields": (
                    "tunnel_waste",
                    *Diagnostic.WASTE_FIELDS,
                )
            },
        ),
        (
            "Diversification des sources de protéines et menus végétariens",
            {
                "fields": (
                    "tunnel_diversification",
                    *Diagnostic.DIVERSIFICATION_FIELDS,
                )
            },
        ),
        (
            "Substitution des plastiques",
            {
                "fields": (
                    "tunnel_plastic",
                    *Diagnostic.PLASTIC_FIELDS,
                )
            },
        ),
        (
            "Information des usagers et convives",
            {
                "fields": (
                    "tunnel_info",
                    *Diagnostic.INFO_FIELDS,
                )
            },
        ),
        (
            "Lien tracké lors de la création",
            {"fields": Diagnostic.MATOMO_FIELDS},
        ),
        (
            "Valeurs détaillés",
            {
                "fields": [
                    field_name
                    for field_name in Diagnostic.APPRO_FIELDS
                    if field_name not in Diagnostic.SIMPLE_APPRO_FIELDS
                ]
            },
        ),
        (
            "Télédéclaration",
            {
                "fields": (
                    *Diagnostic.TELEDECLARATION_FIELDS,
                    "applicant",
                    # *Diagnostic.TELEDECLARATION_SNAPSHOT_FIELDS
                    "canteen_snapshot_pretty",
                    "satellites_snapshot_pretty",
                    "applicant_snapshot_pretty",
                )
            },
        ),
        (
            "Metadonnées",
            {"fields": Diagnostic.CREATION_META_FIELDS},
        ),
    )
    readonly_fields = (
        "status",
        *Diagnostic.MATOMO_FIELDS,
        *Diagnostic.TUNNEL_PROGRESS_FIELDS,
        *Diagnostic.TELEDECLARATION_FIELDS,
        "applicant",
        "canteen_snapshot_pretty",
        "satellites_snapshot_pretty",
        "applicant_snapshot_pretty",
        *Diagnostic.CREATION_META_FIELDS,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("canteen")
        return qs

    def save_model(self, request, obj, form, change):
        """
        - run validation (full_clean() is called here, because they are not run on save())
        - set creation_source (on create)
        """
        obj.full_clean()
        if not change:
            obj.creation_source = CreationSource.ADMIN
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return obj and not obj.is_teledeclared

    def has_delete_permission(self, request, obj=None):
        return obj and not obj.is_teledeclared

    def canteen_name(self, obj):
        return obj.canteen.name

    def canteen_snapshot_pretty(self, obj):
        data = json.dumps(obj.canteen_snapshot, indent=2)
        return mark_safe(f"<pre>{data}</pre>")

    canteen_snapshot_pretty.short_description = Diagnostic._meta.get_field("canteen_snapshot").verbose_name

    def satellites_snapshot_pretty(self, obj):
        data = json.dumps(obj.satellites_snapshot, indent=2)
        return mark_safe(f"<pre>{data}</pre>")

    satellites_snapshot_pretty.short_description = Diagnostic._meta.get_field("satellites_snapshot").verbose_name

    def applicant_snapshot_pretty(self, obj):
        data = json.dumps(obj.applicant_snapshot, indent=2)
        return mark_safe(f"<pre>{data}</pre>")

    applicant_snapshot_pretty.short_description = Diagnostic._meta.get_field("applicant_snapshot").verbose_name
