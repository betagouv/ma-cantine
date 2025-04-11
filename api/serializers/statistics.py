import logging

from django.db.models import Sum
from rest_framework import serializers

from common.utils.badges import badges_for_queryset
from data.models import Sector

logger = logging.getLogger(__name__)


class CanteenStatisticsSerializer(serializers.Serializer):
    canteen_count = serializers.IntegerField()
    bio_percent = serializers.IntegerField()
    sustainable_percent = serializers.IntegerField()
    diagnostics_count = serializers.IntegerField()
    approPercent = serializers.IntegerField()
    sector_categories = serializers.DictField()
    epci_error = serializers.CharField(required=False)

    @staticmethod
    def calculate_statistics(canteens, diagnostics):
        data = {"canteen_count": canteens.count(), "diagnostics_count": diagnostics.count()}

        agg = diagnostics.is_filled().aggregate(
            Sum("value_bio_ht", default=0),
            Sum("value_total_ht", default=0),
            Sum("value_sustainable_ht", default=0),
            Sum("value_externality_performance_ht", default=0),
            Sum("value_egalim_others_ht", default=0),
        )

        if agg["value_total_ht__sum"] > 0:
            data["bio_percent"] = round(100 * agg["value_bio_ht__sum"] / agg["value_total_ht__sum"])
            data["sustainable_percent"] = round(
                100
                * (
                    agg["value_sustainable_ht__sum"]
                    + agg["value_externality_performance_ht__sum"]
                    + agg["value_egalim_others_ht__sum"]
                )
                / agg["value_total_ht__sum"]
            )
        else:
            data["bio_percent"] = 0
            data["sustainable_percent"] = 0

        badge_querysets = badges_for_queryset(diagnostics)
        total_diag = data["diagnostics_count"]
        data["approPercent"] = int(badge_querysets["appro"].count() / total_diag * 100) if total_diag else 0

        sector_categories_data = {}
        for category in Sector.Categories:
            sectors = Sector.objects.filter(category=category)
            sector_categories_data[category] = canteens.filter(sectors__in=sectors).count()
        sectors = Sector.objects.filter(category=None)
        sector_categories_data["inconnu"] = canteens.filter(sectors__in=sectors).count()
        data["sector_categories"] = sector_categories_data

        return data
