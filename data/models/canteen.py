from urllib.parse import quote
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from data.department_choices import Department
from data.region_choices import Region
from data.utils import get_region, optimize_image
from .sector import Sector
from .softdeletionmodel import SoftDeletionModel


def validate_siret(siret):
    """
    Performs length and Luhn validation
    (https://portal.hardis-group.com/pages/viewpage.action?pageId=120357227)
    """
    if siret is None or siret == "":
        return
    if len(siret) != 14:
        raise ValidationError("14 caractères numériques sont attendus")
    odd_digits = [int(n) for n in siret[-1::-2]]
    even_digits = [int(n) for n in siret[-2::-2]]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(int(n) for n in str(digit * 2))
    luhn_checksum_valid = checksum % 10 == 0

    if not luhn_checksum_valid:
        raise ValidationError("Le numéro SIRET n'est pas valide.")


class Canteen(SoftDeletionModel):
    class Meta:
        verbose_name = "cantine"
        verbose_name_plural = "cantines"
        ordering = ["-creation_date"]

    class ManagementType(models.TextChoices):
        DIRECT = "direct", "Directe"
        CONCEDED = "conceded", "Concédée"

    class ProductionType(models.TextChoices):
        CENTRAL = "central", "Cuisine centrale sans lieu de consommation"
        CENTRAL_SERVING = "central_serving", "Cuisine centrale qui accueille aussi des convives sur place"
        ON_SITE = "site", "Cantine qui produit les repas sur place"
        ON_SITE_CENTRAL = "site_cooked_elsewhere", "Cantine qui sert des repas preparés par une cuisine centrale"

    class PublicationStatus(models.TextChoices):
        DRAFT = "draft", "🔒 Non publié"
        PENDING = "pending", "❓ En attente de vérification"
        PUBLISHED = "published", "✅ Publié"

    class EconomicModel(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Privé"

    class Ministries(models.TextChoices):
        PREMIER_MINISTRE = "premier_ministre", "Service du Premier Ministre"
        AFFAIRES_ETRANGERES = "affaires_etrangeres", "Ministère de l’Europe et des Affaires étrangères"
        ECOLOGIE = "ecologie", "Ministère de la Transition écologique"
        JEUNESSE = "jeunesse", "Ministère de l’Education Nationale et de la Jeunesse et des Sports"
        ECONOMIE = "economie", "Ministère de l’Economie, de la Finance et de la Relance"
        ARMEE = "armee", "Ministère de l’Armée"
        INTERIEUR = "interieur", "Ministère de l’Intérieur"
        TRAVAIL = "travail", "Ministère Travail, de l’Emploi et de l’Insertion"
        OUTRE_MER = "outre_mer", "Ministère des Outre-mer"
        TERRITOIRES = (
            "territoires",
            "Ministère de la Cohésion des Territoires et des Relations avec les Collectivités Territoriales",
        )
        JUSTICE = "justice", "Ministère de la Justice"
        CULTURE = "culture", "Ministère de la Culture"
        SANTE = "sante", "Ministère des Solidarités et de la Santé"
        MER = "mer", "Ministère de la Mer"
        ENSEIGNEMENT_SUPERIEUR = (
            "enseignement_superieur",
            "Ministère de l’Enseignement Supérieur et de la Recherche et de l’Innovation",
        )
        AGRICULTURE = "agriculture", "Ministère de l’Agriculture et de l’Alimentation"
        TRANSFORMATION = "transformation", "Ministère de la Transformation et de la Fonction Publiques"
        AUTRE = "autre", "Autre"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    name = models.TextField(verbose_name="nom")

    city = models.TextField(null=True, blank=True, verbose_name="ville")
    city_insee_code = models.TextField(null=True, blank=True, verbose_name="Code INSEE")

    department = models.TextField(null=True, blank=True, choices=Department.choices, verbose_name="département")
    region = models.TextField(null=True, blank=True, choices=Region.choices, verbose_name="région")
    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name="code postal")
    sectors = models.ManyToManyField(Sector, blank=True, verbose_name="secteurs d'activité")
    line_ministry = models.TextField(
        null=True, blank=True, choices=Ministries.choices, verbose_name="Ministère de tutelle"
    )
    managers = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="canteens",
        verbose_name="gestionnaires",
    )

    daily_meal_count = models.IntegerField(null=True, blank=True, verbose_name="repas par jour")
    satellite_canteens_count = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="nombre de cantines satellites dépendantes (si cuisine centrale)",
    )

    # TODO: once have a standardised format (see _normalise_siret), index by siret if given
    siret = models.TextField(null=True, blank=True, validators=[validate_siret])
    central_producer_siret = models.TextField(
        null=True,
        blank=True,
        verbose_name="siret de la cuisine centrale (si cuisine satellite)",
        validators=[validate_siret],
    )
    management_type = models.CharField(
        max_length=255,
        choices=ManagementType.choices,
        null=True,
        blank=True,
        verbose_name="mode de gestion",
    )
    production_type = models.CharField(
        max_length=255,
        choices=ProductionType.choices,
        null=True,
        blank=True,
        verbose_name="mode de production",
    )

    logo = models.ImageField(null=True, blank=True, verbose_name="Logo")

    economic_model = models.CharField(
        max_length=50,
        choices=EconomicModel.choices,
        null=True,
        blank=True,
        verbose_name="Secteur économique",
    )

    # Publication things
    publication_status = models.CharField(
        max_length=50,
        choices=PublicationStatus.choices,
        default="draft",
        verbose_name="état de publication",
    )
    publication_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="commentaires de publication",
    )
    quality_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="commentaires de mesure appro",
    )
    waste_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="commentaires de mesure gaspillage",
    )
    diversification_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="commentaires de mesure diversification",
    )
    plastics_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="commentaires de mesure plastiques",
    )
    information_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="commentaires de mesure information",
    )

    # experiments
    reservation_expe_participant = models.BooleanField(
        null=True, blank=True, verbose_name="participnte à l'expérimentation réservation"
    )

    vegetarian_expe_participant = models.BooleanField(
        null=True, blank=True, verbose_name="participnte à l'expérimentation repas végétariens"
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        max_image_size = 1024
        if self.logo:
            self.logo = optimize_image(self.logo, self.logo.name, max_image_size)
        if self.department:
            self.region = self._get_region()
        super(Canteen, self).save(force_insert, force_update, using, update_fields)

    @property
    def url_slug(self):
        return f"{self.id}--{quote(self.name)}"

    @property
    def url_path(self):
        return f"/nos-cantines/{self.url_slug}"

    def __str__(self):
        return f'Cantine "{self.name}"'

    def update_publication_comments(self, data):
        self.publication_comments = data.get("publication_comments")
        self.quality_comments = data.get("quality_comments")
        self.waste_comments = data.get("waste_comments")
        self.diversification_comments = data.get("diversification_comments")
        self.plastics_comments = data.get("plastics_comments")
        self.information_comments = data.get("information_comments")

    def _get_region(self):
        return get_region(self.department)


class CanteenImage(models.Model):
    canteen = models.ForeignKey(Canteen, related_name="images", on_delete=models.CASCADE, null=True)
    image = models.ImageField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image = optimize_image(self.image, self.image.name)
        super(CanteenImage, self).save(force_insert, force_update, using, update_fields)
