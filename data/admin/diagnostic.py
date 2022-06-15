from django import forms
from django.contrib import admin
from data.models import Diagnostic
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
    fields = ("year", "creation_date")
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):

    form = DiagnosticForm
    inlines = (TeledeclarationInline,)
    list_display = (
        "canteen_name",
        "year",
        "creation_date",
        "modification_date",
    )
    list_filter = ("year",)
    readonly_fields = ("creation_mtm_source", "creation_mtm_campaign", "creation_mtm_medium")

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "canteen",
                    "year",
                )
            },
        ),
        (
            "Plus de produits de qualité et durables dans nos assiettes",
            {
                "fields": (
                    "value_bio_ht",
                    "value_fair_trade_ht",
                    "value_sustainable_ht",
                    "value_label_rouge",
                    "value_label_aoc_igp",
                    "value_label_hve",
                    "value_pat_ht",
                    "value_total_ht",
                )
            },
        ),
        (
            "Lutte contre le gaspillage alimentaire et dons alimentaires",
            {
                "fields": (
                    "has_waste_diagnostic",
                    "has_waste_plan",
                    "waste_actions",
                    "other_waste_action",
                    "has_donation_agreement",
                    "bread_leftovers",
                    "served_leftovers",
                    "unserved_leftovers",
                    "side_leftovers",
                    "donation_frequency",
                    "donation_quantity",
                    "donation_food_type",
                    "other_waste_comments",
                )
            },
        ),
        (
            "Diversification des sources de protéines et menus végétariens",
            {
                "fields": (
                    "has_diversification_plan",
                    "diversification_plan_actions",
                    "vegetarian_weekly_recurrence",
                    "vegetarian_menu_type",
                    "vegetarian_menu_bases",
                )
            },
        ),
        (
            "Substitution des plastiques",
            {
                "fields": (
                    "cooking_plastic_substituted",
                    "serving_plastic_substituted",
                    "plastic_bottles_substituted",
                    "plastic_tableware_substituted",
                )
            },
        ),
        (
            "Information des usagers et convives",
            {
                "fields": (
                    "communication_supports",
                    "other_communication_support",
                    "communication_support_url",
                    "communicates_on_food_plan",
                    "communicates_on_food_quality",
                    "communication_frequency",
                )
            },
        ),
        (
            "Lien tracké lors de la création",
            {
                "fields": (
                    "creation_mtm_source",
                    "creation_mtm_campaign",
                    "creation_mtm_medium",
                )
            },
        ),
        (
            "Valeurs détaillés",
            {
                "fields": (
                    "viandes_volailles_bio",
                    "produits_de_la_mer_bio",
                    "produits_laitiers_bio",
                    "boulangerie_bio",
                    "boissons_bio",
                    "autres_bio",
                    "viandes_volailles_label_rouge",
                    "produits_de_la_mer_label_rouge",
                    "produits_laitiers_label_rouge",
                    "boulangerie_label_rouge",
                    "boissons_label_rouge",
                    "autres_label_rouge",
                    "viandes_volailles_aocaop_igp_stg",
                    "produits_de_la_mer_aocaop_igp_stg",
                    "produits_laitiers_aocaop_igp_stg",
                    "boulangerie_aocaop_igp_stg",
                    "boissons_aocaop_igp_stg",
                    "autres_aocaop_igp_stg",
                    "viandes_volailles_hve",
                    "produits_de_la_mer_hve",
                    "produits_laitiers_hve",
                    "boulangerie_hve",
                    "boissons_hve",
                    "autres_hve",
                    "viandes_volailles_peche_durable",
                    "produits_de_la_mer_peche_durable",
                    "produits_laitiers_peche_durable",
                    "boulangerie_peche_durable",
                    "boissons_peche_durable",
                    "autres_peche_durable",
                    "viandes_volailles_rup",
                    "produits_de_la_mer_rup",
                    "produits_laitiers_rup",
                    "boulangerie_rup",
                    "boissons_rup",
                    "autres_rup",
                    "viandes_volailles_fermier",
                    "produits_de_la_mer_fermier",
                    "produits_laitiers_fermier",
                    "boulangerie_fermier",
                    "boissons_fermier",
                    "autres_fermier",
                    "viandes_volailles_externalites",
                    "produits_de_la_mer_externalites",
                    "produits_laitiers_externalites",
                    "boulangerie_externalites",
                    "boissons_externalites",
                    "autres_externalites",
                    "viandes_volailles_commerce_equitable",
                    "produits_de_la_mer_commerce_equitable",
                    "produits_laitiers_commerce_equitable",
                    "boulangerie_commerce_equitable",
                    "boissons_commerce_equitable",
                    "autres_commerce_equitable",
                    "viandes_volailles_performance",
                    "produits_de_la_mer_performance",
                    "produits_laitiers_performance",
                    "boulangerie_performance",
                    "boissons_performance",
                    "autres_performance",
                    "viandes_volailles_equivalents",
                    "produits_de_la_mer_equivalents",
                    "produits_laitiers_equivalents",
                    "boulangerie_equivalents",
                    "boissons_equivalents",
                    "autres_equivalents",
                    "viandes_volailles_france",
                    "produits_de_la_mer_france",
                    "produits_laitiers_france",
                    "boulangerie_france",
                    "boissons_france",
                    "autres_france",
                    "viandes_volailles_short_distribution",
                    "produits_de_la_mer_short_distribution",
                    "produits_laitiers_short_distribution",
                    "boulangerie_short_distribution",
                    "boissons_short_distribution",
                    "autres_short_distribution",
                    "viandes_volailles_local",
                    "produits_de_la_mer_local",
                    "produits_laitiers_local",
                    "boulangerie_local",
                    "boissons_local",
                    "autres_local",
                )
            },
        ),
    )

    search_fields = ("canteen__name",)

    def canteen_name(self, obj):
        return obj.canteen.name
