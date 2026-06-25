from datetime import date

from common.utils import utils as utils_utils


def validate_purchase_date(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is empty or a date
    - extra validation:
        - date cannot be in the future
    """
    errors = {}
    field_name = "date"
    value = getattr(instance, field_name)
    if value and str(value) > str(date.today()):
        utils_utils.add_validation_error(errors, field_name, "La date ne peut pas être dans le futur.")
    return errors


def validate_purchase_caracteristiques(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is empty or in the choices
    - extra validation:
        - both "EUROPE" and "FRANCE" cannot be selected at the same time
    """
    errors = {}
    field_name = "caracteristiques"
    value = getattr(instance, field_name) or []
    if instance.Characteristic.EUROPE in value and instance.Characteristic.FRANCE in value:
        utils_utils.add_validation_error(
            errors,
            field_name,
            f"Les caractéristiques {instance.Characteristic.EUROPE} et {instance.Characteristic.FRANCE} ne peuvent pas être sélectionnées en même temps.",
        )
    return errors


def validate_purchase_definition_local(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is empty or in the choices
    - extra validation:
        - if caracteristiques includes "LOCAL"
            - definition_local can be filled
            - if definition_local is "KM", then definition_local_km can be filled
            - if definition_local is not "KM", then definition_local_km must be empty
        - if caracteristiques does not include "LOCAL", definition_local & definition_local_km must be empty
    """
    errors = {}
    field_name = "definition_local"
    value = getattr(instance, field_name)
    definition_local_km = getattr(instance, "definition_local_km")
    caracteristiques = getattr(instance, "caracteristiques") or []
    if instance.Characteristic.LOCAL in caracteristiques:
        if value != instance.Local.KM:
            if definition_local_km not in [None, ""]:
                utils_utils.add_validation_error(
                    errors,
                    "definition_local_km",
                    "La distance en km doit être vide lorsque la définition locale n'est pas 'KM'.",
                )
    else:
        if value not in [None, ""]:
            utils_utils.add_validation_error(
                errors,
                field_name,
                f"La caractéristique {instance.Characteristic.LOCAL} n'est pas sélectionnée : le champ doit être vide.",
            )
        if definition_local_km not in [None, ""]:
            utils_utils.add_validation_error(
                errors,
                "definition_local_km",
                f"La caractéristique {instance.Characteristic.LOCAL} n'est pas sélectionnée : le champ doit être vide.",
            )
    return errors
