from urllib.parse import quote

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Case, Count, Exists, F, OuterRef, Q, Subquery, Value, When
from django.utils import timezone
from django.utils.functional import cached_property
from simple_history.models import HistoricalRecords

from common.utils import siret as utils_siret
from data.department_choices import Department
from data.fields import ChoiceArrayField
from data.models.sector import Sector
from data.region_choices import Region
from data.utils import (
    get_diagnostic_lower_limit_year,
    get_diagnostic_upper_limit_year,
    get_region,
    optimize_image,
)

from .softdeletionmodel import (
    SoftDeletionManager,
    SoftDeletionModel,
    SoftDeletionQuerySet,
)


def get_diagnostic_year_choices():
    return [(y, str(y)) for y in range(get_diagnostic_lower_limit_year(), get_diagnostic_upper_limit_year())]


def list_properties(queryset, property):
    return list(queryset.values_list(property, flat=True))


def has_siret_or_siren_unite_legale_query():
    has_siret_query = Q(siret__isnull=False) & ~Q(siret="")
    has_siren_unite_legale_query = Q(siren_unite_legale__isnull=False) & ~Q(siren_unite_legale="")
    return has_siret_query | has_siren_unite_legale_query


def is_serving_query():
    return Q(
        production_type__in=[
            Canteen.ProductionType.CENTRAL_SERVING,
            Canteen.ProductionType.ON_SITE,
            Canteen.ProductionType.ON_SITE_CENTRAL,
        ]
    )


def is_satellite_query():
    return Q(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)


def is_central_cuisine_query():
    return Q(production_type__in=[Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING])


def has_missing_data_query():
    return (
        Q(name=None)
        | Q(city_insee_code=None)
        | Q(city_insee_code="")
        | Q(yearly_meal_count=None)
        | Q(~has_siret_or_siren_unite_legale_query())
        | Q(production_type=None)
        | Q(management_type=None)
        | Q(economic_model=None)
        | Q(is_serving_query()) & (Q(daily_meal_count=None) | Q(daily_meal_count=0))
        | (is_satellite_query() & (Q(central_producer_siret=None) | Q(central_producer_siret="")))
        | (is_satellite_query() & Q(central_producer_siret=F("siret")))
        | (is_central_cuisine_query() & (Q(satellite_canteens_count=None) | Q(satellite_canteens_count=0)))
        | (
            Q(economic_model=Canteen.EconomicModel.PUBLIC) & Q(requires_line_ministry=True) & Q(line_ministry=None)
        )  # with annotate_with_requires_line_ministry()
    )


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

    def is_satellite(self):
        return self.filter(is_satellite_query())

    def annotate_with_central_kitchen_id(self):
        central_kitchen = Canteen.objects.filter(siret=OuterRef("central_producer_siret")).values("id")
        return self.annotate(
            central_kitchen_id=Case(When(is_satellite_query(), Subquery(central_kitchen[:1])), default=None)
        )

    def get_satellites(self, central_producer_siret):
        return self.filter(is_satellite_query(), central_producer_siret=central_producer_siret)

    def annotate_with_satellites_in_db_count(self):
        # https://docs.djangoproject.com/en/4.1/ref/models/expressions/#using-aggregates-within-a-subquery-expression
        satellites = (
            Canteen.objects.filter(central_producer_siret=OuterRef("siret"))
            .order_by()
            .values("central_producer_siret")
        )  # sets the groupBy for the aggregation
        satellites_count = satellites.annotate(count=Count("id")).values("count")
        return self.annotate(
            satellites_in_db_count=Case(When(is_central_cuisine_query(), then=Subquery(satellites_count)), default=0)
        )

    def annotate_with_purchases_for_year(self, year):
        from data.models import Purchase

        purchases_for_year = Purchase.objects.filter(canteen=OuterRef("pk"), date__year=year)
        return self.annotate(has_purchases_for_year=Exists(purchases_for_year))

    def annotate_with_diagnostic_for_year(self, year):
        from data.models import Diagnostic

        diagnostics = Diagnostic.objects.filter(
            Q(canteen=OuterRef("central_kitchen_id")) | Q(canteen=OuterRef("pk")), year=year
        )
        complete_diagnostics = diagnostics.filter(value_total_ht__gt=0)
        diagnostic_for_year_with_cc_mode = Diagnostic.objects.filter(
            pk=OuterRef("diagnostic_for_year"),
            central_kitchen_diagnostic_mode__isnull=False,
        ).exclude(central_kitchen_diagnostic_mode="")
        return self.annotate(
            diagnostic_for_year=Subquery(diagnostics.values("id")[:1]),
            has_complete_diagnostic_for_year=Exists(Subquery(complete_diagnostics)),
            diagnostic_for_year_cc_mode=Subquery(
                diagnostic_for_year_with_cc_mode.values("central_kitchen_diagnostic_mode")[:1]
            ),
        )

    def annotate_with_td_for_year(self, year):
        from data.models import Teledeclaration

        tds = Teledeclaration.objects.filter(
            Q(canteen=OuterRef("pk")) | Q(canteen=OuterRef("central_kitchen_id")),
            year=year,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
        )
        return self.annotate(has_td=Exists(Subquery(tds)))

    def annotate_with_requires_line_ministry(self):
        canteen_sector_relation = apps.get_model(app_label="data", model_name="Canteen_sectors")
        has_sector_requiring_line_ministry = canteen_sector_relation.objects.filter(
            canteen=OuterRef("pk"), sector__has_line_ministry=True
        )
        return self.annotate(requires_line_ministry=Exists(has_sector_requiring_line_ministry))

    def has_siret_or_siren_unite_legale(self):
        return self.filter(has_siret_or_siren_unite_legale_query())

    def has_missing_data(self):
        return self.annotate_with_requires_line_ministry().filter(has_missing_data_query())

    def has_complete_data(self):
        return self.annotate_with_requires_line_ministry().exclude(has_missing_data_query())

    def annotate_with_action_for_year(self, year):
        from data.models import Diagnostic

        # prep add satellites action
        self = self.annotate_with_satellites_in_db_count()
        self = self.annotate_with_central_kitchen_id()
        # prep add diag actions
        self = self.annotate_with_purchases_for_year(year)
        self = self.annotate_with_diagnostic_for_year(year)
        # prep missing data action
        self = self.annotate_with_requires_line_ministry()
        # prep TD action
        self = self.annotate_with_td_for_year(year)
        # annotate with action
        should_teledeclare = settings.ENABLE_TELEDECLARATION
        conditions = [
            When(
                (is_central_cuisine_query() & Q(satellite_canteens_count__gt=0) & Q(satellites_in_db_count=None)),
                then=Value(Canteen.Actions.ADD_SATELLITES),
            ),
            When(
                is_central_cuisine_query() & Q(satellites_in_db_count__lt=F("satellite_canteens_count")),
                then=Value(Canteen.Actions.ADD_SATELLITES),
            ),
            When(
                is_central_cuisine_query() & Q(satellites_in_db_count__gt=F("satellite_canteens_count")),
                then=Value(Canteen.Actions.ADD_SATELLITES),
            ),
            When(
                is_satellite_query()
                & Q(diagnostic_for_year_cc_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL, has_td=False),
                then=Value(Canteen.Actions.NOTHING_SATELLITE),
            ),
            When(
                is_satellite_query()
                & Q(diagnostic_for_year_cc_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL, has_td=True),
                then=Value(Canteen.Actions.NOTHING_SATELLITE_TELEDECLARED),
            ),
            When(
                Q(diagnostic_for_year=None) & Q(has_purchases_for_year=True),
                then=Value(Canteen.Actions.PREFILL_DIAGNOSTIC),
            ),
            When(diagnostic_for_year=None, then=Value(Canteen.Actions.CREATE_DIAGNOSTIC)),
            When(has_complete_diagnostic_for_year=False, then=Value(Canteen.Actions.COMPLETE_DIAGNOSTIC)),
            When(
                (is_central_cuisine_query() & Q(diagnostic_for_year_cc_mode=None)),
                then=Value(Canteen.Actions.COMPLETE_DIAGNOSTIC),
            ),
            When(has_missing_data_query(), then=Value(Canteen.Actions.FILL_CANTEEN_DATA)),
        ]
        if should_teledeclare:
            conditions.append(When(has_td=False, then=Value(Canteen.Actions.TELEDECLARE)))
        if not settings.PUBLISH_BY_DEFAULT:
            conditions.append(
                When(publication_status=Canteen.PublicationStatus.DRAFT, then=Value(Canteen.Actions.PUBLISH))
            )
        return self.annotate(action=Case(*conditions, default=Value(Canteen.Actions.NOTHING)))


class CanteenManager(SoftDeletionManager):
    queryset_model = CanteenQuerySet

    def publicly_visible(self):
        return self.get_queryset().publicly_visible()

    def publicly_hidden(self):
        return self.get_queryset().publicly_hidden()

    def is_satellite(self):
        return self.get_queryset().is_satellite()

    def annotate_with_central_kitchen_id(self):
        return self.get_queryset().annotate_with_central_kitchen_id()

    def get_satellites(self, central_producer_siret):
        return self.get_queryset().get_satellites(central_producer_siret)

    def annotate_with_satellites_in_db_count(self):
        return self.get_queryset().annotate_with_satellites_in_db_count()

    def annotate_with_purchases_for_year(self, year):
        return self.get_queryset().annotate_with_purchases_for_year(year)

    def annotate_with_diagnostic_for_year(self, year):
        return self.get_queryset().annotate_with_diagnostic_for_year(year)

    def annotate_with_td_for_year(self, year):
        return self.get_queryset().annotate_with_td_for_year(year)

    def has_missing_data(self):
        return self.get_queryset().has_missing_data()

    def has_complete_data(self):
        return self.get_queryset().has_complete_data()

    def annotate_with_action_for_year(self, year):
        return self.get_queryset().annotate_with_action_for_year(year)


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
        CENTRAL = "central", "Livreur des repas sans lieu de consommation"
        CENTRAL_SERVING = "central_serving", "Livreur des repas qui accueille aussi des convives sur place"
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
        NOTHING_SATELLITE = "90_nothing_satellite", "En attente de la télédéclaration de votre livreur"
        NOTHING_SATELLITE_TELEDECLARED = (
            "91_nothing_satellite_teledeclared",
            "Rien à faire (télédéclaré par votre livreur)",
        )
        NOTHING = "95_nothing", "Rien à faire !"

    class Ministries(models.TextChoices):
        AFFAIRES_ETRANGERES = "affaires_etrangeres", "Affaires étrangères"
        AGRICULTURE = "agriculture", "Agriculture, Alimentation et Forêts"
        ARMEE = "armee", "Armées"
        TERRITOIRES = "territoires", "Cohésion des territoires - Relations avec les collectivités territoriales"
        CULTURE = "culture", "Culture"
        ECONOMIE = "economie", "Économie et finances"
        JEUNESSE = "jeunesse", "Éducation et Jeunesse"
        ENSEIGNEMENT_SUPERIEUR = "enseignement_superieur", "Enseignement supérieur et Recherche"
        ECOLOGIE = "ecologie", "Environnement"
        TRANSFORMATION = "transformation", "Fonction Publiques"
        INTERIEUR = "interieur", "Intérieur et Outre-mer"
        JUSTICE = "justice", "Justice"
        MER = "mer", "Mer"
        ADMINISTRATION_TERRITORIALE = (
            "administration_territoriale",
            "Préfecture - Administration Territoriale de l'État (ATE)",
        )
        AUTORITES_INDEPENDANTES = (
            "autorites_independantes",
            "Présidence de la république - Autorités indépendantes (AAI, API)",
        )
        PREMIER_MINISTRE = "premier_ministre", "Services du Premier Ministre"
        SANTE = "sante", "Santé et Solidarités"
        SPORT = "sport", "Sport"
        TRAVAIL = "travail", "Travail"
        OUTRE_MER = "outre_mer", "Ministère des Outre-mer"
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

    daily_meal_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="repas par jour")
    yearly_meal_count = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="repas par an (y compris livrés)"
    )
    satellite_canteens_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="nombre de cantines satellites dépendantes (si cuisine centrale)",
    )

    siret = models.TextField(null=True, blank=True, validators=[utils_siret.validate_siret])
    siren_unite_legale = models.TextField(
        null=True, blank=True, verbose_name="siren de l'unité légale", validators=[utils_siret.validate_siren]
    )

    central_producer_siret = models.TextField(
        null=True,
        blank=True,
        verbose_name="siret de la cuisine centrale",
        validators=[utils_siret.validate_siret],
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # cleanup some fields
        if self.siret:
            self.siret = utils_siret.normalise_siret(self.siret)
        if self.siren_unite_legale:
            self.siren_unite_legale = utils_siret.normalise_siret(self.siren_unite_legale)
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

    @property
    def is_serving(self):
        return self.production_type and self.production_type in [
            Canteen.ProductionType.CENTRAL_SERVING,
            Canteen.ProductionType.ON_SITE,
            Canteen.ProductionType.ON_SITE_CENTRAL,
        ]

    @property
    def satellites(self):
        if self.siret:
            return Canteen.objects.get_satellites(self.siret)
        return Canteen.objects.none()

    @property
    def is_central_cuisine(self) -> bool:
        return self.production_type and self.production_type in [
            Canteen.ProductionType.CENTRAL,
            Canteen.ProductionType.CENTRAL_SERVING,
        ]

    @property
    def is_satellite(self) -> bool:
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

    @property
    def has_complete_data(self) -> bool:
        # basic rules
        has_complete_data = (
            bool(self.name)
            and bool(self.city_insee_code)
            and bool(self.yearly_meal_count)
            and bool(self.siret or self.siren_unite_legale)
            and bool(self.production_type)
            and bool(self.management_type)
            and bool(self.economic_model)
        )
        # serving-specific rules
        if has_complete_data and self.is_serving:
            has_complete_data = bool(self.daily_meal_count)
        # satellite-specific rules
        if has_complete_data and self.is_satellite:
            has_complete_data = bool(self.central_producer_siret and self.central_producer_siret != self.siret)
        # cc-specific rules
        if has_complete_data and self.is_central_cuisine:
            has_complete_data = bool(self.satellite_canteens_count)
            # We check again to avoid useless DB hits
            if has_complete_data:
                has_complete_data = (
                    Canteen.objects.filter(central_producer_siret=self.siret).count() == self.satellite_canteens_count
                )
        # sectors & line_ministry
        if has_complete_data:
            has_complete_data = self.sectors.exists()
        if has_complete_data and self.sectors.filter(has_line_ministry=True).exists():
            has_complete_data = bool(self.line_ministry)
        return has_complete_data

    def has_diagnostic_for_year(self, year):
        has_diagnostics = self.diagnostic_set.filter(year=year).exists()
        has_central_kitchen_diagnostic = (
            self.central_kitchen_diagnostics and self.central_kitchen_diagnostics.filter(year=year).exists()
        )
        return has_diagnostics or has_central_kitchen_diagnostic

    def has_teledeclaration_for_year(self, year):
        from data.models.teledeclaration import Teledeclaration

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

    @property
    def publication_status_display_to_public(self):
        if not settings.PUBLISH_BY_DEFAULT:
            return self.publication_status
        if self.line_ministry == Canteen.Ministries.ARMEE:
            return Canteen.PublicationStatus.DRAFT
        return Canteen.PublicationStatus.PUBLISHED

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
        from data.models import Sector

        scolaire_sectors = Sector.objects.filter(category="education")
        if scolaire_sectors.count() and self.sectors.intersection(scolaire_sectors).exists():
            return True

    @property
    def in_administration(self):
        from data.models import Sector

        administration_sectors = Sector.objects.filter(category="administration")
        if administration_sectors.count() and self.sectors.intersection(administration_sectors).exists():
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
