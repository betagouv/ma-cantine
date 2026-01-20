from decimal import Decimal

from common.utils import utils as utils_utils
from data.utils import get_diagnostic_lower_limit_year, get_diagnostic_upper_limit_year


def validate_year(instance):
    """
    - extra validation:
        - year must be filled
        - year must be an integer
        - year must be between lower and upper limit years
    """
    errors = {}
    field_name = "year"
    value = getattr(instance, "year")
    if value in [None, ""]:
        utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
    elif not (isinstance(value, int) or (isinstance(value, str) and value.isdigit())):
        utils_utils.add_validation_error(errors, field_name, "Le champ doit être un nombre entier.")
    else:
        lower_limit_year = get_diagnostic_lower_limit_year()
        upper_limit_year = get_diagnostic_upper_limit_year()
        if not isinstance(value, int) or value < lower_limit_year or value > upper_limit_year:
            utils_utils.add_validation_error(
                errors, "year", f"L'année doit être comprise entre {lower_limit_year} et {upper_limit_year}."
            )
    return errors


def validate_diagnostic_type(instance):
    """
    - extra validation:
        - diagnostic_type must be filled
        - diagnostic_type must be among the allowed values
    """
    errors = {}
    field_name = "diagnostic_type"
    value = getattr(instance, field_name)
    if value not in instance.DiagnosticType.values:
        utils_utils.add_validation_error(
            errors,
            field_name,
            f"Le type de diagnostic doit être parmi {instance.DiagnosticType.values}.",
        )
    return errors


def validate_appro_fields_required(instance):
    """
    - clean_fields() (called by full_clean()) already does some checks
      BUT most of the model fields are optional...
    - extra validation: depending on the year & diagnostic_type of the diagnostic
    """
    errors = {}
    if instance.year:
        if int(instance.year) >= 2025:
            required_fields = (
                instance.SIMPLE_APPRO_FIELDS_REQUIRED_2025
                if instance.diagnostic_type == instance.DiagnosticType.SIMPLE
                else instance.COMPLETE_APPRO_FIELDS_REQUIRED_2025
            )
        else:
            required_fields = ["valeur_totale"]
        for field in required_fields:
            if getattr(instance, field) is None:
                utils_utils.add_validation_error(
                    errors, field, f"Ce champ est obligatoire pour l'année {instance.year}."
                )
    return errors


def validate_valeur_totale(instance):
    """
    - clean_fields() (called by full_clean()) already does some checks
    - extra validation:
        - valeur_totale must be > 0
        - valeur_totale must be >= each of the other fields (simple only for now)
        - valeur totale must be >= sum of each label
        - valeur_totale must be >= sum of egalim fields
    """
    errors = {}
    if instance.valeur_totale is not None:
        if instance.valeur_totale <= 0:
            utils_utils.add_validation_error(
                errors,
                "valeur_totale",
                "La valeur totale (HT) doit être supérieure à 0",
            )
        elif isinstance(instance.valeur_totale, Decimal):
            for field_name in instance.SIMPLE_APPRO_FIELDS:
                field_value = getattr(instance, field_name)
                if field_value and field_value > instance.valeur_totale:
                    utils_utils.add_validation_error(
                        errors,
                        "valeur_totale",
                        f"La valeur totale (HT), {instance.valeur_totale}, est moins que la valeur (HT) {field_name}, {field_value}",
                    )
            for label in instance.APPRO_LABELS_ALL:
                label_sum = instance.label_sum(label)
                if label_sum and label_sum > instance.valeur_totale:
                    utils_utils.add_validation_error(
                        errors,
                        "valeur_totale",
                        f"La valeur totale (HT), {instance.valeur_totale}, est moins que la somme des valeurs d'approvisionnement pour le label {label}, {label_sum}",
                    )
            egalim_sum = instance.egalim_sum()
            if egalim_sum and egalim_sum > instance.valeur_totale:
                utils_utils.add_validation_error(
                    errors,
                    "valeur_totale",
                    f"La valeur totale (HT), {instance.valeur_totale}, est moins que la somme des valeurs d'approvisionnement, {egalim_sum}",
                )
    return errors


def validate_valeur_bio(instance):
    """
    - extra validation:
        - valeur_bio_dont_commerce_equitable must be <= valeur_bio
    """
    errors = {}
    if instance.valeur_bio is not None:
        if (
            instance.valeur_bio_dont_commerce_equitable is not None
            and instance.valeur_bio_dont_commerce_equitable > instance.valeur_bio
        ):
            utils_utils.add_validation_error(
                errors,
                "valeur_bio",
                f"La valeur (HT) bio dont commerce équitable, {instance.valeur_bio_dont_commerce_equitable}, est plus que la valeur totale (HT) bio, {instance.valeur_bio}",
            )
    return errors


def validate_valeur_egalim_autres(instance):
    """
    - extra validation:
        - valeur_egalim_autres_dont_commerce_equitable must be <= valeur_egalim_autres
    """
    errors = {}
    if instance.valeur_egalim_autres is not None:
        if (
            instance.valeur_egalim_autres_dont_commerce_equitable is not None
            and instance.valeur_egalim_autres_dont_commerce_equitable > instance.valeur_egalim_autres
        ):
            utils_utils.add_validation_error(
                errors,
                "valeur_egalim_autres",
                f"La valeur (HT) achats commerce équitable (hors bio), {instance.valeur_egalim_autres_dont_commerce_equitable}, est plus que la valeur totale (HT) des autres achats EGalim, {instance.valeur_egalim_autres}",
            )
    return errors


def validate_viandes_volailles_total(instance):
    """
    - extra validation:
        - valeur_viandes_volailles_egalim must be <= valeur_viandes_volailles
        - valeur_viandes_volailles_france must be <= valeur_viandes_volailles
    """
    errors = {}
    if instance.valeur_viandes_volailles is not None:
        if (
            instance.valeur_viandes_volailles_egalim is not None
            and instance.valeur_viandes_volailles_egalim > instance.valeur_viandes_volailles
        ):
            utils_utils.add_validation_error(
                errors,
                "valeur_viandes_volailles",
                f"La valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim, {instance.valeur_viandes_volailles_egalim}, est plus que la valeur totale (HT) viandes et volailles, {instance.valeur_viandes_volailles}",
            )
        if (
            instance.valeur_viandes_volailles_france is not None
            and instance.valeur_viandes_volailles_france > instance.valeur_viandes_volailles
        ):
            utils_utils.add_validation_error(
                errors,
                "valeur_viandes_volailles",
                f"La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, {instance.valeur_viandes_volailles_france}, est plus que la valeur totale (HT) viandes et volailles, {instance.valeur_viandes_volailles}",
            )
    return errors


def validate_produits_de_la_mer_total(instance):
    """
    - extra validation:
        - valeur_produits_de_la_mer_egalim must be <= valeur_produits_de_la_mer
        - valeur_produits_de_la_mer_france must be <= valeur_produits_de_la_mer
    """
    errors = {}
    if instance.valeur_produits_de_la_mer is not None:
        if (
            instance.valeur_produits_de_la_mer_egalim is not None
            and instance.valeur_produits_de_la_mer_egalim > instance.valeur_produits_de_la_mer
        ):
            utils_utils.add_validation_error(
                errors,
                "valeur_produits_de_la_mer",
                f"La valeur totale (HT) poissons et produits aquatiques EGalim, {instance.valeur_produits_de_la_mer_egalim}, est plus que la valeur totale (HT) poissons et produits aquatiques, {instance.valeur_produits_de_la_mer}",
            )
        if (
            instance.valeur_produits_de_la_mer_france is not None
            and instance.valeur_produits_de_la_mer_france > instance.valeur_produits_de_la_mer
        ):
            utils_utils.add_validation_error(
                errors,
                "valeur_produits_de_la_mer",
                f"La valeur totale (HT) poissons et produits aquatiques provenance France, {instance.valeur_produits_de_la_mer_france}, est plus que la valeur totale (HT) poissons et produits aquatiques, {instance.valeur_produits_de_la_mer}",
            )
    return errors


def validate_viandes_volailles_produits_de_la_mer_egalim(instance):
    """
    - extra validation:
        - sum of valeur_viandes_volailles_egalim and valeur_produits_de_la_mer_egalim must be <= sum of egalim fields
    """
    errors = {}
    if instance.valeur_viandes_volailles_egalim is not None and instance.valeur_produits_de_la_mer_egalim is not None:
        egalim_sum = instance.egalim_sum()
        viandes_volailles_produits_de_la_mer_egalim_sum = (instance.valeur_produits_de_la_mer_egalim or 0) + (
            instance.valeur_viandes_volailles_egalim or 0
        )
        if viandes_volailles_produits_de_la_mer_egalim_sum > egalim_sum:
            utils_utils.add_validation_error(
                errors,
                "valeur_siqo",
                f"La somme des valeurs viandes et poissons EGalim, {viandes_volailles_produits_de_la_mer_egalim_sum}, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGalim, {egalim_sum}",
            )
    return errors
