import logging

from django.db.models import Sum
from rest_framework import serializers

from common.utils.badges import badges_for_queryset
from data.models import Canteen, Sector

logger = logging.getLogger(__name__)


def calculate_statistics_canteens(canteens, data):
    data["canteen_count"] = canteens.count()
    # stats per sector categories (group by)
    data["sector_categories"] = {}
    canteen_count_per_sector_categories = canteens.group_and_count_by_field("sectors__category")
    for category in Sector.Categories:
        data["sector_categories"][category] = next(
            (item["count"] for item in canteen_count_per_sector_categories if item["sectors__category"] == category),
            0,
        )
    data["sector_categories"]["inconnu"] = next(
        (item["count"] for item in canteen_count_per_sector_categories if item["sectors__category"] in ["", None]), 0
    )
    # stats per management_type (group by)
    data["management_types"] = {}
    canteen_count_per_management_type = canteens.group_and_count_by_field("management_type")
    for management_type in Canteen.ManagementType:
        data["management_types"][management_type] = next(
            (
                item["count"]
                for item in canteen_count_per_management_type
                if item["management_type"] == management_type
            ),
            0,
        )
    data["management_types"]["inconnu"] = next(
        (item["count"] for item in canteen_count_per_management_type if item["management_type"] in ["", None]), 0
    )
    # stats per production_type (group by)
    data["production_types"] = {}
    canteen_count_per_production_type = canteens.group_and_count_by_field("production_type")
    for production_type in Canteen.ProductionType:
        data["production_types"][production_type] = next(
            (
                item["count"]
                for item in canteen_count_per_production_type
                if item["production_type"] == production_type
            ),
            0,
        )
    data["production_types"]["inconnu"] = next(
        (item["count"] for item in canteen_count_per_production_type if item["production_type"] is None), 0
    )
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
    management_types = serializers.DictField()
    production_types = serializers.DictField()

    @staticmethod
    def calculate_statistics(canteens, teledeclarations):
        data = {}
        data = calculate_statistics_teledeclarations(teledeclarations, data)
        data = calculate_statistics_canteens(canteens, data)
        return data
