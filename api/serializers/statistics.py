import logging

from django.db.models import Count, FloatField, Sum
from django.db.models.fields.json import KT
from django.db.models.functions import Cast
from rest_framework import serializers

from common.utils.badges import badges_for_queryset
from data.models import Canteen, Sector

logger = logging.getLogger(__name__)


def calculate_statistics_canteens(canteens, data):
    # count
    data["canteen_count"] = canteens.count()
    # group by
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
    # aggregate
    agg = teledeclarations.annotate(
        value_meat_poultry_ht=Cast(
            KT("declared_data__teledeclaration__value_meat_poultry_ht"), output_field=FloatField()
        ),
        value_meat_poultry_egalim_ht=Cast(
            KT("declared_data__teledeclaration__value_meat_poultry_egalim_ht"), output_field=FloatField()
        ),
        value_meat_poultry_france_ht=Cast(
            KT("declared_data__teledeclaration__value_meat_poultry_france_ht"), output_field=FloatField()
        ),
        value_fish_ht=Cast(KT("declared_data__teledeclaration__value_fish_ht"), output_field=FloatField()),
        value_fish_egalim_ht=Cast(
            KT("declared_data__teledeclaration__value_fish_egalim_ht"), output_field=FloatField()
        ),
    ).aggregate(
        Count("id"),
        Sum("value_bio_ht_agg", default=0),
        Sum("value_total_ht", default=0),
        Sum("value_sustainable_ht_agg", default=0),
        Sum("value_externality_performance_ht_agg", default=0),
        Sum("value_egalim_others_ht_agg", default=0),
        Sum("value_meat_poultry_ht", default=0),
        Sum("value_meat_poultry_egalim_ht", default=0),
        Sum("value_meat_poultry_france_ht", default=0),
        Sum("value_fish_ht", default=0),
        Sum("value_fish_egalim_ht", default=0),
    )
    # count
    data["teledeclarations_count"] = agg["id__count"]
    # percent of bio, sustainable & egalim (bio + sustainable)
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
    data["egalim_percent"] = data["bio_percent"] + data["sustainable_percent"]  # same denominator
    # percent of meat egalim & france
    if agg["value_meat_poultry_ht__sum"] > 0:
        data["meat_egalim_percent"] = round(
            100 * agg["value_meat_poultry_egalim_ht__sum"] / agg["value_meat_poultry_ht__sum"]
        )
        data["meat_france_percent"] = round(
            100 * agg["value_meat_poultry_france_ht__sum"] / agg["value_meat_poultry_ht__sum"]
        )
    else:
        data["meat_egalim_percent"] = 0
        data["meat_france_percent"] = 0
    # percent of fish egalim
    if agg["value_fish_ht__sum"] > 0:
        data["fish_egalim_percent"] = round(100 * agg["value_fish_egalim_ht__sum"] / agg["value_fish_ht__sum"])
    else:
        data["fish_egalim_percent"] = 0
    # percent of appro
    badge_querysets = badges_for_queryset(teledeclarations)
    data["appro_percent"] = (
        int(badge_querysets["appro"].count() / data["teledeclarations_count"] * 100)
        if data["teledeclarations_count"]
        else 0
    )
    # return
    return data


class CanteenStatisticsSerializer(serializers.Serializer):
    # canteen stats
    canteen_count = serializers.IntegerField()
    sector_categories = serializers.DictField()
    management_types = serializers.DictField()
    production_types = serializers.DictField()
    economic_models = serializers.DictField()
    # teledeclaration stats
    teledeclarations_count = serializers.IntegerField()
    bio_percent = serializers.IntegerField()
    sustainable_percent = serializers.IntegerField()
    egalim_percent = serializers.IntegerField()
    meat_egalim_percent = serializers.IntegerField()
    meat_france_percent = serializers.IntegerField()
    fish_egalim_percent = serializers.IntegerField()
    appro_percent = serializers.IntegerField()

    @staticmethod
    def calculate_statistics(canteens, teledeclarations):
        data = {}
        data = calculate_statistics_canteens(canteens, data)
        data = calculate_statistics_teledeclarations(teledeclarations, data)
        return data
