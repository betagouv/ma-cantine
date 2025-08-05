from django.db.models import Q

from data.department_choices import Department
from data.region_choices import Region
from macantine.utils import EGALIM_OBJECTIVES


def badges_for_queryset(teledeclaration_year_queryset):
    badge_querysets = {}
    if teledeclaration_year_queryset:
        # Avoid division by zero for TD with value_total_ht < 1, rounded to 0 when casting as int
        teledeclaration_year_queryset = teledeclaration_year_queryset.filter(value_total_ht__gt=0)
        # Calculate the share of bio & egalim
        teledeclaration_year_queryset = teledeclaration_year_queryset.with_appro_percent_stats()
        # Saint-Martin should be in group 1
        group_1 = [Region.guadeloupe, Region.martinique, Region.guyane, Region.la_reunion]
        group_2 = [Region.mayotte]
        # should have a group 3 with Saint-Pierre-et-Miquelon
        badge_querysets["appro"] = teledeclaration_year_queryset.filter(
            Q(
                egalim_percent__gte=EGALIM_OBJECTIVES["egalim_percent"],
                bio_percent__gte=EGALIM_OBJECTIVES["bio_percent"],
            )
            | Q(canteen__region__in=group_1, egalim_percent__gte=20, bio_percent__gte=5)
            | Q(canteen__department=Department.saint_martin, egalim_percent__gte=20, bio_percent__gte=5)
            | Q(canteen__region__in=group_2, egalim_percent__gte=5, bio_percent__gte=2)
            | Q(canteen__department=Department.saint_pierre_et_miquelon, egalim_percent__gte=30, bio_percent__gte=10)
        ).distinct()
    return badge_querysets
