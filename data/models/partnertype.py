from django.db import models


class PartnerType(models.TextChoices):
    LOGICIEL = "logiciel", "Logiciels / outils numériques"
    RESEAU = "reseau", "Réseaux ou communautés interprofessionnelles"
    PLATEFORME = "plateforme", "Plateformes de producteurs / fournisseurs / grossistes"
    ASSOCIATION = "association", "Une association / un syndicat"
    INSTITUTION_PUBLIQUE = "institution_publique", "Une institution, un acteur public, un organisme d'Etat"
    ENTREPRISE_PRIVEE = "entreprise_privee", "Entreprise privée"
    AUTRE = "autre", "Autre"


def get_partner_type_lib_list_from_type_list(type_list: list[str]) -> list[str]:
    return [
        PartnerType(partner_type).label for partner_type in (type_list or []) if partner_type in PartnerType.values
    ]
