from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Case, F, Func, Value, When


class SectorCategory(models.TextChoices):
    ADMINISTRATION = "administration", "Administration"
    ENTERPRISE = "enterprise", "Entreprise"  # TODO: rename to ENTREPRISE?
    EDUCATION = "education", "Enseignement"
    HEALTH = "health", "Santé"  # TODO: rename to SANTE?
    SOCIAL = "social", "Social / Médico-social"
    LEISURE = "leisure", "Loisirs"  # TODO: rename to LOISIR?
    AUTRES = "autres", "Autres"


class Sector(models.TextChoices):
    # administration
    ADMINISTRATION_PRISON = "administration_prison", "Restaurants des prisons"
    ADMINISTRATION_ADMINISTRATIF = "administration_administratif", "Restaurants administratifs d'Etat (RA)"
    ADMINISTRATION_ARMEE = (
        "administration_armee",
        "Restaurants des armées / police / gendarmerie",
    )
    ADMINISTRATION_ETABLISSEMENT_PUBLIC = (
        "administration_etablissement_public",
        "Etablissements publics d'Etat (EPA ou EPIC)",
    )
    ADMINISTRATION_INTER_ADMINISTRATIF = (
        "administration_inter_administratif",
        "Restaurants inter-administratifs d'État (RIA)",
    )
    ADMINISTRATION_ADMINISTRATIF_DES_COLLECTIVITES = (
        "administration_administratif_des_collectivites",
        "Restaurants administratifs des collectivités territoriales",
    )
    # entreprise
    ENTERPRISE_ENTREPRISE = "entreprise_entreprise", "Restaurants d'entreprises"
    ENTERPRISE_INTER_ENTREPRISE = "entreprise_inter_entreprise", "Restaurants inter-entreprises"
    # education
    EDUCATION_PRIMAIRE = "education_primaire", "Ecole primaire (maternelle et élémentaire)"
    EDUCATION_SECONDAIRE_COLLEGE = "education_secondaire_college", "Secondaire collège"
    EDUCATION_SECONDAIRE_LYCEE = "education_secondaire_lycee", "Secondaire lycée (hors agricole)"
    EDUCATION_ENSEIGNEMENT_AGRICOLE = (
        "education_enseignement_agricole",
        "Etablissements d'enseignement agricole",
    )
    EDUCATION_SUPERIEUR_UNIVERSITAIRE = "education_superieur_universitaire", "Supérieur et Universitaire"
    EDUCATION_AUTRE = "education_autre", "Autres structures d'enseignement"
    # sante
    SANTE_HOPITAL = "sante_hopital", "Hôpitaux"
    SANTE_CLINIQUE = "sante_clinique", "Cliniques"
    SANTE_AUTRE = "sante_autre", "Autres établissements de soins"
    # social
    SOCIAL_CRECHE = "social_creche", "Crèche"
    SOCIAL_IME = "social_ime", "IME / ITEP"
    SOCIAL_ESAT = "social_esat", "ESAT / Etablissements spécialisés"
    SOCIAL_EHPAD = (
        "social_ehpad",
        "EHPAD / maisons de retraite / foyers de personnes âgées",
    )
    SOCIAL_PJJ = "social_pjj", "Etablissements de la PJJ"
    SOCIAL_AUTRE = "social_autre", "Autres établissements sociaux et médico-sociaux"
    # loisir
    LOISIR_CENTRE_VACANCES = "loisir_centre_vacances", "Centre de vacances / sportif"
    LOISIR_AUTRE = "loisir_autre", "Autres établissements de loisirs"
    # autres
    AUTRES_AUTRE = "autres_autre", "Autres établissements non listés"


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
    Sector.SANTE_HOPITAL,
    Sector.SANTE_CLINIQUE,
    Sector.SANTE_AUTRE,
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
    Sector.LOISIR_CENTRE_VACANCES,
    Sector.LOISIR_AUTRE,
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


def get_sector_lib_list_from_sector_list(sector_list: list[str]) -> list[str]:
    return [Sector(sector).label for sector in (sector_list or []) if sector in Sector.values]


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


def get_category_lib_list_from_sector_list(sector_list: list[str]) -> list[str]:
    category_lib_list = []
    for sector in sector_list or []:
        if sector:
            category_lib_list.append(get_sector_category_from_sector(sector).label)
    return list(dict.fromkeys(category_lib_list))  # remove duplicates while preserving order


def is_sector_with_line_ministry(sector: str) -> bool:
    return sector in SECTOR_HAS_LINE_MINISTRY_LIST


def annotate_with_sector_category_list(queryset):
    """
    Annotate with sector_category_list based on the sector_list field.
    Returns an array of categories.
    """
    queryset = queryset.annotate(
        _sector_category_administration=Case(
            When(sector_list__overlap=ADMINISTRATION_SECTOR_LIST, then=Value([SectorCategory.ADMINISTRATION])),
            default=Value([], output_field=ArrayField(models.TextField())),
        ),
        _sector_category_enterprise=Case(
            When(sector_list__overlap=ENTERPRISE_SECTOR_LIST, then=Value([SectorCategory.ENTERPRISE])),
            default=Value([], output_field=ArrayField(models.TextField())),
        ),
        _sector_category_education=Case(
            When(sector_list__overlap=EDUCATION_SECTOR_LIST, then=Value([SectorCategory.EDUCATION])),
            default=Value([], output_field=ArrayField(models.TextField())),
        ),
        _sector_category_health=Case(
            When(sector_list__overlap=HEALTH_SECTOR_LIST, then=Value([SectorCategory.HEALTH])),
            default=Value([], output_field=ArrayField(models.TextField())),
        ),
        _sector_category_social=Case(
            When(sector_list__overlap=SOCIAL_SECTOR_LIST, then=Value([SectorCategory.SOCIAL])),
            default=Value([], output_field=ArrayField(models.TextField())),
        ),
        _sector_category_leisure=Case(
            When(sector_list__overlap=LEISURE_SECTOR_LIST, then=Value([SectorCategory.LEISURE])),
            default=Value([], output_field=ArrayField(models.TextField())),
        ),
        _sector_category_autres=Case(
            When(sector_list__overlap=AUTRES_SECTOR_LIST, then=Value([SectorCategory.AUTRES])),
            default=Value([], output_field=ArrayField(models.TextField())),
        ),
    )
    # array_cat: Postgres function that concatenates two arrays
    queryset = queryset.annotate(
        _cat1=Func(F("_sector_category_administration"), F("_sector_category_enterprise"), function="array_cat")
    )
    queryset = queryset.annotate(_cat2=Func(F("_cat1"), F("_sector_category_education"), function="array_cat"))
    queryset = queryset.annotate(_cat3=Func(F("_cat2"), F("_sector_category_health"), function="array_cat"))
    queryset = queryset.annotate(_cat4=Func(F("_cat3"), F("_sector_category_social"), function="array_cat"))
    queryset = queryset.annotate(_cat5=Func(F("_cat4"), F("_sector_category_leisure"), function="array_cat"))
    queryset = queryset.annotate(
        sector_category_list=Func(
            F("_cat5"), F("_sector_category_autres"), function="array_cat", output_field=ArrayField(models.TextField())
        )
    )
    return queryset


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
