import logging

from django.db.models import Sum
from rest_framework import serializers

from common.utils.badges import badges_for_queryset
from data.models import Sector

logger = logging.getLogger(__name__)


def calculate_statistics_canteens(canteens, data):
    if canteens:
        nbre_canteens = canteens.count()
    else:
        nbre_canteens = 0
    data["canteen_count"] = nbre_canteens
    if canteens:
        sector_categories_data = {}
        for category in Sector.Categories:
            sectors = Sector.objects.filter(category=category)
            sector_categories_data[category] = canteens.filter(sectors__in=sectors).count()
        sectors = Sector.objects.filter(category=None)
        sector_categories_data["inconnu"] = canteens.filter(sectors__in=sectors).count()
        data["sector_categories"] = sector_categories_data
    return data


def calculate_statistics_teledeclarations(teledeclarations, data):
    if teledeclarations:
        nbre_teledeclarations = teledeclarations.count()
    else:
        nbre_teledeclarations = 0
    data["teledeclarations_count"] = nbre_teledeclarations

    if nbre_teledeclarations:
        agg = teledeclarations.aggregate(
            Sum("value_bio_ht_agg", default=0),
            Sum("value_total_ht", default=0),
            Sum("value_sustainable_ht_agg", default=0),
            Sum("value_externality_performance_ht_agg", default=0),
            Sum("value_egalim_others_ht_agg", default=0),
        )

        if agg["value_total_ht__sum"] > 0:
            data["bio_percent"] = round(100 * agg["value_bio_ht_agg__sum"] / agg["value_total_ht__sum"])
            data["sustainable_percent"] = round(
                100
                * (
                    agg["value_sustainable_ht_agg__sum"]
                    + agg["value_externality_performance_ht_agg__sum"]
                    + agg["value_egalim_others_ht_agg__sum"]
                )
                / agg["value_total_ht__sum"]
            )
        else:
            data["bio_percent"] = 0
            data["sustainable_percent"] = 0
    else:
        data["bio_percent"] = 0
        data["sustainable_percent"] = 0

    badge_querysets = badges_for_queryset(teledeclarations)
    total_diag = data["teledeclarations_count"]
    data["approPercent"] = int(badge_querysets["appro"].count() / total_diag * 100) if total_diag else 0
    return data


class CanteenStatisticsSerializer(serializers.Serializer):
    canteen_count = serializers.IntegerField()
    bio_percent = serializers.IntegerField()
    sustainable_percent = serializers.IntegerField()
    teledeclarations_count = serializers.IntegerField()
    approPercent = serializers.IntegerField()
    sector_categories = serializers.DictField()
    epci_error = serializers.CharField(required=False)

    @staticmethod
    def calculate_statistics(canteens, teledeclarations):
        data = {}
        data = calculate_statistics_teledeclarations(teledeclarations, data)
        data = calculate_statistics_canteens(canteens, data)
        return data
