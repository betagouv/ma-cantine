from urllib.parse import quote

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import ValidationError
from django.db import models
from django.db.models import BooleanField, Case, Count, Exists, F, OuterRef, Q, Subquery, Value, When, Func
from django.utils import timezone
from django.db.models.functions import Coalesce, Length
from django.utils.functional import cached_property
from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason
from dirtyfields import DirtyFieldsMixin

from common.utils import siret as utils_siret
from common.utils import utils as utils_utils
from data.fields import ChoiceArrayField
from data.models.creation_source import CreationSource
from data.models.geo import Department, Region, get_region_from_department
from data.models.sector import (
    SECTOR_HAS_LINE_MINISTRY_LIST,
    Sector,
    SectorM2M,
    ADMINISTRATION_SECTOR_LIST,
    annotate_with_sector_category_list,
)
from data.utils import (
    get_diagnostic_lowest_limit_year,
    get_diagnostic_upper_limit_year,
    has_charfield_missing_query,
    has_arrayfield_missing_query,
    optimize_image,
)
from data.validators import canteen as canteen_validators
from macantine.utils import get_year_campaign_end_date_or_today_date, is_in_correction, is_in_teledeclaration

from .softdeletionmodel import SoftDeletionManager, SoftDeletionModel, SoftDeletionQuerySet


def get_diagnostic_year_choices():
    return [(y, str(y)) for y in range(get_diagnostic_lowest_limit_year(), get_diagnostic_upper_limit_year())]


def list_properties(queryset, property):
    return list(queryset.values_list(property, flat=True))


def has_siret_or_siren_unite_legale_query():
    has_siret_query = ~has_charfield_missing_query("siret")
    has_siren_unite_legale_query = ~has_charfield_missing_query("siren_unite_legale")
    return has_siret_query | has_siren_unite_legale_query


def is_groupe_query():
    return Q(production_type=Canteen.ProductionType.GROUPE)


def is_central_query():
    return Q(production_type=Canteen.ProductionType.CENTRAL)


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


def is_public_query():
    return Q(economic_model=Canteen.EconomicModel.PUBLIC)


def is_filled_query():
    return Q(is_filled=True)


class CanteenQuerySet(SoftDeletionQuerySet):
    def publicly_visible(self):
        return self.exclude(production_type=Canteen.ProductionType.GROUPE).exclude(
            line_ministry=Canteen.Ministries.ARMEE
        )

    def publicly_hidden(self):
        return self.filter(
            Q(production_type=Canteen.ProductionType.GROUPE) | Q(line_ministry=Canteen.Ministries.ARMEE)
        )

    def created_before_year_campaign_end_date(self, year):
        canteen_created_before_date = get_year_campaign_end_date_or_today_date(year)
        if canteen_created_before_date:
            return self.filter(creation_date__lt=canteen_created_before_date)
        return self.none()

    def is_groupe(self):
        return self.filter(is_groupe_query())

    def is_central(self):
        return self.filter(is_central_query())

    def is_serving(self):
        return self.filter(is_serving_query())

    def is_satellite(self):
        return self.filter(is_satellite_query())

    def get_satellites_old(self, central_producer_siret):
        return self.filter(is_satellite_query(), central_producer_siret=central_producer_siret)

    def is_public(self):
        return self.filter(is_public_query())

    def has_geo_data_missing(self):
        return self.filter(
            has_charfield_missing_query("city")
            | has_charfield_missing_query("postal_code")
            | has_charfield_missing_query("epci")
            | has_charfield_missing_query("epci_lib")
            | has_arrayfield_missing_query("pat_list")
            | has_arrayfield_missing_query("pat_lib_list")
            | has_charfield_missing_query("department")
            | has_charfield_missing_query("department_lib")
            | has_charfield_missing_query("region")
            | has_charfield_missing_query("region_lib")
        )

    def candidates_for_siret_to_city_insee_code_bot(self):
        return self.is_serving().has_siret().has_city_insee_code_missing().order_by("-creation_date")

    def candidates_for_city_insee_code_to_geo_data_bot(self):
        return (
            self.is_serving()
            .has_city_insee_code_and_length_5()
            .has_geo_data_missing()
            .filter(geolocation_bot_attempts__lt=20)
            .order_by("creation_date")
        )

    def annotate_with_satellites_in_db_count(self):
        # # https://docs.djangoproject.com/en/4.1/ref/models/expressions/#using-aggregates-within-a-subquery-expression
        # TODO: improve with a related_name on the groupe FK
        satellites = Canteen.objects.filter(groupe_id=OuterRef("pk")).order_by().values("groupe_id")
        satellites_count = satellites.annotate(count=Count("id")).values("count")
        satellites_missing_data = satellites.has_missing_data()
        satellites_missing_data_count = satellites_missing_data.annotate(count=Count("id")).values("count")
        return self.annotate(
            satellites_in_db_count=Case(
                When(is_groupe_query(), then=Coalesce(Subquery(satellites_count), 0)), default=0
            ),
            satellites_in_db_missing_data_count=Case(
                When(is_groupe_query(), then=Coalesce(Subquery(satellites_missing_data_count), 0)), default=0
            ),
        )

    def annotate_with_is_managed_by_user(self, user):
        if not user or user.is_anonymous:
            return self.annotate(is_managed_by_user=Value(False, output_field=BooleanField()))
        return self.annotate(
            is_managed_by_user=Exists(
                self.exclude(managers=None).filter(managers__id=user.id, pk=OuterRef("pk")),
            )
        )

    def annotate_with_purchases_for_year(self, year):
        from data.models import Purchase

        purchases_for_year = Purchase.objects.filter(canteen=OuterRef("pk"), date__year=year)
        return self.annotate(has_purchases_for_year=Exists(purchases_for_year))

    def annotate_with_diagnostic_for_year(self, year):
        from data.models import Diagnostic

        diagnostics = Diagnostic.objects.filter(
            Q(canteen=OuterRef("groupe_id")) | Q(canteen=OuterRef("pk")), year=year
        )
        diagnostics_filled = diagnostics.filled()
        diagnostic_for_year_with_cc_mode = Diagnostic.objects.filter(
            pk=OuterRef("diagnostic_for_year"),
            central_kitchen_diagnostic_mode__isnull=False,
        ).exclude(central_kitchen_diagnostic_mode="")
        diagnostics_teledeclared = diagnostics.teledeclared()
        return self.annotate(
            diagnostic_for_year=Subquery(diagnostics.values("id")[:1]),
            has_diagnostic_filled_for_year=Exists(Subquery(diagnostics_filled)),
            diagnostic_for_year_cc_mode=Subquery(
                diagnostic_for_year_with_cc_mode.values("central_kitchen_diagnostic_mode")[:1]
            ),
            has_diagnostic_teledeclared_for_year=Exists(Subquery(diagnostics_teledeclared)),
        )

    def annotate_with_requires_line_ministry(self):
        """
        requires_line_ministry is True if the canteen has at least one sector requiring line ministry
        sectors requiring line_ministry: {SECTOR_HAS_LINE_MINISTRY_LIST}
        """
        return self.annotate(
            requires_line_ministry=Case(
                When(is_public_query() & Q(sector_list__overlap=SECTOR_HAS_LINE_MINISTRY_LIST), then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )

    def annotate_with_sector_list_count(self):
        return self.annotate(sector_list_count=F("sector_list__len"))

    def annotate_with_sector_category_list(self):
        return annotate_with_sector_category_list(self)

    def has_siret(self):
        return self.exclude(has_charfield_missing_query("siret"))

    def has_siret_or_siren_unite_legale(self):
        return self.filter(has_siret_or_siren_unite_legale_query())

    def has_city_insee_code(self):
        return self.exclude(has_charfield_missing_query("city_insee_code"))

    def has_city_insee_code_missing(self):
        return self.filter(has_charfield_missing_query("city_insee_code"))

    def has_city_insee_code_and_length_5(self):
        return (
            self.has_city_insee_code()
            .annotate(city_insee_code_len=Length("city_insee_code"))
            .filter(city_insee_code_len=5)
        )

    def has_missing_data(self):
        return self.exclude(is_filled_query())

    def is_filled(self):
        return self.filter(is_filled_query())

    def group_and_count_by_field(self, field):
        """
        https://docs.djangoproject.com/en/5.2/topics/db/aggregation/#values
        Example:
        - Input: 4 canteens: 3 with management_type 'direct', 1 with 'conceded'
        - Usage: group_and_count_by_field('management_type')
        - Output: [{'management_type': 'direct', 'count': 3}, {'management_type': 'conceded', 'count': 1}]
        """
        if field == "sector_category":
            self = self.annotate_with_sector_category_list().annotate(
                sector_category=Func(F("sector_category_list"), function="unnest")
            )
        return self.values(field).annotate(count=Count("id", distinct=True)).order_by("-count")

    def annotate_with_action_for_year(self, year):
        from data.models import Diagnostic

        # prep groupe rules
        self = self.annotate_with_satellites_in_db_count()
        # prep add diag & TD actions
        self = self.annotate_with_purchases_for_year(year)
        self = self.annotate_with_diagnostic_for_year(year)
        # annotate with action
        conditions = [
            When(
                is_satellite_query()
                & is_filled_query()
                & Q(
                    diagnostic_for_year_cc_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                    has_diagnostic_teledeclared_for_year=False,
                ),
                then=Value(Canteen.Actions.NOTHING_SATELLITE),
            ),
            When(
                is_satellite_query()
                & Q(
                    diagnostic_for_year_cc_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                    has_diagnostic_teledeclared_for_year=True,
                ),
                then=Value(Canteen.Actions.NOTHING_SATELLITE_TELEDECLARED),
            ),
            When(
                has_diagnostic_teledeclared_for_year=True,
                then=Value(Canteen.Actions.NOTHING),
            ),
            When(
                is_groupe_query() & Q(satellites_in_db_count=0),
                then=Value(Canteen.Actions.ADD_SATELLITES),
            ),
            When(
                Q(diagnostic_for_year=None) & Q(has_purchases_for_year=True),
                then=Value(Canteen.Actions.PREFILL_DIAGNOSTIC),
            ),
            When(diagnostic_for_year=None, then=Value(Canteen.Actions.CREATE_DIAGNOSTIC)),
            When(has_diagnostic_filled_for_year=False, then=Value(Canteen.Actions.FILL_DIAGNOSTIC)),
            When(
                (is_groupe_query() & Q(diagnostic_for_year_cc_mode=None)),
                then=Value(Canteen.Actions.FILL_DIAGNOSTIC),
            ),
            When(~is_filled_query(), then=Value(Canteen.Actions.FILL_CANTEEN_DATA)),
            When(
                is_groupe_query() & Q(satellites_in_db_missing_data_count__gt=0),
                then=Value(Canteen.Actions.FILL_SATELLITE_CANTEEN_DATA),
            ),
        ]
        if is_in_correction():
            # TODO: figure out a way to detect that the canteen has indeed teledeclared during the teledeclaration campaign
            conditions.append(
                When(
                    Q(has_diagnostic_teledeclared_for_year=False),
                    then=Value(Canteen.Actions.TELEDECLARE),
                )
            )
        if is_in_teledeclaration():
            conditions.append(
                When(has_diagnostic_teledeclared_for_year=False, then=Value(Canteen.Actions.TELEDECLARE))
            )
        else:
            conditions.append(
                When(has_diagnostic_teledeclared_for_year=False, then=Value(Canteen.Actions.DID_NOT_TELEDECLARE))
            )
        return self.annotate(action=Case(*conditions, default=Value(Canteen.Actions.NOTHING)))


class CanteenManager(SoftDeletionManager):
    queryset_model = CanteenQuerySet


class Canteen(DirtyFieldsMixin, SoftDeletionModel):
    objects = CanteenManager.from_queryset(CanteenQuerySet)()
    all_objects = CanteenManager.from_queryset(CanteenQuerySet)(alive_only=False)

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
        GROUPE = "groupe", "Groupe"
        CENTRAL = "central", "Cuisine centrale"
        CENTRAL_SERVING = "central_serving", "Cuisine centrale et site"
        ON_SITE = "site", "Restaurant avec cuisine sur place"
        ON_SITE_CENTRAL = (
            "site_cooked_elsewhere",
            "Restaurant satellite",
        )

    class EconomicModel(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Privé"

    class PublicationStatus(models.TextChoices):
        DRAFT = "draft", "🔒 Non publié"
        PUBLISHED = "published", "✅ Publié"

    class Actions(models.TextChoices):
        ADD_SATELLITES = "10_add_satellites", "Ajouter des restaurants satellites"
        PREFILL_DIAGNOSTIC = "18_prefill_diagnostic", "Créer et pré-remplir le diagnostic"
        CREATE_DIAGNOSTIC = "20_create_diagnostic", "Créer le diagnostic"
        FILL_DIAGNOSTIC = "30_fill_diagnostic", "Compléter le diagnostic"
        FILL_CANTEEN_DATA = "35_fill_canteen_data", "Compléter les infos de la cantine"
        FILL_SATELLITE_CANTEEN_DATA = "36_fill_satellite_canteen_data", "Compléter les infos des cantines satellites"
        TELEDECLARE = "40_teledeclare", "Télédéclarer"
        DID_NOT_TELEDECLARE = "45_did_not_teledeclare", "Non télédéclaré"
        NOTHING_SATELLITE = "90_nothing_satellite", "En attente de la télédéclaration de votre groupe"
        NOTHING_SATELLITE_TELEDECLARED = (
            "91_nothing_satellite_teledeclared",
            "Rien à faire (télédéclaré par votre groupe)",
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

    GEO_FIELDS = [
        "city_insee_code",
        "city",
        "postal_code",
        "epci",
        "epci_lib",
        "pat_list",
        "pat_lib_list",
        "department",
        "department_lib",
        "region",
        "region_lib",
    ]
    # not all city_insee_code are linked to a PAT
    GEO_FIELDS_WITHOUT_PAT = [
        field_name for field_name in GEO_FIELDS if field_name not in ("pat_list", "pat_lib_list")
    ]

    TD_FIELDS = [
        "declaration_donnees_2021",
        "declaration_donnees_2022",
        "declaration_donnees_2023",
        "declaration_donnees_2024",
        "declaration_donnees_2025",
    ]

    MATOMO_FIELDS = [
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
    ]

    CREATION_META_FIELDS = [
        "creation_date",
        "modification_date",
        "creation_source",
        "import_source",
    ]

    import_source = models.TextField(null=True, blank=True, verbose_name="Source de l'import de la cantine")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    name = models.TextField(verbose_name="nom")

    siret = models.TextField(null=True, blank=True, validators=[utils_siret.validate_siret])
    siren_unite_legale = models.TextField(
        null=True, blank=True, verbose_name="siren de l'unité légale", validators=[utils_siret.validate_siren]
    )

    city_insee_code = models.TextField(
        null=True, blank=True, verbose_name="Code INSEE"
    )  # nécessaire pour remplir les autres champs geo
    city = models.TextField(null=True, blank=True, verbose_name="ville")
    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name="code postal")
    epci = models.CharField(null=True, blank=True, verbose_name="Code EPCI", validators=[utils_siret.validate_siren])
    epci_lib = models.TextField(null=True, blank=True, verbose_name="nom EPCI")
    pat_list = ArrayField(base_field=models.CharField(), blank=True, default=list, verbose_name="codes PAT")
    pat_lib_list = ArrayField(base_field=models.CharField(), blank=True, default=list, verbose_name="noms PAT")
    department = models.TextField(null=True, blank=True, choices=Department.choices, verbose_name="département")
    department_lib = models.TextField(null=True, blank=True, verbose_name="nom du département")
    region = models.TextField(null=True, blank=True, choices=Region.choices, verbose_name="région")
    region_lib = models.TextField(null=True, blank=True, verbose_name="nom de la région")

    sectors_m2m = models.ManyToManyField(SectorM2M, blank=True, verbose_name="secteurs d'activité")
    sector_list = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=Sector.choices),
        default=list,
        blank=True,
        verbose_name="secteurs d'activité",
    )
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

    groupe = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name="Groupe",
        on_delete=models.SET_NULL,
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
    economic_model = models.CharField(
        max_length=50,
        choices=EconomicModel.choices,
        null=True,
        blank=True,
        verbose_name="Modèle économique",
    )

    is_filled = models.BooleanField(default=False, verbose_name="cantine complète (champ calculé)")

    # TDs (rempli grâce à canteen_fill_declaration_donnees_year_field)
    declaration_donnees_2021 = models.BooleanField(default=False, verbose_name="a télédéclaré ses données de 2021")
    declaration_donnees_2022 = models.BooleanField(default=False, verbose_name="a télédéclaré ses données de 2022")
    declaration_donnees_2023 = models.BooleanField(default=False, verbose_name="a télédéclaré ses données de 2023")
    declaration_donnees_2024 = models.BooleanField(default=False, verbose_name="a télédéclaré ses données de 2024")
    declaration_donnees_2025 = models.BooleanField(default=False, verbose_name="a télédéclaré ses données de 2025")

    logo = models.ImageField(null=True, blank=True, verbose_name="Logo")

    # Publication things
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

    # Automatic tasks
    siret_inconnu = models.BooleanField(
        default=False, verbose_name="le siret de cette cantine est inconnu (obtenu via API Recherche Entreprises)"
    )
    siret_etat_administratif = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="état administratif du siret (obtenu via API Recherche Entreprises)",
    )
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

    creation_source = models.CharField(
        max_length=255,
        choices=CreationSource.choices,
        blank=True,
        null=True,
        verbose_name="Source de création de la cantine",
    )

    def normalize_fields(self):
        for field_name in ["siret", "siren_unite_legale", "epci", "central_producer_siret"]:
            setattr(self, field_name, utils_utils.normalize_string(getattr(self, field_name)))

    def optimize_logo(self):
        max_image_size = 1024
        if self.logo:
            self.logo = optimize_image(self.logo, self.logo.name, max_image_size)

    def reset_geo_fields_if_siret_changed(self):
        """
        Cases where we need to reset geo fields:
        - if siret has changed: reset all geo fields (including city_insee_code)
        """
        if self.id and self.is_dirty():
            if "siret" in self.get_dirty_fields():
                self.reset_geo_fields(with_city_insee_code=True, with_save=False)

    def set_is_filled(self):
        self.is_filled = self._is_filled()

    def clean(self, *args, **kwargs):
        validation_errors = utils_utils.merge_validation_errors(
            canteen_validators.validate_canteen_siret_or_siren_unite_legale(self),
            canteen_validators.validate_canteen_management_type_field(self),
            canteen_validators.validate_canteen_production_type_field(self),
            canteen_validators.validate_canteen_economic_model_field(self),
            canteen_validators.validate_canteen_meal_count_fields(self),
            canteen_validators.validate_canteen_sector_list_field(self),
            canteen_validators.validate_canteen_line_ministry_field(self),
            canteen_validators.validate_canteen_groupe_field(self),
            canteen_validators.validate_canteen_central_producer_siret_field(self),
        )
        if validation_errors:
            raise ValidationError(validation_errors)

    def save(self, skip_validations=False, **kwargs):
        """
        - cleanup some fields (siret, siren_unite_legale, epci, central_producer_siret, logo)
        - set region from department
        - full_clean(): run validations (with extra validations in clean())
            - this can be skipped with skip_validations=True (USE WITH CAUTION)
        """
        self.normalize_fields()
        self.optimize_logo()
        self.reset_geo_fields_if_siret_changed()
        if not skip_validations:
            self.full_clean()
        self.set_is_filled()
        super().save(**kwargs)
        # see also: post_save signal

    def delete(self, skip_validations=False, **kwargs):
        """
        Override the SoftDeletionModel delete method
        - add the skip_validations parameter to skip validations (USE WITH CAUTION)
        - if groupe: make sure no satellite cantines are linked to it
        """
        if self.is_groupe:
            satellites_count = self.satellites.count()
            if satellites_count > 0:
                raise ValidationError(
                    f"Impossible de supprimer ce groupe car il a encore {satellites_count} satellites(s) de rattaché(s)."
                )
        super().delete(skip_validations=skip_validations, **kwargs)

    @property
    def url_slug(self):
        return f"{self.id}--{quote(self.name)}"

    @property
    def url_path(self):
        return f"/nos-cantines/{self.url_slug}"

    @property
    def siret_or_siren_unite_legale(self) -> str:
        return self.siret or self.siren_unite_legale or ""

    @property
    def is_public(self) -> bool:
        return self.economic_model and self.economic_model == Canteen.EconomicModel.PUBLIC

    @property
    def is_groupe(self) -> bool:
        return self.production_type and self.production_type == Canteen.ProductionType.GROUPE

    @property
    def is_central(self) -> bool:
        return self.production_type and self.production_type in [
            Canteen.ProductionType.CENTRAL,
        ]

    @property
    def is_central_cuisine(self) -> bool:
        return self.production_type and self.production_type in [
            Canteen.ProductionType.CENTRAL,
            Canteen.ProductionType.CENTRAL_SERVING,
        ]

    @property
    def is_groupe_or_central_cuisine(self) -> bool:
        return self.is_groupe or self.is_central_cuisine

    @property
    def is_serving(self):
        return self.production_type and self.production_type in [
            Canteen.ProductionType.CENTRAL_SERVING,
            Canteen.ProductionType.ON_SITE,
            Canteen.ProductionType.ON_SITE_CENTRAL,
        ]

    @property
    def satellites(self):
        if self.is_groupe:
            return self.canteen_set.all()
        elif self.is_central_cuisine:
            if self.siret:
                return Canteen.objects.get_satellites_old(self.siret)
        return Canteen.objects.none()

    @property
    def satellites_count(self):
        return self.satellites.count()

    @property
    def satellites_missing_data_count(self):
        return self.satellites.has_missing_data().count()

    @property
    def satellites_already_teledeclared_count(self):
        if self.is_groupe:
            year = timezone.now().year - 1
            return (
                self.satellites.annotate_with_action_for_year(year)
                .filter(action__in=[Canteen.Actions.NOTHING_SATELLITE_TELEDECLARED, Canteen.Actions.NOTHING])
                .count()
            )

    @property
    def is_satellite(self) -> bool:
        return self.production_type and self.production_type == Canteen.ProductionType.ON_SITE_CENTRAL

    @property
    def central_kitchen(self):
        if self.groupe_id:
            return self.groupe

    @property
    def central_kitchen_diagnostics(self):
        if self.groupe_id:
            return self.groupe.diagnostics.filter(central_kitchen_diagnostic_mode__isnull=False)

    @property
    def sector_lib_list(self):
        from data.models.sector import get_sector_lib_list_from_sector_list

        return get_sector_lib_list_from_sector_list(self.sector_list)

    @property
    def category_lib_list_from_sector_list(self):
        from data.models.sector import get_category_lib_list_from_sector_list

        return get_category_lib_list_from_sector_list(self.sector_list)

    @property
    def is_spe(self) -> bool:
        return bool(self.line_ministry)

    @property
    def can_be_claimed(self):
        return not self.managers.exists()

    @property
    def has_missing_geo_data(self) -> bool:
        """
        returns True if at least one geo field is missing
        Note: not all city_insee_code belong to a PAT. So we don't check these fields.
        """
        for field_name in self.GEO_FIELDS_WITHOUT_PAT:
            if not getattr(self, field_name):
                return True
        return False

    def _is_filled(self) -> bool:
        # basic rules
        is_filled = (
            bool(self.name)
            and bool(self.daily_meal_count)
            and bool(self.yearly_meal_count)
            and bool(self.siret or self.siren_unite_legale)
            and bool(self.management_type)
            and bool(self.production_type)
        )
        # groupe-specific rules
        # - the check on satellites_count is only done in teledeclare()
        # serving-specific rules: basics
        if is_filled and self.is_serving:
            is_filled = (
                bool(self.city_insee_code)
                and bool(self.economic_model)
                and bool(self.sector_list)
                and len(self.sector_list) <= 3
            )
        # serving-specific rules: line_ministry
        if (
            is_filled
            and self.is_serving
            and self.is_public
            and set(self.sector_list).intersection(SECTOR_HAS_LINE_MINISTRY_LIST)
        ):
            is_filled = bool(self.line_ministry)
        return is_filled

    def has_diagnostic_for_year(self, year):
        has_diagnostic = self.diagnostics.filter(year=year).exists()
        has_central_kitchen_diagnostic = (
            self.central_kitchen_diagnostics and self.central_kitchen_diagnostics.filter(year=year).exists()
        )
        return has_diagnostic or has_central_kitchen_diagnostic

    def has_diagnostic_teledeclared_for_year(self, year):
        has_diagnostics_teledeclared = self.diagnostics.filter(year=year).teledeclared().exists()
        has_central_kitchen_diagnostic_teledeclared = (
            self.central_kitchen_diagnostics
            and self.central_kitchen_diagnostics.filter(year=year).teledeclared().exists()
        )
        return has_diagnostics_teledeclared or has_central_kitchen_diagnostic_teledeclared

    def get_declaration_donnees_year_display(self, year):
        from data.models.teledeclaration import Teledeclaration

        if getattr(self, f"declaration_donnees_{year}"):
            if self.teledeclaration_set.filter(
                year=year, status=Teledeclaration.TeledeclarationStatus.SUBMITTED
            ).exists():
                return "📩 Télédéclarée"
            else:
                return "📩 Télédéclarée (par CC)"
        return ""

    @property
    def publication_status_display_to_public(self):
        if self.is_groupe or self.line_ministry == Canteen.Ministries.ARMEE:
            return Canteen.PublicationStatus.DRAFT
        return Canteen.PublicationStatus.PUBLISHED

    def __str__(self):
        return f'Cantine "{self.name}"'

    def _get_region(self):
        return get_region_from_department(self.department)

    def reset_geo_fields(self, with_city_insee_code=False, with_save=True):
        """
        Helper to reset geo fields
        The geolocation bot will then fill them again (using the siret) (post_save signal)
        """
        if with_city_insee_code:
            self.city_insee_code = None
        self.city = None
        self.postal_code = None
        self.epci = None
        self.epci_lib = None
        self.pat_list = []
        self.pat_lib_list = []
        self.department = None
        self.department_lib = None
        self.region = None
        self.region_lib = None
        self.siret_inconnu = False
        self.siret_etat_administratif = None
        self.geolocation_bot_attempts = 0
        if with_save:
            self.save(skip_validations=True)
            update_change_reason(self, "Reset geo fields")

    @cached_property
    def appro_diagnostics(self):
        diag_ids = list_properties(self.diagnostics, "id")

        if self.central_kitchen_diagnostics:
            # for any given year, could have own diag or CC diag
            # CC diag always takes precedent TODO: do we consistently assume this?
            # if don't have own diag, include CC diag in set
            cc_diag_years = list_properties(self.central_kitchen_diagnostics, "year")
            own_diagnostics = self.diagnostics.exclude(year__in=cc_diag_years)

            diag_ids = list_properties(self.central_kitchen_diagnostics, "id")
            diag_ids += list_properties(own_diagnostics, "id")

        from data.models import Diagnostic

        this_year = timezone.now().date().year
        return Diagnostic.objects.filter(id__in=diag_ids, year__lt=this_year).order_by("-year")

    @cached_property
    def service_diagnostics(self):
        diag_ids = list_properties(self.diagnostics, "id")

        if self.central_kitchen_diagnostics:
            cc_service_diagnostics = self.central_kitchen_diagnostics.filter(central_kitchen_diagnostic_mode="ALL")
            # for any given year, could have own diag or CC diag
            # CC diag always takes precedent, if ALL TODO: do we consistently assume this?
            # if don't have own diag, include CC diag in set
            cc_diag_years = list_properties(cc_service_diagnostics, "year")
            own_diagnostics = self.diagnostics.exclude(year__in=cc_diag_years)

            diag_ids = list_properties(cc_service_diagnostics, "id")
            diag_ids += list_properties(own_diagnostics, "id")

        from data.models import Diagnostic

        this_year = timezone.now().date().year
        return Diagnostic.objects.filter(id__in=diag_ids, year__lt=this_year).order_by("-year")

    @cached_property
    def published_appro_diagnostics(self):
        diagnostics_to_redact_id_list = []
        for year in self.redacted_appro_years:
            diag = self.appro_diagnostics.filter(year=year).first()
            if diag and not diag.is_teledeclared:
                diagnostics_to_redact_id_list.append(diag.id)
        return self.appro_diagnostics.exclude(id__in=diagnostics_to_redact_id_list)

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
    def in_administration(self):
        return set(self.sector_list).intersection(ADMINISTRATION_SECTOR_LIST)

    @property
    def lead_image(self):
        return self.images.first()


@receiver(post_save, sender=Canteen)
def fill_geo_fields_from_siret(sender, instance, created, **kwargs):
    """
    On canteen creation, we need to fill its geo fields

    Notes:
    - if city_insee_code is (already) set, we don't override it
    - GROUPE canteens don't have siret, so it won't be triggered for them
    TODO: canteen edit (when the canteen changes siret)
    """
    from macantine import tasks

    if instance.siret:
        tasks.update_canteen_geo_fields_from_siret(instance)


class CanteenImage(models.Model):
    canteen = models.ForeignKey(Canteen, related_name="images", on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    alt_text = models.TextField(
        null=True,
        blank=True,
        verbose_name="texte alternatif pour les utilisateurs qui voient pas l'image",
    )

    def save(self, **kwargs):
        self.image = optimize_image(self.image, self.image.name)
        super().save(**kwargs)
