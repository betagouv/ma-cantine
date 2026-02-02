from data.models import Diagnostic


def appro_to_percentages(representation, instance, remove_values=True):
    # first do the percentages relative to meat and fish totals
    # not removing these totals so that can then calculate the percent of those compared to global total
    meat_total = representation.get("valeur_viandes_volailles")
    if meat_total:
        field = "valeur_viandes_volailles_egalim"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / meat_total
        field = "valeur_viandes_volailles_france"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / meat_total

    fish_total = representation.get("valeur_produits_de_la_mer")
    if fish_total:
        field = "valeur_produits_de_la_mer_egalim"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / fish_total
        field = "valeur_produits_de_la_mer_france"
        value = representation.get(field)
        if value is not None:
            representation[f"percentage_{field}"] = value / fish_total

    # NOTE: on va écraser les pourcentages viande/poisson france car ils vont être recalculés...
    appro_fields = [
        "valeur_totale",
        "valeur_bio",
        "valeur_siqo",
        "valeur_externalites_performance",
        "valeur_egalim_autres",
    ]

    if representation.get("diagnostic_type") is Diagnostic.DiagnosticType.COMPLETE:
        appro_fields.append(Diagnostic.COMPLETE_APPRO_FIELDS)  # meat and fish totals included in COMPLETE

    total = representation.get("valeur_totale")
    for field in appro_fields:
        new_field_name = f"percentage_{field}"
        if total and representation.get(field) is not None:
            representation[new_field_name] = representation[field] / total
        if remove_values:
            representation.pop(field, None)

    representation["percentage_valeur_totale"] = 1
    if remove_values:
        representation.pop("valeur_totale", None)
        representation.pop("valeur_viandes_volailles", None)
        representation.pop("valeur_viandes_volailles_egalim", None)
        representation.pop("valeur_viandes_volailles_france", None)
        representation.pop("valeur_produits_de_la_mer", None)
        representation.pop("valeur_produits_de_la_mer_egalim", None)
        representation.pop("valeur_produits_de_la_mer_france", None)

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
