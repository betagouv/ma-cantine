from common.utils import utils as utils_utils


def validate_purchase_definition_local(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is empty or in the choices
    - extra validation:
        - if caracteristiques includes "LOCAL", definition_local must be filled
        - if caracteristiques does not include "LOCAL", definition_local must be empty
    """
    errors = {}
    field_name = "definition_local"
    value = getattr(instance, field_name)
    caracteristiques = getattr(instance, "caracteristiques") or []
    if instance.Characteristic.LOCAL in caracteristiques:
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
    return errors
