from django.db.models import F, FloatField, Q, Sum
from django.db.models.functions import Cast

from data.department_choices import Department
from data.region_choices import Region


def badges_for_queryset(teledeclaration_year_queryset):
    badge_querysets = {}
    appro_total = teledeclaration_year_queryset
    if appro_total:
        appro_total = teledeclaration_year_queryset.count()
        appro_share_query = teledeclaration_year_queryset.annotate(
            bio_share=Cast(Sum("value_bio_ht_agg", default=0), FloatField())
            / Cast(Sum("value_total_ht"), FloatField())
        )
        teledeclaration_year_queryset.annotate(bio_share=F("value_bio_ht_agg") / F("value_total_ht"))
        appro_share_query = appro_share_query.annotate(
            combined_share=Cast(
                Sum("value_bio_ht_agg", default=0)
                + Sum("value_sustainable_ht_agg", default=0)
                + Sum("value_externality_performance_ht_agg", default=0)
                + Sum("value_egalim_others_ht_agg", default=0),
                FloatField(),
            )
            / Cast(Sum("value_total_ht"), FloatField()),
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
    return badge_querysets
