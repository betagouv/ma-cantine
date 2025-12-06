from common.utils import utils as utils_utils


def validate_purchase_local_definition(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is empty or in the choices
    - extra validation:
        - if characteristics includes "LOCAL", local_definition must be filled
        - if characteristics does not include "LOCAL", local_definition must be empty
    """
    errors = {}
    field_name = "local_definition"
    value = getattr(instance, field_name)
    characteristics = getattr(instance, "characteristics")
    if characteristics:
        if instance.Characteristic.LOCAL in characteristics:
            if value in [None, ""]:
                utils_utils.add_validation_error(
                    errors,
                    field_name,
                    f"La caractéristique {instance.Characteristic.LOCAL} est sélectionnée : le champ doit être rempli.",
                )
        else:
            if value not in [None, ""]:
                utils_utils.add_validation_error(
                    errors,
                    field_name,
                    f"La caractéristique {instance.Characteristic.LOCAL} n'est pas sélectionnée : le champ doit être vide.",
                )
    else:
        if value not in [None, ""]:
            utils_utils.add_validation_error(
                errors,
                field_name,
                f"La caractéristique {instance.Characteristic.LOCAL} n'est pas sélectionnée : le champ doit être vide.",
            )
    return errors
