from urllib.parse import quote
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.functional import cached_property
from simple_history.models import HistoricalRecords
from data.department_choices import Department
from data.region_choices import Region
from data.fields import ChoiceArrayField
from data.utils import get_region, optimize_image
from data.utils import get_diagnostic_lower_limit_year, get_diagnostic_upper_limit_year
from .sector import Sector
from .softdeletionmodel import SoftDeletionModel, SoftDeletionManager, SoftDeletionQuerySet


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


def get_diagnostic_year_choices():
    return [(y, str(y)) for y in range(get_diagnostic_lower_limit_year(), get_diagnostic_upper_limit_year())]


def list_properties(queryset, property):
    return list(queryset.values_list(property, flat=True))


class CanteenQuerySet(SoftDeletionQuerySet):
    def publicly_visible(self):
        return (
            self.exclude(line_ministry=Canteen.Ministries.ARMEE)
            if settings.PUBLISH_BY_DEFAULT
            else self.filter(publication_status=Canteen.PublicationStatus.PUBLISHED)
        )

    def publicly_hidden(self):
        return (
            self.filter(line_ministry=Canteen.Ministries.ARMEE)
            if settings.PUBLISH_BY_DEFAULT
            else self.exclude(publication_status=Canteen.PublicationStatus.PUBLISHED)
        )


class CanteenManager(SoftDeletionManager):
    queryset_model = CanteenQuerySet

    def publicly_visible(self):
        return self.get_queryset().publicly_visible()

    def publicly_hidden(self):
        return self.get_queryset().publicly_hidden()


class Canteen(SoftDeletionModel):
    objects = CanteenManager()
    all_objects = CanteenManager(alive_only=False)

    class Meta:
        verbose_name = "cantine"
        verbose_name_plural = "cantines"
        ordering = ["-creation_date"]
        indexes = [
            models.Index(fields=["siret"]),
            models.Index(fields=["central_producer_siret"]),
        ]

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
        PUBLISHED = "published", "✅ Publié"

    class EconomicModel(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Privé"

    class Actions(models.TextChoices):
        ADD_SATELLITES = "10_add_satellites", "Ajouter des satellites"
        PREFILL_DIAGNOSTIC = "18_prefill_diagnostic", "Créer et pré-remplir le diagnostic"
        CREATE_DIAGNOSTIC = "20_create_diagnostic", "Créer le diagnostic"
        COMPLETE_DIAGNOSTIC = "30_complete_diagnostic", "Compléter le diagnostic"
        FILL_CANTEEN_DATA = "35_fill_canteen_data", "Compléter les infos de la cantine"
        TELEDECLARE = "40_teledeclare", "Télédéclarer"
        PUBLISH = "50_publish", "Publier"
        NOTHING = "95_nothing", "Rien à faire !"

    class Ministries(models.TextChoices):
        PREMIER_MINISTRE = "premier_ministre", "Services du Premier Ministre"
        AFFAIRES_ETRANGERES = "affaires_etrangeres", "Ministère en charge des affaires étrangères"
        ECOLOGIE = "ecologie", "Ministère de la Transition écologique"
        JEUNESSE = "jeunesse", "Ministère en charge de l'Éducation, de la Jeunesse et des Sports"
        ECONOMIE = "economie", "Ministère en charge de l'Économie et des finances"
        ARMEE = "armee", "Ministère des Armées"
        INTERIEUR = "interieur", "Ministère de l’Intérieur"
        TRAVAIL = "travail", "Ministère en charge du Travail"
        OUTRE_MER = "outre_mer", "Ministère des Outre-mer"
        TERRITOIRES = (
            "territoires",
            "Ministère de la Cohésion des Territoires et des Relations avec les Collectivités Territoriales",
        )
        JUSTICE = "justice", "Ministère de la Justice"
        CULTURE = "culture", "Ministère de la Culture"
        SANTE = "sante", "Ministère en charge de la Santé et des Solidarités"
        MER = "mer", "Ministère de la Mer"
        ENSEIGNEMENT_SUPERIEUR = (
            "enseignement_superieur",
            "Ministère en charge de l'Enseignement supérieur et de la Recherche",
        )
        AGRICULTURE = "agriculture", "Ministère en charge de l'Agriculture et de l'Alimentation"
        TRANSFORMATION = "transformation", "Ministère de la Transformation et de la Fonction Publiques"
        ADMINISTRATION_TERRITORIALE = (
            "administration_territoriale",
            "Préfecture - Administration Territoriale de l'État (ATE)",
        )
        AUTORITES_INDEPENDANTES = (
            "autorites_independantes",
            "Présidence de la république - Autorités indépendantes (AAI, API)",
        )
        AUTRE = "autre", "Autre"

    import_source = models.TextField(null=True, blank=True, verbose_name="Source de l'import de la cantine")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

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
    claimed_by = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        verbose_name="Personne qui a revendiqué la cantine",
        on_delete=models.SET_NULL,
    )
    has_been_claimed = models.BooleanField(default=False, verbose_name="cette cantine a été revendiquée")

    daily_meal_count = models.IntegerField(null=True, blank=True, verbose_name="repas par jour")
    yearly_meal_count = models.IntegerField(null=True, blank=True, verbose_name="repas par an (y compris livrés)")
    satellite_canteens_count = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="nombre de cantines satellites dépendantes (si cuisine centrale)",
    )

    # TODO: consider using normalise_siret on save
    siret = models.TextField(null=True, blank=True, validators=[validate_siret])
    central_producer_siret = models.TextField(
        null=True,
        blank=True,
        verbose_name="siret de la cuisine centrale",
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
    redacted_appro_years = ChoiceArrayField(
        base_field=models.IntegerField(choices=get_diagnostic_year_choices),
        default=list,
        blank=True,
        verbose_name="les années pour lesquelles les données d'appro sont masquées",
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
        null=True, blank=True, verbose_name="participante à l'expérimentation réservation"
    )

    vegetarian_expe_participant = models.BooleanField(
        null=True, blank=True, verbose_name="participante à l'expérimentation repas végétariens"
    )

    # Email campaigns
    email_no_diagnostic_first_reminder = models.DateTimeField(
        null=True, blank=True, verbose_name="Date d'envoi du premier email pour manque de diagnostics"
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        max_image_size = 1024
        if self.logo:
            self.logo = optimize_image(self.logo, self.logo.name, max_image_size)
        if self.department:
            self.region = self._get_region()
        super(Canteen, self).save(force_insert, force_update, using, update_fields)

    # Automatic tasks
    geolocation_bot_attempts = models.IntegerField(default=0)

    # Campaign tracking
    creation_mtm_source = models.TextField(
        null=True, blank=True, verbose_name="mtm_source du lien tracké lors de la création"
    )
    creation_mtm_campaign = models.TextField(
        null=True, blank=True, verbose_name="mtm_campaign du lien tracké lors de la création"
    )
    creation_mtm_medium = models.TextField(
        null=True, blank=True, verbose_name="mtm_medium du lien tracké lors de la création"
    )

    @property
    def url_slug(self):
        return f"{self.id}--{quote(self.name)}"

    @property
    def url_path(self):
        return f"/nos-cantines/{self.url_slug}"

    @property
    def satellites(self):
        if self.siret:
            return Canteen.objects.filter(
                central_producer_siret=self.siret,
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            )
        return Canteen.objects.none()

    @property
    def is_central_cuisine(self):
        return self.production_type and self.production_type in [
            Canteen.ProductionType.CENTRAL,
            Canteen.ProductionType.CENTRAL_SERVING,
        ]

    @property
    def is_satellite(self):
        return self.production_type and self.production_type == Canteen.ProductionType.ON_SITE_CENTRAL

    @property
    def central_kitchen(self):
        if self.is_satellite and self.central_producer_siret:
            central_types = [Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING]
            try:
                return Canteen.objects.get(siret=self.central_producer_siret, production_type__in=central_types)
            except (Canteen.DoesNotExist, Canteen.MultipleObjectsReturned):
                return None

    @property
    def central_kitchen_diagnostics(self):
        if self.central_kitchen:
            return self.central_kitchen.diagnostic_set.filter(central_kitchen_diagnostic_mode__isnull=False)

    @property
    def can_be_claimed(self):
        return not self.managers.exists()

    def has_diagnostic_for_year(self, year):
        has_diagnostics = self.diagnostic_set.filter(year=year).exists()
        has_central_kitchen_diagnostic = (
            self.central_kitchen_diagnostics and self.central_kitchen_diagnostics.filter(year=year).exists()
        )
        return has_diagnostics or has_central_kitchen_diagnostic

    def has_teledeclaration_for_year(self, year):
        from .teledeclaration import Teledeclaration  # Circular import

        has_canteen_td = self.teledeclaration_set.filter(
            year=year, status=Teledeclaration.TeledeclarationStatus.SUBMITTED
        ).exists()
        has_central_kitchen_td = (
            self.central_kitchen.teledeclaration_set.filter(
                year=year, status=Teledeclaration.TeledeclarationStatus.SUBMITTED
            ).exists()
            if self.central_kitchen
            else False
        )
        return has_canteen_td or has_central_kitchen_td

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

    @cached_property
    def appro_diagnostics(self):
        diag_ids = list_properties(self.diagnostic_set, "id")

        if self.central_kitchen_diagnostics:
            # for any given year, could have own diag or CC diag
            # CC diag always takes precedent TODO: do we consistently assume this?
            # if don't have own diag, include CC diag in set
            cc_diag_years = list_properties(self.central_kitchen_diagnostics, "year")
            own_diagnostics = self.diagnostic_set.exclude(year__in=cc_diag_years)

            diag_ids = list_properties(self.central_kitchen_diagnostics, "id")
            diag_ids += list_properties(own_diagnostics, "id")

        from data.models import Diagnostic

        this_year = timezone.now().date().year
        return Diagnostic.objects.filter(id__in=diag_ids, year__lt=this_year).order_by("-year")

    @cached_property
    def service_diagnostics(self):
        diag_ids = list_properties(self.diagnostic_set, "id")

        if self.central_kitchen_diagnostics:
            cc_service_diagnostics = self.central_kitchen_diagnostics.filter(central_kitchen_diagnostic_mode="ALL")
            # for any given year, could have own diag or CC diag
            # CC diag always takes precedent, if ALL TODO: do we consistently assume this?
            # if don't have own diag, include CC diag in set
            cc_diag_years = list_properties(cc_service_diagnostics, "year")
            own_diagnostics = self.diagnostic_set.exclude(year__in=cc_diag_years)

            diag_ids = list_properties(cc_service_diagnostics, "id")
            diag_ids += list_properties(own_diagnostics, "id")

        from data.models import Diagnostic

        this_year = timezone.now().date().year
        return Diagnostic.objects.filter(id__in=diag_ids, year__lt=this_year).order_by("-year")

    @cached_property
    def published_appro_diagnostics(self):
        diagnostics_to_redact = []
        for year in self.redacted_appro_years:
            diag = self.appro_diagnostics.filter(year=year).first()
            if diag and not diag.is_teledeclared:
                diagnostics_to_redact.append(diag.id)
        return self.appro_diagnostics.exclude(id__in=diagnostics_to_redact)

    @cached_property
    def published_service_diagnostics(self):
        # a wrapper to have consistent naming conventions
        return self.service_diagnostics

    @cached_property
    def latest_published_year(self):
        if not self.published_appro_diagnostics and not self.published_service_diagnostics:
            return

        latest_appro = self.published_appro_diagnostics.only("year").first()
        latest_service = self.published_service_diagnostics.only("year").first()

        appro_year = latest_appro.year if latest_appro else 0
        service_year = latest_service.year if latest_service else 0

        max_year = max(appro_year, service_year)
        return max_year if max_year > 0 else None

    @cached_property
    def latest_published_appro_diagnostic(self):
        return self.published_appro_diagnostics.filter(year=self.latest_published_year).first()

    @cached_property
    def latest_published_service_diagnostic(self):
        return self.published_service_diagnostics.filter(year=self.latest_published_year).first()

    @property
    def in_education(self):
        scolaire_sectors = Sector.objects.filter(category="education")
        if scolaire_sectors.count() and self.sectors.intersection(scolaire_sectors).exists():
            return True

    @property
    def lead_image(self):
        return self.images.first()


class CanteenImage(models.Model):
    canteen = models.ForeignKey(Canteen, related_name="images", on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    alt_text = models.TextField(
        null=True,
        blank=True,
        verbose_name="texte alternatif pour les utilisateurs qui voient pas l'image",
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image = optimize_image(self.image, self.image.name)
        super(CanteenImage, self).save(force_insert, force_update, using, update_fields)
