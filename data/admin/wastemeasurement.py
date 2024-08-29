from django.contrib import admin
from data.models import WasteMeasurement
from simple_history.admin import SimpleHistoryAdmin


@admin.register(WasteMeasurement)
class WasteMeasurementAdmin(SimpleHistoryAdmin):
    list_display = (
        "canteen",
        "period_start_date",
        "period_end_date",
        "meal_count",
        "total_mass",
        "is_sorted_by_source",
    )
    search_fields = (
        "canteen__name",
        "canteen__siret",
    )

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "canteen",
                    "period_start_date",
                    "period_end_date",
                    "meal_count",
                    "total_mass",
                    "is_sorted_by_source",
                )
            },
        ),
        (
            "Excédentes de préparation",
            {
                "fields": (
                    "preparation_total_mass",
                    "preparation_is_sorted",
                    "preparation_edible_mass",
                    "preparation_inedible_mass",
                )
            },
        ),
        (
            "Denrées présentées aux convives mais non servies",
            {
                "fields": (
                    "unserved_total_mass",
                    "unserved_is_sorted",
                    "unserved_edible_mass",
                    "unserved_inedible_mass",
                )
            },
        ),
        (
            "Excédentes reste assiette",
            {
                "fields": (
                    "leftovers_total_mass",
                    "leftovers_is_sorted",
                    "leftovers_edible_mass",
                    "leftovers_inedible_mass",
                )
            },
        ),
    )
