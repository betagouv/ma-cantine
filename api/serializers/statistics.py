import locale
import logging

from django.db.models import Count, FloatField, Sum
from django.db.models.fields.json import KT
from django.db.models.functions import Cast
from django.utils import timezone
from rest_framework import serializers

from common.utils.badges import badges_for_queryset
from data.models import Canteen, Sector
from macantine.utils import (
    CAMPAIGN_DATES,
    EGALIM_OBJECTIVES,
    get_year_campaign_end_date_or_today_date,
)

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
    FIELDS_TO_HIDE_IF_REPORT_NOT_PUBLISHED = [
        "bio_percent",
        "sustainable_percent",
        "egalim_percent",
        "meat_egalim_percent",
        "meat_france_percent",
        "fish_egalim_percent",
        "appro_percent",
    ]
    FIELDS_TO_HIDE_IF_CAMPAIGN_NOT_FOUND = ["teledeclarations_count"] + FIELDS_TO_HIDE_IF_REPORT_NOT_PUBLISHED

    # canteen stats
    canteen_count = serializers.IntegerField()
    sector_categories = serializers.DictField()
    management_types = serializers.DictField()
    production_types = serializers.DictField()
    economic_models = serializers.DictField()
    # teledeclaration stats
    teledeclarations_count = serializers.IntegerField()
    bio_percent = serializers.IntegerField(label="Part des achats bio dans les achats alimentaires de l'année")
    sustainable_percent = serializers.IntegerField(
        label="Part des achats durables (hors bio) dans les achats alimentaires de l'année"
    )
    egalim_percent = serializers.IntegerField(label="Part des achats EGalim dans les achats alimentaires de l'année")
    meat_egalim_percent = serializers.IntegerField()
    meat_france_percent = serializers.IntegerField()
    fish_egalim_percent = serializers.IntegerField()
    appro_percent = serializers.IntegerField()
    # notes
    notes = serializers.DictField()

    @staticmethod
    def calculate_statistics(canteens, teledeclarations):
        data = {}
        data = calculate_statistics_canteens(canteens, data)
        data = calculate_statistics_teledeclarations(teledeclarations, data)
        return data

    @staticmethod
    def generate_notes(year):
        data = {}
        data["warnings"] = [
            "Pour des raisons de confidentialité, les cantines des armées ne sont pas intégrées dans cet observatoire."
        ]
        canteen_created_before_date = get_year_campaign_end_date_or_today_date(year)
        if canteen_created_before_date:
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
            data["canteen_count_description"] = f"Au {canteen_created_before_date.strftime('%-d %B %Y')}"
        # egalim objectives
        data["bio_percent_objective"] = EGALIM_OBJECTIVES["bio_percent"]
        data["egalim_percent_objective"] = EGALIM_OBJECTIVES["egalim_percent"]
        return data

    @staticmethod
    def hide_data_if_report_not_published(data, year):
        """
        Hide data if the report for the given year is not published yet.
        """
        year = int(year)
        if year not in CAMPAIGN_DATES.keys():
            for field in CanteenStatisticsSerializer.FIELDS_TO_HIDE_IF_CAMPAIGN_NOT_FOUND:
                data[field] = None
            # TODO: ajouter le cas où la campagne de TD n'a pas commencé mais dont on connait les dates
            if year >= timezone.now().year:
                data["notes"][
                    "campaign_info"
                ] = f"La campagne de télédéclaration pour l'année {year} n'a pas encore commencée, les données seront disponibles en {year + 1}."
            else:
                data["notes"][
                    "campaign_info"
                ] = f"Aucune campagne de télédéclaration trouvée pour l'année {year}. Veuillez vérifier l'année saisie."
        elif not CAMPAIGN_DATES[year].get("rapport_parlement_url"):
            for field in CanteenStatisticsSerializer.FIELDS_TO_HIDE_IF_REPORT_NOT_PUBLISHED:
                data[field] = None
            data["notes"][
                "campaign_info"
            ] = f"Le détail des données de {year} télédéclarées durant la campagne {year + 1} seront disponibles d'ici la fin d'année dès lors que le rapport statistique sera validé par le parlement."
        else:
            pass  # report is published, do not hide data
        return data
