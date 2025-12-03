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
    if self.valeur_totale is not None and isinstance(self.valeur_totale, Decimal):
        egalim_sum = (
            (self.valeur_bio or 0)
            + (self.valeur_siqo or 0)
            + (self.valeur_externalites_performance or 0)
            + (self.valeur_egalim_autres or 0)
        )
        if egalim_sum > self.valeur_totale:
            utils_utils.add_validation_error(
                errors,
                "valeur_totale",
                f"La somme des valeurs d'approvisionnement, {egalim_sum}, est plus que le total, {self.valeur_totale}",
            )
    return errors


def validate_viandes_volailles_total(self):
    errors = {}
    if (
        self.valeur_viandes_volailles is not None
        and self.valeur_viandes_volailles is not None
        and self.valeur_viandes_volailles_egalim > self.valeur_viandes_volailles
    ):
        utils_utils.add_validation_error(
            errors,
            "valeur_viandes_volailles",
            f"La valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim, {self.valeur_viandes_volailles_egalim}, est plus que la valeur totale (HT) viandes et volailles, {self.valeur_viandes_volailles}",
        )
    elif (
        self.valeur_viandes_volailles_france is not None
        and self.valeur_viandes_volailles is not None
        and self.valeur_viandes_volailles_france > self.valeur_viandes_volailles
    ):
        utils_utils.add_validation_error(
            errors,
            "valeur_viandes_volailles",
            f"La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, {self.valeur_viandes_volailles_france}, est plus que la valeur totale (HT) viandes et volailles, {self.valeur_viandes_volailles}",
        )
    return errors


def validate_produits_de_la_mer_total(self):
    errors = {}
    if (
        self.valeur_produits_de_la_mer_egalim is not None
        and self.valeur_produits_de_la_mer is not None
        and self.valeur_produits_de_la_mer_egalim > self.valeur_produits_de_la_mer
    ):
        utils_utils.add_validation_error(
            errors,
            "valeur_produits_de_la_mer",
            f"La valeur totale (HT) poissons et produits aquatiques EGalim, {self.valeur_produits_de_la_mer_egalim}, est plus que la valeur totale (HT) poissons et produits aquatiques, {self.valeur_produits_de_la_mer}",
        )
    return errors


def validate_viandes_volailles_produits_de_la_mer_egalim(self):
    errors = {}
    if self.valeur_totale is not None and isinstance(self.valeur_totale, Decimal):
        egalim_sum = (
            (self.valeur_bio or 0)
            + (self.valeur_siqo or 0)
            + (self.valeur_externalites_performance or 0)
            + (self.valeur_egalim_autres or 0)
        )
        viandes_volailles_produits_de_la_mer_egalim_sum = (self.valeur_produits_de_la_mer_egalim or 0) + (
            self.valeur_viandes_volailles_egalim or 0
        )
        if viandes_volailles_produits_de_la_mer_egalim_sum > egalim_sum:
            utils_utils.add_validation_error(
                errors,
                "valeur_siqo",
                f"La somme des valeurs viandes et poissons EGalim, {viandes_volailles_produits_de_la_mer_egalim_sum}, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGalim, {egalim_sum}",
            )
    return errors
