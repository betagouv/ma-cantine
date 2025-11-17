from django.db import models


class SectorCategory(models.TextChoices):
    ADMINISTRATION = "administration", "Administration"
    ENTERPRISE = "enterprise", "Entreprise"
    EDUCATION = "education", "Enseignement"
    HEALTH = "health", "Santé"
    SOCIAL = "social", "Social / Médico-social"
    LEISURE = "leisure", "Loisirs"
    AUTRES = "autres", "Autres"


class Sector(models.TextChoices):
    # administration
    ADMINISTRATION_PRISON = "Restaurants des prisons", "Restaurants des prisons"
    ADMINISTRATION_ADMINISTRATIF = "Restaurants administratifs d'Etat (RA)", "Restaurants administratifs d'Etat (RA)"
    ADMINISTRATION_ARMEE = (
        "Restaurants des armées / police / gendarmerie",
        "Restaurants des armées / police / gendarmerie",
    )
    ADMINISTRATION_ETABLISSEMENT_PUBLIC = (
        "Etablissements publics d'Etat (EPA ou EPIC)",
        "Etablissements publics d'Etat (EPA ou EPIC)",
    )
    ADMINISTRATION_INTER_ADMINISTRATIF = (
        "Restaurants inter-administratifs d'État (RIA)",
        "Restaurants inter-administratifs d'État (RIA)",
    )
    ADMINISTRATION_ADMINISTRATIF_DES_COLLECTIVITES = (
        "Restaurants administratifs des collectivités territoriales",
        "Restaurants administratifs des collectivités territoriales",
    )
    # entreprise
    ENTERPRISE_ENTREPRISE = "Restaurants d'entreprises", "Restaurants d'entreprises"
    ENTERPRISE_INTER_ENTREPRISE = "Restaurants inter-entreprises", "Restaurants inter-entreprises"
    # education
    EDUCATION_PRIMAIRE = "Ecole primaire (maternelle et élémentaire)", "Ecole primaire (maternelle et élémentaire)"
    EDUCATION_SECONDAIRE_COLLEGE = "Secondaire collège", "Secondaire collège"
    EDUCATION_SECONDAIRE_LYCEE = "Secondaire lycée (hors agricole)", "Secondaire lycée (hors agricole)"
    EDUCATION_ENSEIGNEMENT_AGRICOLE = (
        "Etablissements d'enseignement agricole",
        "Etablissements d'enseignement agricole",
    )
    EDUCATION_SUPERIEUR_UNIVERSITAIRE = "Supérieur et Universitaire", "Supérieur et Universitaire"
    EDUCATION_AUTRE = "Autres structures d'enseignement", "Autres structures d'enseignement"
    # health
    HEALTH_HOPITAL = "Hôpitaux", "Hôpitaux"
    HEALTH_CLINIQUE = "Cliniques", "Cliniques"
    HEALTH_AUTRE = "Autres établissements de soins", "Autres établissements de soins"
    # social
    SOCIAL_CRECHE = "Crèche", "Crèche"
    SOCIAL_IME = "IME / ITEP", "IME / ITEP"
    SOCIAL_ESAT = "ESAT / Etablissements spécialisés", "ESAT / Etablissements spécialisés"
    SOCIAL_EHPAD = (
        "EHPAD / maisons de retraite / foyers de personnes âgées",
        "EHPAD / maisons de retraite / foyers de personnes âgées",
    )
    SOCIAL_PJJ = "Etablissements de la PJJ", "Etablissements de la PJJ"
    SOCIAL_AUTRE = "Autres établissements sociaux et médico-sociaux", "Autres établissements sociaux et médico-sociaux"
    # leisure
    LEISURE_CENTRE_VACANCE = "Centre de vacances / sportif", "Centre de vacances / sportif"
    LEISURE_AUTRE = "Autres établissements de loisirs", "Autres établissements de loisirs"
    # autres
    AUTRES_AUTRE = "Autres établissements non listés", "Autres établissements non listés"


ADMINISTRATION_SECTOR_LIST = [
    Sector.ADMINISTRATION_PRISON,
    Sector.ADMINISTRATION_ADMINISTRATIF,
    Sector.ADMINISTRATION_ARMEE,
    Sector.ADMINISTRATION_ETABLISSEMENT_PUBLIC,
    Sector.ADMINISTRATION_INTER_ADMINISTRATIF,
    Sector.ADMINISTRATION_ADMINISTRATIF_DES_COLLECTIVITES,
]
ENTERPRISE_SECTOR_LIST = [
    Sector.ENTERPRISE_ENTREPRISE,
    Sector.ENTERPRISE_INTER_ENTREPRISE,
]
EDUCATION_SECTOR_LIST = [
    Sector.EDUCATION_PRIMAIRE,
    Sector.EDUCATION_SECONDAIRE_COLLEGE,
    Sector.EDUCATION_SECONDAIRE_LYCEE,
    Sector.EDUCATION_ENSEIGNEMENT_AGRICOLE,
    Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE,
    Sector.EDUCATION_AUTRE,
]
HEALTH_SECTOR_LIST = [
    Sector.HEALTH_HOPITAL,
    Sector.HEALTH_CLINIQUE,
    Sector.HEALTH_AUTRE,
]
SOCIAL_SECTOR_LIST = [
    Sector.SOCIAL_CRECHE,
    Sector.SOCIAL_IME,
    Sector.SOCIAL_ESAT,
    Sector.SOCIAL_EHPAD,
    Sector.SOCIAL_PJJ,
    Sector.SOCIAL_AUTRE,
]
LEISURE_SECTOR_LIST = [
    Sector.LEISURE_CENTRE_VACANCE,
    Sector.LEISURE_AUTRE,
]
AUTRES_SECTOR_LIST = [
    Sector.AUTRES_AUTRE,
]


SECTOR_HAS_LINE_MINISTRY_LIST = [
    Sector.ADMINISTRATION_PRISON,
    Sector.ADMINISTRATION_ADMINISTRATIF,
    Sector.ADMINISTRATION_ARMEE,
    Sector.ADMINISTRATION_ETABLISSEMENT_PUBLIC,
    Sector.ADMINISTRATION_INTER_ADMINISTRATIF,
    Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE,
    Sector.EDUCATION_AUTRE,
    Sector.SOCIAL_PJJ,
]


# SECTEURS_SPE = [26, 24, 23, 22, 4, 2]
SECTOR_SPE_LIST = [
    Sector.ADMINISTRATION_PRISON,
    Sector.ADMINISTRATION_ADMINISTRATIF,
    Sector.ADMINISTRATION_ARMEE,
    Sector.ADMINISTRATION_ETABLISSEMENT_PUBLIC,
    Sector.ADMINISTRATION_INTER_ADMINISTRATIF,
    Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE,
]


def get_sector_category_from_sector(sector: str) -> str:
    if sector in ADMINISTRATION_SECTOR_LIST:
        return SectorCategory.ADMINISTRATION
    elif sector in ENTERPRISE_SECTOR_LIST:
        return SectorCategory.ENTERPRISE
    elif sector in EDUCATION_SECTOR_LIST:
        return SectorCategory.EDUCATION
    elif sector in HEALTH_SECTOR_LIST:
        return SectorCategory.HEALTH
    elif sector in SOCIAL_SECTOR_LIST:
        return SectorCategory.SOCIAL
    elif sector in LEISURE_SECTOR_LIST:
        return SectorCategory.LEISURE
    else:
        return SectorCategory.AUTRES


class SectorM2M(models.Model):
    class Meta:
        verbose_name = "secteur d'activité"
        verbose_name_plural = "secteurs d'activité"

    class Categories(models.TextChoices):
        ADMINISTRATION = "administration", "Administration"
        ENTERPRISE = "enterprise", "Entreprise"
        EDUCATION = "education", "Enseignement"
        HEALTH = "health", "Santé"
        SOCIAL = "social", "Social / Médico-social"
        LEISURE = "leisure", "Loisirs"
        AUTRES = "autres", "Autres"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    name = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=Categories.choices,
        null=True,
        blank=True,
        verbose_name="catégorie",
    )
    has_line_ministry = models.BooleanField(default=False, verbose_name="Afficher le champ « Ministère de tutelle »")

    @classmethod
    def choices(self):
        return [(x.id, x.__str__()) for x in self.objects.all()]

    def __str__(self):
        return self.name
