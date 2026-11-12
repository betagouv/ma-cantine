from django.core.exceptions import ValidationError

from common.utils.utils import normalize_string


def normalize_siret(siret):
    """
    Clean a SIRET read from an import file:
    - remove the spaces (e.g. "213 401 722 01787" -> "21340172201787")
    - Excel number cell: the leading 0s are lost (e.g. 5980406200087 instead of "05980406200087"): add them back
    """
    if isinstance(siret, float) and siret.is_integer():
        siret = int(siret)
    if isinstance(siret, int) and not isinstance(siret, bool):
        return str(siret).zfill(14)
    return normalize_string(siret)


def is_valid_length_siren(siren: str) -> bool:
    if len(siren) == 9:
        return True


def is_valid_length_siret(siret: str) -> bool:
    if len(siret) == 14:
        return True


def is_valid_luhn_siret(siret: str) -> bool:
    odd_digits = [int(n) for n in siret[-1::-2]]
    even_digits = [int(n) for n in siret[-2::-2]]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(int(n) for n in str(digit * 2))
    return checksum % 10 == 0


def validate_siren(siren):
    if siren is None or siren == "":
        return
    if not siren.isdigit() or not is_valid_length_siren(siren):
        raise ValidationError("9 caractères numériques sont attendus")


def validate_siret(siret):
    """
    Performs length and Luhn validation
    (https://portal.hardis-group.com/pages/viewpage.action?pageId=120357227)
    """
    if siret is None or siret == "":
        return
    if not siret.isdigit() or not is_valid_length_siret(siret):
        raise ValidationError("14 caractères numériques sont attendus")
    if not is_valid_luhn_siret(siret):
        raise ValidationError(
            "Le numéro SIRET est invalide et semble ne pas exister dans les registres officiels, vous pouvez vérifier sa validité depuis le site : https://annuaire-entreprises.data.gouv.fr"
        )
