import json
from functools import cache
from pathlib import Path

from django.conf import settings

TELEDECLARATION_YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
VOLETS = ["APPROVISIONNEMENT", "GASPILLAGE", "DIVERSIFICATION", "PLASTIQUE", "INFORMATION"]
DIAGNOSTIC_TYPES = ["SIMPLE", "COMPLETE"]


@cache
def get_teledeclaration_config(year):
    """
    The fields configuration of a bilan year: teledeclaration/<year>/champs.json
    """
    config_path = Path(settings.BASE_DIR) / "teledeclaration" / str(year) / "champs.json"
    return json.loads(config_path.read_text(encoding="utf-8"))


def get_teledeclaration_import_fields(year, diagnostic_type):
    """
    The appro fields of an import, in the order of its columns
    """
    fields = get_teledeclaration_config(year)["APPROVISIONNEMENT"]
    present_fields = [
        name for name, field in fields.items() if field["diagnostic_type"][diagnostic_type]["is_present"]
    ]

    def get_import_position(name):
        # 2025: its SIMPLE and COMPLETE column orders are different a specific order is needed
        field = fields[name]
        return field["diagnostic_type"][diagnostic_type].get("legacy_import_order") or field["index_code"]

    return sorted(present_fields, key=get_import_position)


def get_teledeclaration_import_fields_required(year, diagnostic_type):
    fields = get_teledeclaration_config(year)["APPROVISIONNEMENT"]
    return [
        name
        for name in get_teledeclaration_import_fields(year, diagnostic_type)
        if fields[name]["diagnostic_type"][diagnostic_type]["is_required"]
    ]


def get_teledeclaration_verbose_name(year, volet, field_name):
    return get_teledeclaration_config(year)[volet][field_name]["verbose_name"]


def get_teledeclaration_verbose_names(year):
    """
    The verbose_name of the fields of all the volets for a given year (fields with an empty verbose_name are skipped)
    """
    return {
        name: field["verbose_name"]
        for volet_fields in get_teledeclaration_config(year).values()
        for name, field in volet_fields.items()
        if field["verbose_name"]
    }


def _sort_by_index_code(year, volet, field_names):
    volet_fields = get_teledeclaration_config(year)[volet]
    return sorted(field_names, key=lambda name: volet_fields[name]["index_code"])


def _get_teledeclaration_fields(year, volet, diagnostic_type=None, required=False):
    """
    diagnostic_type (SIMPLE / COMPLETE) is only used by the APPROVISIONNEMENT volet
    """
    year = int(year) if year else None
    if year not in TELEDECLARATION_YEARS:
        raise ValueError(f"Field 'year' expected one of {TELEDECLARATION_YEARS} but got '{year}'.")
    if volet not in VOLETS:
        raise ValueError(f"Volet expected one of {VOLETS} but got '{volet}'.")
    volet_fields = get_teledeclaration_config(year)[volet]
    if volet == "APPROVISIONNEMENT":
        if diagnostic_type not in DIAGNOSTIC_TYPES:
            raise ValueError(
                f"Field 'diagnostic_type' expected one of {DIAGNOSTIC_TYPES} but got '{diagnostic_type}'."
            )
        volet_fields = {
            name: field["diagnostic_type"][diagnostic_type]
            for name, field in volet_fields.items()
            if field["diagnostic_type"][diagnostic_type]["is_present"]
        }
    field_names = [name for name, field in volet_fields.items() if field["is_required"] or not required]
    return _sort_by_index_code(year, volet, field_names)


def get_teledeclaration_fields_all(year, volet, diagnostic_type=None):
    return _get_teledeclaration_fields(year, volet, diagnostic_type, required=False)


def get_teledeclaration_fields_required(year, volet, diagnostic_type=None):
    return _get_teledeclaration_fields(year, volet, diagnostic_type, required=True)


def get_teledeclaration_fields_all_years(volet):
    """
    Union of the volet's fields over all the years (& diagnostic_types for APPROVISIONNEMENT)
    Order: the most recent year's fields first, then the fields that were removed since (legacy)
    """
    fields = {}
    for year in sorted(TELEDECLARATION_YEARS, reverse=True):
        diagnostic_types = DIAGNOSTIC_TYPES if volet == "APPROVISIONNEMENT" else [None]
        year_fields = {}
        for diagnostic_type in diagnostic_types:
            year_fields.update(dict.fromkeys(get_teledeclaration_fields_all(year, volet, diagnostic_type)))
        fields.update(dict.fromkeys(_sort_by_index_code(year, volet, year_fields)))
    return list(fields)


def get_teledeclaration_fields_all_volets(year, diagnostic_type):
    """
    All the fields of all the volets for a given year (diagnostic_type is used by the APPROVISIONNEMENT volet)
    """
    year = int(year) if year else None
    if year not in TELEDECLARATION_YEARS:
        raise ValueError(f"Field 'year' expected one of {TELEDECLARATION_YEARS} but got '{year}'.")
    return [field for volet in VOLETS for field in get_teledeclaration_fields_all(year, volet, diagnostic_type)]


TUNNEL_PROGRESS_FIELD_BY_VOLET = {
    "APPROVISIONNEMENT": "tunnel_appro",
    "GASPILLAGE": "tunnel_waste",
    "DIVERSIFICATION": "tunnel_diversification",
    "PLASTIQUE": "tunnel_plastic",
    "INFORMATION": "tunnel_info",
}


def get_tunnel_progress_field(volet):
    """
    The tunnel_* field of the volet (used by the frontend to store the progress in the volet's tunnel)
    """
    if volet not in TUNNEL_PROGRESS_FIELD_BY_VOLET:
        raise ValueError(f"Volet expected one of {list(TUNNEL_PROGRESS_FIELD_BY_VOLET.keys())} but got '{volet}'.")
    return TUNNEL_PROGRESS_FIELD_BY_VOLET[volet]


# opt-in: the volets that can still be edited once the diagnostic is teledeclared (the APPROVISIONNEMENT volet can't)
VOLETS_EDITABLE_EVEN_IF_IS_TELEDECLARED = ["GASPILLAGE", "DIVERSIFICATION", "PLASTIQUE", "INFORMATION"]


def get_fields_editable_even_if_is_teledeclared(year):
    """
    The fields that can still be edited once the diagnostic is teledeclared
    (see VOLETS_EDITABLE_EVEN_IF_IS_TELEDECLARED)
    - the fields of these volets for the given year
    - their tunnel_* field
    """
    return [
        field
        for volet in VOLETS_EDITABLE_EVEN_IF_IS_TELEDECLARED
        for field in get_teledeclaration_fields_all(year, volet)
    ] + [get_tunnel_progress_field(volet) for volet in VOLETS_EDITABLE_EVEN_IF_IS_TELEDECLARED]
