import logging

from django.db.models import Sum
from rest_framework import serializers

from common.utils.badges import badges_for_queryset
from data.models import Sector

logger = logging.getLogger(__name__)


class CanteenStatisticsSerializer(serializers.Serializer):
    canteenCount = serializers.IntegerField()
    bioPercent = serializers.IntegerField()
    sustainablePercent = serializers.IntegerField()
    diagnosticsCount = serializers.IntegerField()
    approPercent = serializers.IntegerField()
    wastePercent = serializers.IntegerField()
    diversificationPercent = serializers.IntegerField()
    plasticPercent = serializers.IntegerField()
    infoPercent = serializers.IntegerField()
    sectorCategories = serializers.DictField()
    epciError = serializers.CharField(required=False)

    @staticmethod
    def calculate_statistics(canteens, diagnostics):
        data = {"canteenCount": canteens.count(), "diagnosticsCount": diagnostics.count()}

        agg = diagnostics.filter(value_total_ht__gt=0).aggregate(
            Sum("value_bio_ht", default=0),
            Sum("value_total_ht", default=0),
            Sum("value_sustainable_ht", default=0),
            Sum("value_externality_performance_ht", default=0),
            Sum("value_egalim_others_ht", default=0),
        )

        if agg["value_total_ht__sum"] > 0:
            data["bioPercent"] = round(100 * agg["value_bio_ht__sum"] / agg["value_total_ht__sum"])
            data["sustainablePercent"] = round(
                100
                * (
                    agg["value_sustainable_ht__sum"]
                    + agg["value_externality_performance_ht__sum"]
                    + agg["value_egalim_others_ht__sum"]
                )
                / agg["value_total_ht__sum"]
            )
        else:
            data["bioPercent"] = 0
            data["sustainablePercent"] = 0

        badge_querysets = badges_for_queryset(diagnostics)
        total_diag = data["diagnosticsCount"]
        data["approPercent"] = int(badge_querysets["appro"].count() / total_diag * 100) if total_diag else 0
        data["wastePercent"] = int(badge_querysets["waste"].count() / total_diag * 100) if total_diag else 0
        data["diversificationPercent"] = (
            int(badge_querysets["diversification"].count() / total_diag * 100) if total_diag else 0
        )
        data["plasticPercent"] = int(badge_querysets["plastic"].count() / total_diag * 100) if total_diag else 0
        data["infoPercent"] = int(badge_querysets["info"].count() / total_diag * 100) if total_diag else 0

        sector_categories_data = {}
        for category in Sector.Categories:
            sectors = Sector.objects.filter(category=category)
            sector_categories_data[category] = canteens.filter(sectors__in=sectors).count()
        sectors = Sector.objects.filter(category=None)
        sector_categories_data["inconnu"] = canteens.filter(sectors__in=sectors).count()
        data["sectorCategories"] = sector_categories_data

        return data
