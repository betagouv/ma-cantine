from decimal import Decimal

from common.utils import utils as utils_utils
from data.utils import get_diagnostic_lower_limit_year, get_diagnostic_upper_limit_year


def validate_year(self):
    errors = {}
    if self.year is None:
        return
    lower_limit_year = get_diagnostic_lower_limit_year()
    upper_limit_year = get_diagnostic_upper_limit_year()
    if not isinstance(self.year, int) or self.year < lower_limit_year or self.year > upper_limit_year:
        utils_utils.add_validation_error(
            errors, "year", f"L'année doit être comprise entre {lower_limit_year} et {upper_limit_year}."
        )
    return errors


def validate_approvisionment_total(self):
    errors = {}
    if self.value_total_ht is None or not isinstance(self.value_total_ht, Decimal):
        return
    value_sum = (
        (self.value_bio_ht or 0)
        + (self.value_sustainable_ht or 0)
        + (self.value_externality_performance_ht or 0)
        + (self.value_egalim_others_ht or 0)
    )
    if value_sum > self.value_total_ht:
        utils_utils.add_validation_error(
            errors,
            "value_total_ht",
            f"La somme des valeurs d'approvisionnement, {value_sum}, est plus que le total, {self.value_total_ht}",
        )
    return errors


def validate_meat_total(self):
    errors = {}
    if (
        self.value_meat_poultry_egalim_ht is not None
        and self.value_meat_poultry_ht is not None
        and self.value_meat_poultry_egalim_ht > self.value_meat_poultry_ht
    ):
        utils_utils.add_validation_error(
            errors,
            "value_meat_poultry_ht",
            f"La valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim, {self.value_meat_poultry_egalim_ht}, est plus que la valeur totale (HT) viandes et volailles, {self.value_meat_poultry_ht}",
        )
    elif (
        self.value_meat_poultry_france_ht is not None
        and self.value_meat_poultry_ht is not None
        and self.value_meat_poultry_france_ht > self.value_meat_poultry_ht
    ):
        utils_utils.add_validation_error(
            errors,
            "value_meat_poultry_ht",
            f"La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, {self.value_meat_poultry_france_ht}, est plus que la valeur totale (HT) viandes et volailles, {self.value_meat_poultry_ht}",
        )
    return errors


def validate_fish_total(self):
    errors = {}
    if (
        self.value_fish_egalim_ht is not None
        and self.value_fish_ht is not None
        and self.value_fish_egalim_ht > self.value_fish_ht
    ):
        utils_utils.add_validation_error(
            errors,
            "value_fish_ht",
            f"La valeur totale (HT) poissons et produits aquatiques EGalim, {self.value_fish_egalim_ht}, est plus que la valeur totale (HT) poissons et produits aquatiques, {self.value_fish_ht}",
        )
    return errors


def validate_meat_fish_egalim(self):
    errors = {}
    if self.value_total_ht is None or not isinstance(self.value_total_ht, Decimal):
        return
    egalim_sum = (
        (self.value_bio_ht or 0)
        + (self.value_sustainable_ht or 0)
        + (self.value_externality_performance_ht or 0)
        + (self.value_egalim_others_ht or 0)
    )
    meat_fish_egalim_sum = (self.value_fish_egalim_ht or 0) + (self.value_meat_poultry_egalim_ht or 0)
    if meat_fish_egalim_sum > egalim_sum:
        utils_utils.add_validation_error(
            errors,
            "value_sustainable_ht",
            f"La somme des valeurs viandes et poissons EGalim, {meat_fish_egalim_sum}, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGalim, {egalim_sum}",
        )
    return errors
