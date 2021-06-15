from django import forms
from django.contrib import admin
from data.models import Diagnostic


class DiagnosticForm(forms.ModelForm):
    class Meta:
        widgets = {
            "other_waste_action": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "other_waste_comments": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "donation_food_type": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "other_communication_support": forms.Textarea(
                attrs={"cols": 60, "rows": 2}
            ),
        }


class DiagnosticInline(admin.TabularInline):
    model = Diagnostic
    show_change_link = True
    fields = ("year", "creation_date")
    readonly_fields = fields
    extra = 0


@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):

    form = DiagnosticForm
    list_display = (
        "canteen_name",
        "year",
        "creation_date",
        "modification_date",
    )
    list_filter = ("year",)

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
            "Au moins 50% de produits de qualité et durables dont 20% de bio",
            {
                "fields": (
                    "value_bio_ht",
                    "value_fair_trade_ht",
                    "value_sustainable_ht",
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
    )

    def canteen_name(self, obj):
        return obj.canteen.name
