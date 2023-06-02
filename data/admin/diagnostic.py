from django import forms
from django.contrib import admin
from data.models import Diagnostic
from simple_history.admin import SimpleHistoryAdmin
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
class DiagnosticAdmin(SimpleHistoryAdmin):
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
    raw_id_fields = ("canteen",)

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "canteen",
                    "year",
                    "diagnostic_type",
                    "central_kitchen_diagnostic_mode",
                )
            },
        ),
        (
            "Plus de produits de qualité et durables dans nos assiettes",
            {
                "fields": (
                    "value_total_ht",
                    "value_bio_ht",
                    "value_sustainable_ht",
                    "value_externality_performance_ht",
                    "value_egalim_others_ht",
                    "value_meat_poultry_ht",
                    "value_meat_poultry_egalim_ht",
                    "value_meat_poultry_france_ht",
                    "value_fish_ht",
                    "value_fish_egalim_ht",
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
                    "value_viandes_volailles_bio",
                    "value_produits_de_la_mer_bio",
                    "value_fruits_et_legumes_bio",
                    "value_charcuterie_bio",
                    "value_produits_laitiers_bio",
                    "value_boulangerie_bio",
                    "value_boissons_bio",
                    "value_autres_bio",
                    "value_viandes_volailles_label_rouge",
                    "value_produits_de_la_mer_label_rouge",
                    "value_fruits_et_legumes_label_rouge",
                    "value_charcuterie_label_rouge",
                    "value_produits_laitiers_label_rouge",
                    "value_boulangerie_label_rouge",
                    "value_boissons_label_rouge",
                    "value_autres_label_rouge",
                    "value_viandes_volailles_aocaop_igp_stg",
                    "value_produits_de_la_mer_aocaop_igp_stg",
                    "value_fruits_et_legumes_aocaop_igp_stg",
                    "value_charcuterie_aocaop_igp_stg",
                    "value_produits_laitiers_aocaop_igp_stg",
                    "value_boulangerie_aocaop_igp_stg",
                    "value_boissons_aocaop_igp_stg",
                    "value_autres_aocaop_igp_stg",
                    "value_viandes_volailles_hve",
                    "value_produits_de_la_mer_hve",
                    "value_fruits_et_legumes_hve",
                    "value_charcuterie_hve",
                    "value_produits_laitiers_hve",
                    "value_boulangerie_hve",
                    "value_boissons_hve",
                    "value_autres_hve",
                    "value_viandes_volailles_peche_durable",
                    "value_produits_de_la_mer_peche_durable",
                    "value_fruits_et_legumes_peche_durable",
                    "value_charcuterie_peche_durable",
                    "value_produits_laitiers_peche_durable",
                    "value_boulangerie_peche_durable",
                    "value_boissons_peche_durable",
                    "value_autres_peche_durable",
                    "value_viandes_volailles_rup",
                    "value_produits_de_la_mer_rup",
                    "value_fruits_et_legumes_rup",
                    "value_charcuterie_rup",
                    "value_produits_laitiers_rup",
                    "value_boulangerie_rup",
                    "value_boissons_rup",
                    "value_autres_rup",
                    "value_viandes_volailles_commerce_equitable",
                    "value_produits_de_la_mer_commerce_equitable",
                    "value_fruits_et_legumes_commerce_equitable",
                    "value_charcuterie_commerce_equitable",
                    "value_produits_laitiers_commerce_equitable",
                    "value_boulangerie_commerce_equitable",
                    "value_boissons_commerce_equitable",
                    "value_autres_commerce_equitable",
                    "value_viandes_volailles_fermier",
                    "value_produits_de_la_mer_fermier",
                    "value_fruits_et_legumes_fermier",
                    "value_charcuterie_fermier",
                    "value_produits_laitiers_fermier",
                    "value_boulangerie_fermier",
                    "value_boissons_fermier",
                    "value_autres_fermier",
                    "value_viandes_volailles_externalites",
                    "value_produits_de_la_mer_externalites",
                    "value_fruits_et_legumes_externalites",
                    "value_charcuterie_externalites",
                    "value_produits_laitiers_externalites",
                    "value_boulangerie_externalites",
                    "value_boissons_externalites",
                    "value_autres_externalites",
                    "value_viandes_volailles_performance",
                    "value_produits_de_la_mer_performance",
                    "value_fruits_et_legumes_performance",
                    "value_charcuterie_performance",
                    "value_produits_laitiers_performance",
                    "value_boulangerie_performance",
                    "value_boissons_performance",
                    "value_autres_performance",
                    "value_viandes_volailles_non_egalim",
                    "value_produits_de_la_mer_non_egalim",
                    "value_fruits_et_legumes_non_egalim",
                    "value_charcuterie_non_egalim",
                    "value_produits_laitiers_non_egalim",
                    "value_boulangerie_non_egalim",
                    "value_boissons_non_egalim",
                    "value_autres_non_egalim",
                    "value_viandes_volailles_france",
                    "value_produits_de_la_mer_france",
                    "value_fruits_et_legumes_france",
                    "value_charcuterie_france",
                    "value_produits_laitiers_france",
                    "value_boulangerie_france",
                    "value_boissons_france",
                    "value_autres_france",
                    "value_viandes_volailles_short_distribution",
                    "value_produits_de_la_mer_short_distribution",
                    "value_fruits_et_legumes_short_distribution",
                    "value_charcuterie_short_distribution",
                    "value_produits_laitiers_short_distribution",
                    "value_boulangerie_short_distribution",
                    "value_boissons_short_distribution",
                    "value_autres_short_distribution",
                    "value_viandes_volailles_local",
                    "value_produits_de_la_mer_local",
                    "value_fruits_et_legumes_local",
                    "value_charcuterie_local",
                    "value_produits_laitiers_local",
                    "value_boulangerie_local",
                    "value_boissons_local",
                    "value_autres_local",
                )
            },
        ),
    )

    search_fields = (
        "canteen__name",
        "canteen__siret",
    )

    def canteen_name(self, obj):
        return obj.canteen.name
