from data.models import Diagnostic
from data.models.sector import Sector


def appro_to_percentages(representation, instance, remove_values=True):
    # first do the percentages relative to meat and fish totals
    # not removing these totals so that can then calculate the percent of those compared to global total
    meat_total = representation.get("value_meat_poultry_ht")
    if meat_total:
        field = "value_meat_poultry_egalim_ht"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / meat_total
        field = "value_meat_poultry_france_ht"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / meat_total

    fish_total = representation.get("value_fish_ht")
    if fish_total:
        field = "value_fish_egalim_ht"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / fish_total

    appro_field = (
        "value_total_ht",
        "value_bio_ht",
        "value_sustainable_ht",
        "value_externality_performance_ht",
        "value_egalim_others_ht",
    ) + Diagnostic.COMPLETE_APPRO_FIELDS  # meat and fish totals included in COMPLETE
    total = representation.get("value_total_ht")

    for field in appro_field:
        new_field_name = f"percentage_{field}"
        if total and representation.get(field) is not None:
            representation[new_field_name] = representation[field] / total
        if remove_values:
            representation.pop(field, None)

    representation["percentage_value_total_ht"] = 1
    if remove_values:
        representation.pop("value_total_ht", None)
        representation.pop("value_meat_poultry_egalim_ht", None)
        representation.pop("value_meat_poultry_france_ht", None)
        representation.pop("value_fish_egalim_ht", None)

    return representation


def safe_to_float(value):
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None


def match_sector_values(value):
    "In order to match historical and actual sector values"
    return (
        value.replace("etablissements", "établissements")
        .replace("médicaux ", "médico-")
        .replace("Lycée", "lycée")
        .replace("Etat", "État")
        .replace("établissements spécialisés", "Etablissements spécialisés")
        .replace("/", " / ")
        .replace("/ ", " / ")
        .replace("   ", " ")
        .replace("  ", " ")
    )


def extract_sector_from_dict_sectors(sectors):
    if len(sectors) > 1:
        return "Secteurs multiples"
    elif len(sectors) == 1:
        return match_sector_values(sectors[0]["name"])
    else:
        return None


def extract_category_from_dict_sectors(categories):
    if len(categories) > 1:
        return "Catégories multiples"
    elif len(categories) == 1:
        return Sector.Categories(categories[0]["category"]).label if categories[0]["category"] else None
    else:
        return None
