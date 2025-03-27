from django.db.models import F, FloatField, Func, Q, Sum
from django.db.models.functions import Cast

from data.department_choices import Department
from data.models import Diagnostic, Sector
from data.region_choices import Region


def badges_for_queryset(diagnostic_year_queryset):
    badge_querysets = {}
    appro_total = diagnostic_year_queryset
    appro_total = diagnostic_year_queryset.count()
    if appro_total:
        appro_share_query = diagnostic_year_queryset.filter(value_total_ht__gt=0)
        appro_share_query = appro_share_query.annotate(
            bio_share=Cast(
                Sum("value_bio_ht", default=0) / Sum("value_total_ht"),
                FloatField(),
            )
        )
        appro_share_query = appro_share_query.annotate(
            combined_share=Cast(
                (
                    Sum("value_bio_ht", default=0)
                    + Sum("value_sustainable_ht", default=0)
                    + Sum("value_externality_performance_ht", default=0)
                    + Sum("value_egalim_others_ht", default=0)
                )
                / Sum("value_total_ht"),
                FloatField(),
            )
        )
        # Saint-Martin should be in group 1
        group_1 = [Region.guadeloupe, Region.martinique, Region.guyane, Region.la_reunion]
        group_2 = [Region.mayotte]
        # should have a group 3 with Saint-Pierre-et-Miquelon
        badge_querysets["appro"] = appro_share_query.filter(
            Q(combined_share__gte=0.5, bio_share__gte=0.2)
            | Q(canteen__region__in=group_1, combined_share__gte=0.2, bio_share__gte=0.05)
            | Q(canteen__department=Department.saint_martin, combined_share__gte=0.2, bio_share__gte=0.05)
            | Q(canteen__region__in=group_2, combined_share__gte=0.05, bio_share__gte=0.02)
            | Q(canteen__department=Department.saint_pierre_et_miquelon, combined_share__gte=0.3, bio_share__gte=0.1)
        ).distinct()

    # waste
    waste_badge_query = diagnostic_year_queryset.filter(has_waste_diagnostic=True)
    waste_badge_query = waste_badge_query.annotate(waste_actions_len=Func(F("waste_actions"), function="CARDINALITY"))
    waste_badge_query = waste_badge_query.filter(waste_actions_len__gt=0)
    waste_badge_query = waste_badge_query.filter(
        Q(canteen__daily_meal_count__lt=3000) | Q(has_donation_agreement=True)
    )
    badge_querysets["waste"] = waste_badge_query

    # diversification
    # TODO : change diversification badge attribution to be homogenous with back_end proprety "diversification_badge".
    diversification_badge_query = diagnostic_year_queryset.exclude(vegetarian_weekly_recurrence__isnull=True)
    diversification_badge_query = diversification_badge_query.exclude(vegetarian_weekly_recurrence="")
    diversification_badge_query = diversification_badge_query.exclude(
        vegetarian_weekly_recurrence=Diagnostic.VegetarianMenuFrequency.LOW
    )
    scolaire_sectors = Sector.objects.filter(category="education")
    if scolaire_sectors.count():
        diversification_badge_query = diversification_badge_query.filter(
            Q(
                canteen__sectors__in=scolaire_sectors,
                vegetarian_weekly_recurrence__in=[
                    Diagnostic.VegetarianMenuFrequency.MID,
                    Diagnostic.VegetarianMenuFrequency.HIGH,
                ],
            )
            | Q(vegetarian_weekly_recurrence=Diagnostic.VegetarianMenuFrequency.DAILY)
        ).distinct()
    badge_querysets["diversification"] = diversification_badge_query

    # plastic
    badge_querysets["plastic"] = diagnostic_year_queryset.filter(
        cooking_plastic_substituted=True,
        serving_plastic_substituted=True,
        plastic_bottles_substituted=True,
        plastic_tableware_substituted=True,
    )

    # info
    badge_querysets["info"] = diagnostic_year_queryset.filter(communicates_on_food_quality=True)
    return badge_querysets
