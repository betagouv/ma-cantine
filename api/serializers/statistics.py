import logging

from django.db.models import Sum
from rest_framework import serializers

from common.utils.badges import badges_for_queryset
from data.models import Canteen, Sector

logger = logging.getLogger(__name__)


def calculate_statistics_canteens(canteens, data):
    data["canteen_count"] = canteens.count()
    # stats: group by & count some fields
    GROUP_BY_FIELDS = [
        ("sectors__category", Sector.Categories, "sector_categories"),
        ("management_type", Canteen.ManagementType, "management_types"),
        ("production_type", Canteen.ProductionType, "production_types"),
        ("economic_model", Canteen.EconomicModel, "economic_models"),
    ]
    for field_name_input, field_enum, field_name_output in GROUP_BY_FIELDS:
        data[field_name_output] = {}
        canteen_count_per_field = canteens.group_and_count_by_field(field_name_input)
        for field_enum_value in field_enum:
            data[field_name_output][field_enum_value] = next(
                (item["count"] for item in canteen_count_per_field if item[field_name_input] == field_enum_value), 0
            )
        data[field_name_output]["inconnu"] = next(
            (item["count"] for item in canteen_count_per_field if item[field_name_input] in ["", None]), 0
        )
    # return
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
    economic_models = serializers.DictField()

    @staticmethod
    def calculate_statistics(canteens, teledeclarations):
        data = {}
        data = calculate_statistics_teledeclarations(teledeclarations, data)
        data = calculate_statistics_canteens(canteens, data)
        return data
