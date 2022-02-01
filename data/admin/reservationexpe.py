from django.contrib import admin
from data.models import ReservationExpe


class ReservationExpeParticipantFilter(admin.SimpleListFilter):
    title = "Participant à l'experimentation"
    parameter_name = "canteen.reservation_expe_participant"

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


@admin.register(ReservationExpe)
class ReservationExpeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "",
            {
                "fields": (
                    "canteen",
                    "has_reservation_system",
                    "reservation_system_start_date",
                    "experimentation_start_date",
                    "reservation_system_description",
                    "publicise_method",
                    "has_leader",
                    "leader_first_name",
                    "leader_last_name",
                    "leader_email",
                    "has_regulations",
                    "has_committee",
                )
            },
        ),
        (
            "t0",
            {
                "fields": (
                    "avg_weight_not_served_t0",
                    "avg_weight_leftover_t0",
                    "ratio_edible_non_edible_t0",
                    "avg_weight_preparation_leftover_t0",
                    "avg_weight_bread_leftover_t0",
                    "avg_attendance_from_evaluation_t0",
                    "solution_use_rate_t0",
                    "satisfaction_t0",
                    "comments_t0",
                )
            },
        ),
        (
            "t1",
            {
                "fields": (
                    "avg_weight_not_served_t1",
                    "avg_weight_leftover_t1",
                    "ratio_edible_non_edible_t1",
                    "avg_weight_preparation_leftover_t1",
                    "avg_weight_bread_leftover_t1",
                    "avg_attendance_from_evaluation_t1",
                    "solution_use_rate_t1",
                    "satisfaction_t1",
                    "comments_t1",
                )
            },
        ),
        (
            "t2",
            {
                "fields": (
                    "avg_weight_not_served_t2",
                    "avg_weight_leftover_t2",
                    "ratio_edible_non_edible_t2",
                    "avg_weight_preparation_leftover_t2",
                    "avg_weight_bread_leftover_t2",
                    "avg_attendance_from_evaluation_t2",
                    "solution_use_rate_t2",
                    "satisfaction_t2",
                    "comments_t2",
                    "system_cost",
                    "participation_cost",
                    "participation_cost_details",
                    "money_saved",
                )
            },
        ),
    )

    list_display = (
        "canteen_name",
        "creation_date",
        "has_reservation_system",
    )

    list_filter = (ReservationExpeParticipantFilter,)

    def canteen_name(self, obj):
        return obj.canteen.name
