from django.contrib import admin
from data.models import VegetarianExpe


class VegetarianExpeParticipantFilter(admin.SimpleListFilter):
    title = "Participant à l'experimentation"
    parameter_name = "canteen.vegetarian_expe_participant"

    def lookups(self, request, model_admin):
        return (
            (None, "Participants"),
            ("non-participants", "Ne participent pas"),
            ("all", "Tous"),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": cl.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter(canteen__reservation_expe_participant=True)
        elif self.value() in ("all"):
            return queryset
        elif self.value() in ("non-participants"):
            return queryset.filter(canteen__reservation_expe_participant=False)


@admin.register(VegetarianExpe)
class VegetarianExpeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "",
            {
                "fields": (
                    "canteen",
                    "has_daily_vegetarian_offer",
                    "daily_vegetarian_offer_start_date",
                    "experimentation_start_date",
                )
            },
        ),
        (
            "t0",
            {
                "fields": (
                    "vegetarian_menu_percentage_t0",
                    "eggs_composition_t0",
                    "cheese_composition_t0",
                    "soy_composition_home_made_t0",
                    "soy_composition_ready_t0",
                    "soyless_composition_home_made_t0",
                    "soyless_composition_ready_t0",
                    "cereal_legume_composition_t0",
                    "waste_evolution_t0",
                    "waste_evolution_percentage_t0",
                    "waste_vegetarian_not_served_t0",
                    "waste_vegetarian_components_t0",
                    "waste_non_vegetarian_not_served_t0",
                    "waste_non_vegetarian_components_t0",
                    "attendance_evolution_t0",
                    "attendance_evolution_percentage_t0",
                    "vegetarian_cost_t0",
                    "non_vegetarian_cost_t0",
                    "cost_evolution_t0",
                    "cost_evolution_percentage_t0",
                    "satisfaction_guests_t0",
                    "satisfaction_guests_reasons_t0",
                    "satisfaction_staff_t0",
                    "satisfaction_staff_reasons_t0",
                    "has_used_recipee_documents_t0",
                    "training_t0",
                )
            },
        ),
        (
            "t1",
            {
                "fields": (
                    "vegetarian_menu_percentage_t1",
                    "eggs_composition_t1",
                    "cheese_composition_t1",
                    "soy_composition_home_made_t1",
                    "soy_composition_ready_t1",
                    "soyless_composition_home_made_t1",
                    "soyless_composition_ready_t1",
                    "cereal_legume_composition_t1",
                    "waste_evolution_t1",
                    "waste_evolution_percentage_t1",
                    "waste_vegetarian_not_served_t1",
                    "waste_vegetarian_components_t1",
                    "waste_non_vegetarian_not_served_t1",
                    "waste_non_vegetarian_components_t1",
                    "attendance_evolution_t1",
                    "attendance_evolution_percentage_t1",
                    "vegetarian_cost_t1",
                    "non_vegetarian_cost_t1",
                    "cost_evolution_t1",
                    "cost_evolution_percentage_t1",
                    "satisfaction_guests_t1",
                    "satisfaction_guests_reasons_t1",
                    "satisfaction_staff_t1",
                    "satisfaction_staff_reasons_t1",
                    "has_used_recipee_documents_t1",
                    "training_t1",
                )
            },
        ),
    )

    list_display = (
        "canteen_name",
        "creation_date",
        "has_daily_vegetarian_offer",
    )

    list_filter = (VegetarianExpeParticipantFilter,)

    def canteen_name(self, obj):
        return obj.canteen.name
