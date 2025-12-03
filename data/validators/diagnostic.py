from decimal import Decimal

from common.utils import utils as utils_utils
from data.utils import get_diagnostic_lower_limit_year, get_diagnostic_upper_limit_year


def validate_year(self):
    errors = {}
    if self.year is not None:
        lower_limit_year = get_diagnostic_lower_limit_year()
        upper_limit_year = get_diagnostic_upper_limit_year()
        if not isinstance(self.year, int) or self.year < lower_limit_year or self.year > upper_limit_year:
            utils_utils.add_validation_error(
                errors, "year", f"L'année doit être comprise entre {lower_limit_year} et {upper_limit_year}."
            )
    return errors


def validate_approvisionment_total(self):
    errors = {}
    if self.value_totale is not None and isinstance(self.value_totale, Decimal):
        egalim_sum = (
            (self.value_bio or 0)
            + (self.value_siqo or 0)
            + (self.value_externalites_performance or 0)
            + (self.value_egalim_autres or 0)
        )
        if egalim_sum > self.value_totale:
            utils_utils.add_validation_error(
                errors,
                "value_totale",
                f"La somme des valeurs d'approvisionnement, {egalim_sum}, est plus que le total, {self.value_totale}",
            )
    return errors


def validate_viandes_volailles_total(self):
    errors = {}
    if (
        self.value_viandes_volailles is not None
        and self.value_viandes_volailles is not None
        and self.value_viandes_volailles_egalim > self.value_viandes_volailles
    ):
        utils_utils.add_validation_error(
            errors,
            "value_viandes_volailles",
            f"La valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim, {self.value_viandes_volailles_egalim}, est plus que la valeur totale (HT) viandes et volailles, {self.value_viandes_volailles}",
        )
    elif (
        self.value_viandes_volailles_france is not None
        and self.value_viandes_volailles is not None
        and self.value_viandes_volailles_france > self.value_viandes_volailles
    ):
        utils_utils.add_validation_error(
            errors,
            "value_viandes_volailles",
            f"La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, {self.value_viandes_volailles_france}, est plus que la valeur totale (HT) viandes et volailles, {self.value_viandes_volailles}",
        )
    return errors


def validate_produits_de_la_mer_total(self):
    errors = {}
    if (
        self.value_produits_de_la_mer_egalim is not None
        and self.value_produits_de_la_mer is not None
        and self.value_produits_de_la_mer_egalim > self.value_produits_de_la_mer
    ):
        utils_utils.add_validation_error(
            errors,
            "value_produits_de_la_mer",
            f"La valeur totale (HT) poissons et produits aquatiques EGalim, {self.value_produits_de_la_mer_egalim}, est plus que la valeur totale (HT) poissons et produits aquatiques, {self.value_produits_de_la_mer}",
        )
    return errors


def validate_viandes_volailles_produits_de_la_mer_egalim(self):
    errors = {}
    if self.value_totale is not None and isinstance(self.value_totale, Decimal):
        egalim_sum = (
            (self.value_bio or 0)
            + (self.value_siqo or 0)
            + (self.value_externalites_performance or 0)
            + (self.value_egalim_autres or 0)
        )
        viandes_volailles_produits_de_la_mer_egalim_sum = (self.value_produits_de_la_mer_egalim or 0) + (
            self.value_viandes_volailles_egalim or 0
        )
        if viandes_volailles_produits_de_la_mer_egalim_sum > egalim_sum:
            utils_utils.add_validation_error(
                errors,
                "value_siqo",
                f"La somme des valeurs viandes et poissons EGalim, {viandes_volailles_produits_de_la_mer_egalim_sum}, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGalim, {egalim_sum}",
            )
    return errors
