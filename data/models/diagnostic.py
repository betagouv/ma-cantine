import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Case, DecimalField, F, Func, IntegerField, Q, Sum, Value, When
from django.db.models.expressions import RawSQL
from django.db.models.functions import Coalesce
from django.utils import timezone
from simple_history.models import HistoricalRecords

from common.utils import utils as utils_utils
from data.fields import ChoiceArrayField
from data.models import Canteen, AuthenticationMethodHistoricalRecords
from data.models.creation_source import CreationSource
from data.models.diagnostic_volet_approvisionnement import DiagnosticVoletApprovisionnementMixin
from data.models.diagnostic_volet_gaspillage import DiagnosticVoletGaspillageMixin
from data.models.diagnostic_volet_diversification import DiagnosticVoletDiversificationMixin
from data.models.diagnostic_volet_plastique import DiagnosticVoletPlastiqueMixin
from data.models.diagnostic_volet_information import DiagnosticVoletInformationMixin
from data.utils import (
    CustomJSONEncoder,
    compute_percentage,
    has_any_value_filled,
    has_arrayfield_missing_query,
    make_optional_positive_decimal_field,
    sum_int_with_potential_null,
    to_decimal,
)
from data.validators import diagnostic as diagnostic_validators
from data.validators import diagnostic_teledeclaration as diagnostic_teledeclaration_validators
from data.models.diagnostic_teledeclaration_dates import (
    CAMPAIGN_DATES,
    is_in_correction,
)
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_required,
)
from data.models.diagnostic_teledeclaration_field_groups import (
    TELEDECLARATION_FIELD_GROUPS,
    get_teledeclaration_field_groups,
)
from data.models.diagnostic_teledeclaration_egalim_objectives import (
    EGALIM_REGION_GROUPS,
    get_egalim_objectives,
    objectifs_egalim_atteints,
)
from macantine.utils import (
    TELEDECLARATION_CURRENT_VERSION,
    YEARS_WITH_1TD1SITE,
)


def in_teledeclaration_campaign_query(year):
    year = int(year)
    return Q(
        teledeclaration_date__range=(
            CAMPAIGN_DATES[year]["teledeclaration_start_date"],
            CAMPAIGN_DATES[year]["teledeclaration_end_date"],
        )
    )


def in_correction_campaign_query(year):
    year = int(year)
    return Q(
        teledeclaration_date__range=(
            CAMPAIGN_DATES[year]["correction_start_date"],
            CAMPAIGN_DATES[year]["correction_end_date"],
        )
    )


def valeur_totale_is_filled_query():
    return Q(valeur_totale__isnull=False)


def valeur_bio_agg_is_filled_query():
    return Q(valeur_bio_agg__isnull=False)


def is_filled_query():
    return Q(is_filled=True)


def teledeclaration_mode_satellite_without_appro_query():
    return Q(teledeclaration_mode=Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO)


def canteen_deleted_query():
    return Q(canteen_id__isnull=True)


def canteen_soft_deleted_during_campaign_query(year):
    year = int(year)
    return Q(
        canteen__deletion_date__range=(
            CAMPAIGN_DATES[year]["teledeclaration_start_date"],
            CAMPAIGN_DATES[year]["teledeclaration_end_date"],
        )
    )


def canteen_has_siret_or_siren_unite_legale_query():
    return Q(
        ~Q(canteen_snapshot__siret=None) & ~Q(canteen_snapshot__siret="")
        | ~Q(canteen_snapshot__siren_unite_legale=None) & ~Q(canteen_snapshot__siren_unite_legale="")
    )


def aberrant_values_query():
    """
    Ici nous filtrons les TDs dont les déclarations paraissent aberrantes et sont impactantes :
    - Coût denrées existe et > 20 euros ET valeur d'achat alimentaires > 1 million d'euros
    Dans le cas particulier où le nombre de repas annuel n'est pas renseigné,
    nous laissons la TD même si la valeur alimentaire est > 1 million d'euros)
    - En 2025, coût denrées existe et < 0.1 euros
    """
    return Q(cout_repas__isnull=False, cout_repas__gt=20, valeur_totale__gt=1000000) | Q(year=2025, cout_repas__lt=0.1)


def incoherent_values_query():
    """
    Ici nous filtrons les TDs dont les déclarations paraissent incohérentes et sont impactantes :
    - Durant la campagne 2023, nous avons identifié deux TDs dont les valeurs étaient incohérentes.
    """
    return Q(year=2022, teledeclaration_id__in=[9656, 8037])


def circuit_court_sup_france_query():
    """
    TDs COMPLETE 2025 avec une incohérence sur "origine France dont circuit_court"
    - En 2025, circuit-court faisait partie d'origine France, mais à parfois été mal télédéclaré
    - A partir de 2026, circuit-court a été sorti d'origine France

    Note: requires with_label_sum("circuit_court") and with_label_sum("france") annotations
    """
    return Q(year=2025, diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, circuit_court_sum__gt=F("france_sum"))


def local_sup_france_query():
    """
    TDs COMPLETE 2025 avec une incohérence sur "origine France dont local"
    - En 2025, local faisait partie d'origine France, mais à parfois été mal télédéclaré
    - A partir de 2026, local a été sorti d'origine France

    Note: requires with_label_sum("local") and with_label_sum("france") annotations
    """
    return Q(year=2025, diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, local_sum__gt=F("france_sum"))


def commerce_equitable_sup_bio_query():
    """
    TDs SIMPLE & COMPLETE 2025 avec une incohérence sur "bio dont commerce équitable"

    Note: see validators/diagnostics.py#validate_valeur_bio
    Note: requires with_label_sum("bio_dont_commerce_equitable") and with_label_sum("bio") annotations
    """
    return Q(
        year=2025,
        diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        valeur_bio_dont_commerce_equitable__gt=F("valeur_bio"),
    ) | Q(
        year=2025, diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, bio_dont_commerce_equitable_sum__gt=F("bio_sum")
    )


def has_invalid_reason_list_query():
    return ~has_arrayfield_missing_query("invalid_reason_list")


def is_teledeclared_query():
    return Q(status=Diagnostic.DiagnosticStatus.SUBMITTED)


class DiagnosticQuerySet(models.QuerySet):
    def filled(self):
        return self.filter(is_filled_query())

    def not_teledeclared(self):
        return self.exclude(is_teledeclared_query())

    def teledeclared(self):
        return self.filter(is_teledeclared_query())

    def has_invalid_reason(self):
        return self.filter(has_invalid_reason_list_query())

    def in_year(self, year):
        return self.filter(year=int(year))

    def in_campaign(self, year):
        year = int(year)
        if year in CAMPAIGN_DATES.keys():
            if "correction_start_date" in CAMPAIGN_DATES[year].keys():
                return self.filter(in_teledeclaration_campaign_query(year) | in_correction_campaign_query(year))
            else:
                return self.filter(in_teledeclaration_campaign_query(year))
        else:
            return self.none()

    def teledeclared_for_year(self, year):
        return self.teledeclared().in_year(year).in_campaign(year)

    def teledeclared_site_for_year(self, year):
        """
        Only return site TDs
        - before 2025: exclude central & central servings
        - 2025: exclude groupes
        """
        return (
            self.teledeclared_for_year(year)
            .annotate(canteen_snapshot_production_type=F("canteen_snapshot__production_type"))
            .exclude(
                canteen_snapshot_production_type__in=[
                    Canteen.ProductionType.GROUPE,
                    Canteen.ProductionType.CENTRAL,
                    Canteen.ProductionType.CENTRAL_SERVING,
                ]
            )
        )

    def with_label_sum(self, label: str):
        """
        Sum all appro fields of a given label.

        Note: see also label_sum method
        Note: the families summed depend on the diagnostic's own year (see
        diagnostic_teledeclaration_field_groups.py), so we build one sum expression per distinct
        family list found in the registry and pick the right one per row via Case/When — this
        works correctly on a queryset spanning multiple years.
        """
        families_by_years = {}
        for year in TELEDECLARATION_FIELD_GROUPS:
            families = tuple(get_teledeclaration_field_groups(year, "APPRO_FAMILIES"))
            families_by_years.setdefault(families, []).append(year)

        cases = [
            When(
                year__in=years,
                then=reduce(
                    operator.add,
                    (
                        Coalesce(F(f"valeur_{family}_{label}"), Value(0), output_field=DecimalField())
                        for family in families
                    ),
                ),
            )
            for families, years in families_by_years.items()
        ]
        return self.annotate(**{f"{label}_sum": Case(*cases, output_field=DecimalField())})

    def with_family_sum(self, family: str):
        """
        Sum all appro fields of a given family.

        Note: see also family_sum method
        NOTE: APPRO_LABELS does not include APPRO_LABELS_ORIGINE & circuit_court & local
        Note: the labels summed depend on the diagnostic's own year (see
        diagnostic_teledeclaration_field_groups.py), so we build one sum expression per distinct
        label list found in the registry and pick the right one per row via Case/When — this
        works correctly on a queryset spanning multiple years.
        """
        labels_by_years = {}
        for year in TELEDECLARATION_FIELD_GROUPS:
            labels = tuple(get_teledeclaration_field_groups(year, "APPRO_LABELS"))
            labels_by_years.setdefault(labels, []).append(year)

        cases = [
            When(
                year__in=years,
                then=reduce(
                    operator.add,
                    (
                        Coalesce(F(f"valeur_{family}_{label}"), Value(0), output_field=DecimalField())
                        for label in labels
                    ),
                ),
            )
            for labels, years in labels_by_years.items()
        ]
        return self.annotate(**{f"{family}_sum": Case(*cases, output_field=DecimalField())})

    def with_satellites_snapshot_stats(self):
        return self.annotate(
            satellites_snapshot_count_annotated=Func(
                "satellites_snapshot", function="jsonb_array_length", output_field=IntegerField()
            )
        ).annotate(
            satellites_snapshot_yearly_meal_count_sum=RawSQL(
                sql="(SELECT SUM((elem->>'yearly_meal_count')::integer) FROM jsonb_array_elements(satellites_snapshot) AS elem)",
                params=[],
                output_field=IntegerField(),
            )
        )

    def canteen_for_stat(self, year):
        return (
            self.select_related("canteen")
            .exclude(canteen_deleted_query())
            .exclude(canteen_soft_deleted_during_campaign_query(year))  # Chaîne de traitement n°6
            .filter(canteen_has_siret_or_siren_unite_legale_query())  # Chaîne de traitement n°7
        )

    def valid_td_by_year(self, year):
        year = int(year)
        if year in CAMPAIGN_DATES.keys():
            return (
                self.teledeclared_for_year(year)
                .exclude(generated_from_groupe_diagnostic=True)  # just to be sure, in case all_objects is used
                .exclude(teledeclaration_mode_satellite_without_appro_query())
                .filter(valeur_bio_agg_is_filled_query())  # Chaîne de traitement n°5
                .canteen_for_stat(year)  # Chaîne de traitement n°6 & n°7
                .exclude(aberrant_values_query())  # Chaîne de traitement n°8
                .exclude(incoherent_values_query())  # Chaîne de traitement n°8
            )
        else:
            return self.none()

    def valid_td_site_by_year(self, year):
        year = int(year)
        if year in CAMPAIGN_DATES.keys():
            if year in YEARS_WITH_1TD1SITE:
                return self.teledeclared_site_for_year(year).exclude(has_invalid_reason_list_query())
            else:
                return self.valid_td_by_year(year)
        else:
            return self.none()

    def valid_td_all_years(self, years: list):
        results = self.none()
        for year in years:
            results = results | self.valid_td_by_year(year)
        return results.select_related("canteen")

    def valid_td_site_all_years(self, years: list):
        results = self.none()
        for year in years:
            results = results | self.valid_td_site_by_year(year)
        return results.select_related("canteen")

    def publicly_visible(self):
        return (
            self.select_related("canteen")
            .exclude(canteen__line_ministry=Canteen.Ministries.ARMEE)
            .exclude(canteen_snapshot__line_ministry=Canteen.Ministries.ARMEE)
        )

    def with_appro_percent_stats(self):
        """
        Note: we use Sum/default instead of F to better manage None values.
        """
        return self.annotate(valeur_totale_sum=Sum("valeur_totale")).annotate(
            bio_percent=100 * Sum("valeur_bio_agg", default=0) / F("valeur_totale_sum"),
            egalim_percent=100 * F("valeur_egalim_agg") / F("valeur_totale_sum"),
        )

    def teledeclaration_objectifs_egalim_atteints(self):
        """
        The field 'objectifs_egalim_atteints' is only filled for teledeclared diagnostics.
        """
        return self.filter(objectifs_egalim_atteints=True)

    def egalim_objectives_reached(self, year):
        # TODO: filter on canteen_snapshot__region instead
        egalim_objectives_appro = get_egalim_objectives(year, "APPRO")
        return self.select_related("canteen").filter(
            Q(
                bio_percent__gte=egalim_objectives_appro["hexagone"]["bio_percent"],
                egalim_percent__gte=egalim_objectives_appro["hexagone"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_REGION_GROUPS["groupe_1"],
                bio_percent__gte=egalim_objectives_appro["groupe_1"]["bio_percent"],
                egalim_percent__gte=egalim_objectives_appro["groupe_1"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_REGION_GROUPS["groupe_2"],
                bio_percent__gte=egalim_objectives_appro["groupe_2"]["bio_percent"],
                egalim_percent__gte=egalim_objectives_appro["groupe_2"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_REGION_GROUPS["groupe_3"],
                bio_percent__gte=egalim_objectives_appro["groupe_3"]["bio_percent"],
                egalim_percent__gte=egalim_objectives_appro["groupe_3"]["egalim_percent"],
            )
        )


class DiagnosticManager(models.Manager):
    queryset_model = DiagnosticQuerySet

    def __init__(self, *args, **kwargs):
        self.exclude_generated = kwargs.pop("exclude_generated", False)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.exclude_generated:
            return self.queryset_model(self.model).exclude(generated_from_groupe_diagnostic=True)
        return self.queryset_model(self.model)


class Diagnostic(
    DiagnosticVoletApprovisionnementMixin,
    DiagnosticVoletGaspillageMixin,
    DiagnosticVoletDiversificationMixin,
    DiagnosticVoletPlastiqueMixin,
    DiagnosticVoletInformationMixin,
    models.Model,
):
    class DiagnosticStatus(models.TextChoices):
        DRAFT = "DRAFT", "Brouillon"
        CORRECTION = "CORRECTION", "En correction"
        SUBMITTED = "SUBMITTED", "Télédéclaré"

    # NB: if the label of the choice changes, double check that the teledeclaration PDF
    # doesn't need an update as well, since the logic in the templates is based on the label
    class DiagnosticType(models.TextChoices):
        SIMPLE = "SIMPLE", "Télédeclaration simple"
        COMPLETE = "COMPLETE", "Télédeclaration détaillée"

    class CentralKitchenDiagnosticMode(models.TextChoices):
        APPRO = (
            "APPRO",
            "Ce diagnostic concerne les données d'approvisionnement de tous les restaurants satellites",
        )
        ALL = "ALL", "Ce diagnostic concerne toutes les données des restaurants satellites"

    class TeledeclarationMode(models.TextChoices):
        SATELLITE_WITHOUT_APPRO = (
            "SATELLITE_WITHOUT_APPRO",
            "Restaurant satellite dont les données d'appro sont déclarées par la cuisine centrale",
        )
        CENTRAL_APPRO = (
            "CENTRAL_APPRO",
            "Cuisine centrale déclarant les données d'appro pour ses restaurants satellites",
        )
        CENTRAL_ALL = (
            "CENTRAL_ALL",
            "Cuisine centrale déclarant toutes les données EGalim pour ses restaurants satellites",
        )
        SITE = "SITE", "Cantine déclarant ses propres données"

    class InvalidReason(models.TextChoices):
        CANTINE_SUPPRIMEE = "CANTINE_SUPPRIMEE", "Cantine supprimée"
        CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE = (
            "CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE",
            "Cantine soft supprimée pendant la campagne",
        )
        CANTINE_SANS_SIRET_OU_SIREN = "CANTINE_SANS_SIRET_OU_SIREN", "Cantine sans siret ou siren"
        TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO = (
            "TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO",
            "Télédeclaration mode satellite without appro",
        )
        VALEUR_TOTALE_VIDE = "VALEUR_TOTALE_VIDE", "Valeur totale des achats vide"
        VALEUR_BIO_AGG_VIDE = "VALEUR_BIO_AGG_VIDE", "Valeur totale des achats bio vide"
        VALEURS_ABERRANTES = "VALEURS_ABERRANTES", "Valeurs aberrantes"
        VALEURS_INCOHERENTES = "VALEURS_INCOHERENTES", "Valeurs incohérentes"
        DOUBLON_1TD1SITE = "DOUBLON_1TD1SITE", "Doublon 1TD1Site"

    class WarningReason(models.TextChoices):
        CIRCUIT_COURT_SUP_FRANCE = "CIRCUIT_COURT_SUP_FRANCE", "Origine France (dont circuit-court) > Origine France"
        LOCAL_SUP_FRANCE = "LOCAL_SUP_FRANCE", "Origine France (dont local) > Origine France"
        COMMERCE_EQUITABLE_SUP_BIO = "COMMERCE_EQUITABLE_SUP_BIO", "Bio dont commerce équitable > Bio"

    APPRO_1TD1SITE_FIELDS = (
        DiagnosticVoletApprovisionnementMixin.SIMPLE_APPRO_FIELDS
        + DiagnosticVoletApprovisionnementMixin.COMPLETE_APPRO_FIELDS
        + DiagnosticVoletApprovisionnementMixin.APPRO_AGGREGATED_FIELDS
    )

    NON_APPRO_FIELDS = (
        DiagnosticVoletGaspillageMixin.WASTE_FIELDS
        + DiagnosticVoletDiversificationMixin.DIVERSIFICATION_FIELDS
        + DiagnosticVoletPlastiqueMixin.PLASTIC_FIELDS
        + DiagnosticVoletInformationMixin.INFO_FIELDS
    )

    OTHER_COMPUTED_FIELDS = [
        "cout_repas",
        "is_filled",
    ]

    CANTEEN_FIELDS = [
        # new in 2026
        "nombre_repas_an",
    ]

    META_FIELDS = [
        "id",
        "canteen_id",
        "year",
        "diagnostic_type",
        "central_kitchen_diagnostic_mode",
        "is_teledeclared",
        "is_filled",
    ]

    CREATION_META_FIELDS = [
        "creation_date",
        "modification_date",
        "creation_user",
        "creation_source",
        "creation_source_api_oauth2_application",
    ]

    MATOMO_FIELDS = [
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
    ]

    TUNNEL_PROGRESS_FIELDS = [
        "tunnel_appro",
        "tunnel_waste",
        "tunnel_diversification",
        "tunnel_plastic",
        "tunnel_info",
    ]

    TELEDECLARATION_FIELDS = [
        "teledeclaration_date",
        "teledeclaration_mode",
        "teledeclaration_version",
        "teledeclaration_id",
    ]
    TELEDECLARATION_SNAPSHOT_FIELDS = [
        "canteen_snapshot",
        "satellites_snapshot",
        "groupe_snapshot",
        "applicant_snapshot",
    ]
    TELEDECLARATION_1TD1SITE_FIELDS = [
        "generated_from_groupe_diagnostic",
        "groupe_snapshot",
    ]
    TELEDECLARATION_DATA_QUALITY_FIELDS = [
        "invalid_reason_list",
        "warning_reason_list",
    ]

    APPRO_PERCENTAGE_PROPERTY_FIELDS = [
        "percentage_valeur_totale",
        "percentage_valeur_bio",
        "percentage_valeur_siqo",
        "percentage_valeur_externalites_performance",
        "percentage_valeur_egalim_autres",
        "percentage_valeur_viandes_volailles_egalim",
        "percentage_valeur_viandes_volailles_france",
        "percentage_valeur_produits_de_la_mer_egalim",
        "percentage_valeur_produits_de_la_mer_france",
    ]

    canteen = models.ForeignKey(
        Canteen, on_delete=models.SET_NULL, null=True, related_name="diagnostics", verbose_name="cantine"
    )

    year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="année",
    )

    status = models.CharField(
        max_length=255,
        choices=DiagnosticStatus.choices,
        default=DiagnosticStatus.DRAFT,
        verbose_name="status",
    )

    diagnostic_type = models.CharField(
        max_length=255,
        choices=DiagnosticType.choices,
        blank=True,
        null=True,
        verbose_name="Type de diagnostic (simplifié, détaillé)",
    )

    generated_from_purchases = models.BooleanField(
        verbose_name="A été automatiquement généré depuis les achats",
        default=False,
    )

    # Relevant only for central cuisines
    central_kitchen_diagnostic_mode = models.CharField(
        max_length=255,
        choices=CentralKitchenDiagnosticMode.choices,
        blank=True,
        null=True,
        verbose_name="Quelles données sont déclarées par ce groupe ? (seulement pertinent pour les groupes)",
    )

    # progress fields
    # NB None = tunnel has not been started; "complet" = tunnel has finished
    # all other values are defined by the front end
    tunnel_appro = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel appro",
    )
    tunnel_waste = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel anti-gaspi",
    )
    tunnel_diversification = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel diversification",
    )
    tunnel_plastic = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel anti-plastique",
    )
    tunnel_info = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel information convives",
    )

    # Campaign tracking
    creation_mtm_source = models.TextField(
        null=True,
        blank=True,
        verbose_name="mtm_source du lien tracké lors de la création",
    )
    creation_mtm_campaign = models.TextField(
        null=True,
        blank=True,
        verbose_name="mtm_campaign du lien tracké lors de la création",
    )
    creation_mtm_medium = models.TextField(
        null=True,
        blank=True,
        verbose_name="mtm_medium du lien tracké lors de la création",
    )

    # Télédéclaration
    teledeclaration_date = models.DateTimeField(
        verbose_name="date de télédéclaration",
        blank=True,
        null=True,
    )
    # a TD can use SATELLITE_WITHOUT_APPRO mode, as well as have some appro data of its own if,
    # for example, the manager of the satellite canteen started completing a diagnostic and then the
    # central kitchen decided to declare for its satellites.
    # We are leaving it up to the team to interpret the data in this case.
    teledeclaration_mode = models.CharField(
        verbose_name="mode de télédéclaration",
        max_length=255,
        choices=TeledeclarationMode.choices,
        null=True,
        blank=True,
    )
    teledeclaration_version = models.IntegerField(
        verbose_name="version de la télédéclaration",
        blank=True,
        null=True,
    )
    teledeclaration_id = models.IntegerField(
        verbose_name="ancien identifiant de la télédéclaration (concerne la période 2021-2024)",
        blank=True,
        null=True,
    )
    applicant = models.ForeignKey(
        get_user_model(),
        related_name="diagnostics_teledeclared",
        verbose_name="déclarant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    canteen_snapshot = models.JSONField(
        verbose_name="cantine (copie au moment de la télédéclaration)",
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
    )
    satellites_snapshot = models.JSONField(
        verbose_name="satellites (copie au moment de la télédéclaration) (seulement pertinent pour les groupes)",
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
    )
    applicant_snapshot = models.JSONField(
        verbose_name="déclarant (copie au moment de la télédéclaration)",
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
    )

    # 1TD1Site
    generated_from_groupe_diagnostic = models.BooleanField(
        verbose_name="A été automatiquement généré depuis le bilan du groupe (seulement pertinent pour les satellites)",
        default=False,
    )
    groupe_snapshot = models.JSONField(
        verbose_name="groupe (copie lors de la génération depuis le bilan du groupe) (seulement pertinent pour les satellites)",
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
    )

    cout_repas = make_optional_positive_decimal_field(
        verbose_name="coût repas (champ calculé)",
        help_text="le coût repas est calculé en divisant la valeur totale annuelle par le nombre de repas annuels de la cantine",
    )

    is_filled = models.BooleanField(default=False, verbose_name="bilan complété ? (champ calculé)")

    # Data quality
    invalid_reason_list = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=InvalidReason.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="bilan ignoré dans les stats (raisons)",
    )
    warning_reason_list = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=WarningReason.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="bilan avec des problèmes de données (raisons)",
    )

    creation_user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="diagnostics_created",
        verbose_name="utilisateur qui a créé le diagnostic",
    )
    creation_source = models.CharField(
        max_length=255,
        choices=CreationSource.choices,
        blank=True,
        null=True,
        verbose_name="Source de création du diagnostic",
    )
    creation_source_api_oauth2_application = models.ForeignKey(
        settings.OAUTH2_PROVIDER_APPLICATION_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diagnostics_created",
        verbose_name="app OAuth2 (API) qui a créé le diagnostic",
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(
        bases=[AuthenticationMethodHistoricalRecords], excluded_fields=TELEDECLARATION_SNAPSHOT_FIELDS
    )

    objects = DiagnosticManager.from_queryset(DiagnosticQuerySet)(exclude_generated=True)
    all_objects = DiagnosticManager.from_queryset(DiagnosticQuerySet)()

    class Meta:
        verbose_name = "diagnostic"
        verbose_name_plural = "diagnostics"
        constraints = [
            models.UniqueConstraint(
                fields=["canteen", "year", "generated_from_groupe_diagnostic"], name="annual_diagnostic"
            ),
        ]

    def __str__(self):
        return f"Diagnostic pour {self.canteen.name} ({self.year})"

    def clean(self):
        validation_errors = utils_utils.merge_validation_errors(
            diagnostic_validators.validate_year(self),
            diagnostic_validators.validate_year_and_can_edit(self),
            diagnostic_validators.validate_canteen_fields_required(self),
        )
        # satellites whose groupe handles appro centrally don't declare their own diagnostic_type/appro fields
        if not self._should_use_central_kitchen_appro():
            validation_errors = utils_utils.merge_validation_errors(
                validation_errors,
                diagnostic_validators.validate_diagnostic_type(self),
                diagnostic_validators.validate_appro_fields_required(self),
                diagnostic_validators.validate_valeur_totale(self),
                diagnostic_validators.validate_valeur_famille(self),
                diagnostic_validators.validate_valeur_famille_bio(self),
                diagnostic_validators.validate_valeur_label(self),
                diagnostic_validators.validate_viandes_volailles_total(self),
                diagnostic_validators.validate_produits_de_la_mer_total(self),
                diagnostic_validators.validate_viandes_volailles_produits_de_la_mer_egalim(self),
                diagnostic_validators.validate_definition_local(self),
            )
        if validation_errors:
            raise ValidationError(validation_errors)

        return super().clean()

    def save(self, **kwargs):
        # NOTE: full_clean() is not called in save() because we need to manage incomplete diagnostics (tunnel)
        validation_errors = utils_utils.merge_validation_errors(diagnostic_validators.validate_year(self))
        if not validation_errors:
            # these methods only work if there is a valid year
            if self.diagnostic_type:
                if self.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
                    self.populate_simplified_diagnostic_values()
                if int(self.year) >= 2026:
                    # since 2026, once the diagnostic_type is known, default any still-empty required field to 0
                    self.populate_required_fields_with_zero()
            self.populate_aggregated_values()
            self.populate_stats_values()
            self.populate_cout_repas()
        self.set_is_filled()
        return super().save(**kwargs)

    def set_is_filled(self):
        self.is_filled = self._is_filled()

    def populate_required_fields_with_zero(self):
        """
        Default any still-empty required appro field (for this diagnostic's year & diagnostic_type) to 0.
        NOTE: valeur_totale is excluded, it must be > 0 (see validate_valeur_totale)
        NOTE: nombre_repas_an is excluded
        """
        if not (self.year and self.diagnostic_type):
            return
        required_fields = get_teledeclaration_fields_required(self.year, "APPROVISIONNEMENT", self.diagnostic_type)
        excluded_fields = ["valeur_totale", "nombre_repas_an"]
        for field_name in required_fields:
            if field_name not in excluded_fields and getattr(self, field_name) is None:
                setattr(self, field_name, 0)

    def populate_simplified_diagnostic_values(self):
        # NOTE: SIMPLIFIED_DIAGNOSTIC_FIELDS
        self.valeur_bio = self.label_group_sum("bio")
        self.valeur_bio_dont_commerce_equitable = self.label_sum("bio_dont_commerce_equitable")
        self.valeur_siqo = self.label_group_sum("siqo")
        self.valeur_externalites_performance = self.label_group_sum("externalites_performance")
        self.valeur_egalim_autres = self.label_group_sum("egalim_autres")
        self.valeur_egalim_autres_dont_commerce_equitable = self.label_sum("commerce_equitable")

        total_meat_egalim = total_fish_egalim = 0
        for label in get_teledeclaration_field_groups(self.year, "APPRO_LABELS_EGALIM"):
            family = "viandes_volailles"
            # need to do or 0 and not give a default value because the value can be explicitly set to None
            total_meat_egalim = total_meat_egalim + (getattr(self, f"valeur_{family}_{label}") or 0)

            family = "produits_de_la_mer"
            total_fish_egalim = total_fish_egalim + (getattr(self, f"valeur_{family}_{label}") or 0)

        # NOTE: stop populating france from ["france", "circuit_court", "local"]
        # for label in ["france", "circuit_court", "local"]:
        #     family = "viandes_volailles"
        #     total_meat_france = total_meat_france + (getattr(self, f"valeur_{family}_{label}") or 0)

        self.valeur_viandes_volailles_egalim = total_meat_egalim
        # self.valeur_viandes_volailles_france = total_meat_france
        self.valeur_produits_de_la_mer_egalim = total_fish_egalim

    def populate_aggregated_values(self):
        # NOTE: AGGREGATED_DIAGNOSTIC_FIELDS
        self.valeur_bio_agg = self.label_group_sum("bio")
        self.valeur_siqo_agg = self.label_group_sum("siqo")
        self.valeur_externalites_performance_agg = self.label_group_sum("externalites_performance")
        self.valeur_egalim_autres_agg = self.label_group_sum("egalim_autres")
        # group_group
        self.valeur_egalim_hors_bio_agg = self.label_group_group_sum("egalim_hors_bio")
        self.valeur_egalim_agg = self.label_group_group_sum("egalim")

    def populate_stats_values(self):
        # NOTE: APPRO_STATS_FIELDS
        self.pourcentage_bio = compute_percentage(self.valeur_bio_agg, self.valeur_totale)
        self.pourcentage_siqo = compute_percentage(self.valeur_siqo_agg, self.valeur_totale)
        self.pourcentage_externalites_performance = compute_percentage(
            self.valeur_externalites_performance_agg, self.valeur_totale
        )
        self.pourcentage_egalim_autres = compute_percentage(self.valeur_egalim_autres_agg, self.valeur_totale)
        self.pourcentage_egalim_hors_bio = compute_percentage(self.valeur_egalim_hors_bio_agg, self.valeur_totale)
        self.pourcentage_egalim = compute_percentage(self.valeur_egalim_agg, self.valeur_totale)
        self.pourcentage_viandes_volailles_egalim = compute_percentage(
            self.valeur_viandes_volailles_egalim, self.valeur_viandes_volailles
        )
        self.pourcentage_produits_de_la_mer_egalim = compute_percentage(
            self.valeur_produits_de_la_mer_egalim, self.valeur_produits_de_la_mer
        )
        # keep None (not 0) if neither viandes_volailles nor produits_de_la_mer are filled
        valeur_viandes_volailles_produits_de_la_mer = (
            None
            if self.valeur_viandes_volailles is None and self.valeur_produits_de_la_mer is None
            else sum_int_with_potential_null([self.valeur_viandes_volailles, self.valeur_produits_de_la_mer])
        )
        self.pourcentage_viandes_volailles_produits_de_la_mer_egalim = compute_percentage(
            sum_int_with_potential_null([self.valeur_viandes_volailles_egalim, self.valeur_produits_de_la_mer_egalim]),
            valeur_viandes_volailles_produits_de_la_mer,
        )
        self.pourcentage_europe = compute_percentage(self.valeur_europe, self.valeur_totale)
        self.pourcentage_france = compute_percentage(self.valeur_france, self.valeur_totale)
        self.pourcentage_circuit_court = compute_percentage(self.valeur_circuit_court, self.valeur_totale)
        self.pourcentage_local = compute_percentage(self.valeur_local, self.valeur_totale)
        # per family & origine/circuit_court/local: relative to the family total
        for family_field in Diagnostic.APPRO_FAMILY_FIELDS:
            family = family_field.removeprefix("valeur_")
            for label in ["europe", "france", "circuit_court", "local"]:
                setattr(
                    self,
                    f"pourcentage_{family}_{label}",
                    compute_percentage(getattr(self, f"valeur_{family}_{label}"), getattr(self, family_field)),
                )
        self.objectifs_egalim_atteints = self.compute_objectifs_egalim_atteints()

    def populate_cout_repas(self):
        self.cout_repas = self.compute_cout_repas()

    def label_sum(self, label: str):
        sum = 0
        is_null = True
        for family in get_teledeclaration_field_groups(self.year, "APPRO_FAMILIES"):
            value = getattr(self, f"valeur_{family}_{label}")
            if value is not None:
                is_null = False
                sum = sum + value
        if not is_null:
            return sum

    def label_group_sum(self, label_group: str):
        if self.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
            return sum_int_with_potential_null(
                [
                    self.label_sum(label)
                    for label in get_teledeclaration_field_groups(self.year, "APPRO_LABELS_GROUPS_MAPPING")[
                        label_group
                    ]
                ]
            )
        return getattr(self, f"valeur_{label_group}")

    def label_group_group_sum(self, label_group_group: str):
        return sum_int_with_potential_null(
            [
                self.label_group_sum(label_group)
                for label_group in get_teledeclaration_field_groups(self.year, "APPRO_LABELS_GROUPS_GROUPS_MAPPING")[
                    label_group_group
                ]
            ]
        )

    def label_has_any_family_filled(self, label):
        """
        Whether any valeur_<famille>_<label> field is filled (0 counts as filled), for any family
        """
        families = get_teledeclaration_field_groups(self.year, "APPRO_FAMILIES")
        return has_any_value_filled(getattr(self, f"valeur_{family}_{label}", None) for family in families)

    def family_sum(self, family: str):
        """
        NOTE: APPRO_LABELS does not include APPRO_LABELS_ORIGINE & circuit_court & local
        """
        sum = 0
        for label in get_teledeclaration_field_groups(self.year, "APPRO_LABELS"):
            value = getattr(self, f"valeur_{family}_{label}")
            if value:
                sum = sum + value
        return sum

    def egalim_sum(self):
        # return self.label_group_group_sum("egalim")
        return sum_int_with_potential_null(
            [
                getattr(self, f"valeur_{group}")
                for group in get_teledeclaration_field_groups(self.year, "APPRO_LABELS_GROUPS_GROUPS_MAPPING")[
                    "egalim"
                ]
            ]
        )

    def family_has_any_label_filled(self, family):
        """
        Whether any valeur_<famille>_<label> field is filled (0 counts as filled), for any label (including the
        egalim aggregate, only defined for 2 families)
        """
        labels = get_teledeclaration_field_groups(self.year, "APPRO_LABELS_ALL") + ["egalim"]
        return has_any_value_filled(getattr(self, f"valeur_{family}_{label}", None) for label in labels)

    def compute_objectifs_egalim_atteints(self):
        canteen_region = self.canteen_snapshot.get("region") if self.canteen_snapshot else None
        return objectifs_egalim_atteints(self.year, canteen_region, self.pourcentage_bio, self.pourcentage_egalim)

    def compute_cout_repas(self):
        if self.valeur_totale and self.canteen_yearly_meal_count:
            return round(to_decimal(self.valeur_totale) / to_decimal(self.canteen_yearly_meal_count), 2)
        return None

    @property
    def percentage_valeur_totale(self) -> float:
        return 1

    @property
    def percentage_valeur_bio(self) -> float | None:
        if self.valeur_totale and self.valeur_bio is not None:
            return self.valeur_bio / self.valeur_totale
        return None

    @property
    def percentage_valeur_siqo(self) -> float | None:
        if self.valeur_totale and self.valeur_siqo is not None:
            return self.valeur_siqo / self.valeur_totale
        return None

    @property
    def percentage_valeur_externalites_performance(self) -> float | None:
        if self.valeur_totale and self.valeur_externalites_performance is not None:
            return self.valeur_externalites_performance / self.valeur_totale
        return None

    @property
    def percentage_valeur_egalim_autres(self) -> float | None:
        if self.valeur_totale and self.valeur_egalim_autres is not None:
            return self.valeur_egalim_autres / self.valeur_totale
        return None

    @property
    def percentage_valeur_viandes_volailles_egalim(self) -> float | None:
        if self.valeur_viandes_volailles and self.valeur_viandes_volailles_egalim is not None:
            return self.valeur_viandes_volailles_egalim / self.valeur_viandes_volailles
        return None

    @property
    def percentage_valeur_viandes_volailles_france(self) -> float | None:
        if self.valeur_viandes_volailles and self.valeur_viandes_volailles_france is not None:
            return self.valeur_viandes_volailles_france / self.valeur_viandes_volailles
        return None

    @property
    def percentage_valeur_produits_de_la_mer_egalim(self) -> float | None:
        if self.valeur_produits_de_la_mer and self.valeur_produits_de_la_mer_egalim is not None:
            return self.valeur_produits_de_la_mer_egalim / self.valeur_produits_de_la_mer
        return None

    @property
    def percentage_valeur_produits_de_la_mer_france(self) -> float | None:
        if self.valeur_produits_de_la_mer and self.valeur_produits_de_la_mer_france is not None:
            return self.valeur_produits_de_la_mer_france / self.valeur_produits_de_la_mer
        return None

    @property
    def valeur_totale_is_filled(self):
        return self.valeur_totale and self.valeur_totale > 0

    @property
    def is_diagnostic_type_simple(self):
        return self.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE

    @property
    def is_diagnostic_type_complete(self):
        return self.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE

    @property
    def is_empty(self) -> bool:
        return (
            not self.year
            or not self.diagnostic_type
            or (self.year and self.year >= 2026 and not self.nombre_repas_an)
            or not self.valeur_totale
        )

    @property
    def is_filled_simple(self) -> bool:
        return (
            not diagnostic_validators.validate_year(self)
            and self.is_diagnostic_type_simple
            and self.valeur_totale_is_filled
            and all(
                getattr(self, field) is not None
                for field in get_teledeclaration_fields_required(self.year, "APPROVISIONNEMENT", self.diagnostic_type)
            )
        )

    @property
    def is_filled_complete(self) -> bool:
        return (
            not diagnostic_validators.validate_year(self)
            and self.is_diagnostic_type_complete
            and self.valeur_totale_is_filled
            and all(
                getattr(self, field) is not None
                for field in get_teledeclaration_fields_required(self.year, "APPROVISIONNEMENT", self.diagnostic_type)
            )
        )

    def _is_filled(self) -> bool:
        return bool(self.is_filled_simple or self.is_filled_complete)

    def is_clean(self, raise_errors=False) -> tuple[bool, dict]:
        try:
            self.full_clean()
            return True, {}
        except ValidationError as e:
            if raise_errors:
                raise
            return False, e.message_dict

    @property
    def has_invalid_reason(self) -> bool:
        return self.invalid_reason_list and len(self.invalid_reason_list) > 0

    @property
    def is_teledeclared(self) -> bool:
        return self.status == Diagnostic.DiagnosticStatus.SUBMITTED

    @property
    def is_teledeclared_by_cc(self) -> bool:
        return self.teledeclaration_mode and self.teledeclaration_mode in [
            Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO,
            Diagnostic.TeledeclarationMode.CENTRAL_APPRO,
            Diagnostic.TeledeclarationMode.CENTRAL_ALL,
        ]

    @property
    def canteen_yearly_meal_count(self):
        if self.year >= 2026:
            return self.nombre_repas_an
        else:
            if self.canteen_snapshot:
                return self.canteen_snapshot.get("yearly_meal_count")
            elif self.canteen:
                return self.canteen.yearly_meal_count
        return None

    @property
    def canteen_snapshot_sector_lib_list(self):
        from data.models.sector import get_sector_lib_list_from_canteen_snapshot

        return get_sector_lib_list_from_canteen_snapshot(self.canteen_snapshot)

    @property
    def canteen_snapshot_category_lib_list(self):
        from data.models.sector import get_category_lib_list_from_canteen_snapshot

        return get_category_lib_list_from_canteen_snapshot(self.canteen_snapshot)

    @property
    def canteen_and_satellites_snapshot_id_list(self):
        id_list = []
        if self.canteen_snapshot and self.canteen_snapshot.get("id"):
            id_list.append(self.canteen_snapshot["id"])
        if self.satellites_snapshot and isinstance(self.satellites_snapshot, list):
            for satellite in self.satellites_snapshot:
                if satellite.get("id"):
                    id_list.append(satellite["id"])
        return id_list

    @property
    def latest_submitted_teledeclaration(self):
        submitted_teledeclarations = self.teledeclaration_set.submitted()
        if submitted_teledeclarations.count() == 0:
            return None
        return submitted_teledeclarations.order_by("-creation_date").first()

    @property
    def appro_badge(self) -> bool | None:
        total = self.valeur_totale
        if total:
            bio_percent = (self.valeur_bio or 0) / total
            egalim_percent = self.egalim_sum() / total

            # * 100 to get around floating point errors when we are on the cusp
            if objectifs_egalim_atteints(self.year, self.canteen.region, bio_percent * 100, egalim_percent * 100):
                return True
        if self.tunnel_appro:
            return False

    @property
    def waste_badge(self) -> bool | None:
        if self.has_waste_diagnostic and self.waste_actions and len(self.waste_actions) > 0:
            if self.has_donation_agreement or (self.canteen.daily_meal_count and self.canteen.daily_meal_count < 3000):
                return True
        if self.tunnel_waste:
            return False

    @property
    def diversification_badge(self) -> bool | None:
        has_daily_frequency = self.vegetarian_weekly_recurrence == Diagnostic.VegetarianMenuFrequency.DAILY
        has_weekly_or_more_frequency = self.vegetarian_weekly_recurrence in [
            Diagnostic.VegetarianMenuFrequency.DAILY,
            Diagnostic.VegetarianMenuFrequency.MID,
            Diagnostic.VegetarianMenuFrequency.HIGH,
        ]
        # Only the canteens with more than 200 daily meals with a diversification plan
        if self.canteen.daily_meal_count and self.canteen.daily_meal_count >= 200 and self.has_diversification_plan:
            return True
        # Only the canteens in the administration sector must have a daily frequency
        if self.canteen.in_administration and has_daily_frequency:
            return True
        if not self.canteen.in_administration and has_weekly_or_more_frequency:
            return True
        if self.tunnel_diversification:
            return False

    @property
    def plastic_badge(self) -> bool | None:
        if (
            self.cooking_plastic_substituted
            and self.serving_plastic_substituted
            and self.plastic_bottles_substituted
            and self.plastic_tableware_substituted
        ):
            return True
        if self.tunnel_plastic:
            return False

    @property
    def info_badge(self) -> bool | None:
        if self.communicates_on_food_quality:
            return True
        if self.tunnel_info:
            return False

    def _should_use_central_kitchen_appro(self):
        if self.canteen.is_satellite:
            if self.canteen.groupe_id:
                try:
                    groupe = self.canteen.groupe
                    existing_diagnostic = groupe.diagnostics.get(year=self.year)
                    handles_satellite_data = existing_diagnostic.central_kitchen_diagnostic_mode in [
                        Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                        Diagnostic.CentralKitchenDiagnosticMode.ALL,
                    ]
                    return groupe.is_groupe and handles_satellite_data
                except (Canteen.DoesNotExist, Canteen.MultipleObjectsReturned, Diagnostic.DoesNotExist):
                    pass
        return False

    def _get_teledeclaration_mode(self):
        uses_central_kitchen_appro = self._should_use_central_kitchen_appro()
        if uses_central_kitchen_appro:
            return Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO
        if self.canteen.is_groupe_or_central_cuisine:
            if self.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.ALL:
                return Diagnostic.TeledeclarationMode.CENTRAL_ALL
            if self.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO:
                return Diagnostic.TeledeclarationMode.CENTRAL_APPRO
        return Diagnostic.TeledeclarationMode.SITE

    def clear_appro_fields_not_matching_diagnostic_type(self):
        """
        Since 2026, appro fields that don't belong to this diagnostic's type must stay empty:
        only the fields for that type (SIMPLE or COMPLETE) may be filled, the rest are cleared.
        NOTE: called from teledeclare() (not save()), so a manager can freely switch
        diagnostic_type while filling out a diagnostic without losing data until they actually
        submit it.
        NOTE: SIMPLIFIED_DIAGNOSTIC_FIELDS are kept regardless of type, since COMPLETE diagnostics
        derive them automatically (see populate_simplified_diagnostic_values).
        """
        if not (self.year and int(self.year) >= 2026):
            return
        if not self.diagnostic_type or self.diagnostic_type not in Diagnostic.DiagnosticType.values:
            return
        matching_fields = set(
            get_teledeclaration_fields_all(self.year, "APPROVISIONNEMENT", self.diagnostic_type)
        ) | set(Diagnostic.SIMPLIFIED_DIAGNOSTIC_FIELDS)
        for field_name in Diagnostic.APPRO_FIELDS:
            if field_name not in matching_fields:
                setattr(self, field_name, None)

    def teledeclare(self, applicant, skip_validations=False):
        """
        Teledeclare the diagnostic
        - applicant is mandatory (User instance)
        - skip_validations: if True, skip validation checks (USE WITH CAUTION) (only for tests)
        """
        if not skip_validations:
            # status & campaign dates validations
            diagnostic_teledeclaration_validators.validate_is_in_teledeclaration_or_correction_period("teledeclare")
            diagnostic_teledeclaration_validators.validate_diagnostic_year_in_teledeclaration_period(self)
            diagnostic_teledeclaration_validators.validate_not_already_teledeclared(self)
            # canteen validations
            diagnostic_teledeclaration_validators.validate_diagnostic_is_filled(self)
            diagnostic_teledeclaration_validators.validate_canteen_is_filled(self)
            diagnostic_teledeclaration_validators.validate_canteen_groupe_satellites(self)
            diagnostic_teledeclaration_validators.validate_applicant_is_canteen_manager(self, applicant)
        # only once past every check above that could still raise: clearing earlier would mutate
        # the instance even if teledeclare() ends up failing
        self.clear_appro_fields_not_matching_diagnostic_type()
        if not skip_validations:
            # field validations
            self.is_clean(raise_errors=True)

        from api.serializers import CanteenTeledeclarationSerializer, SatelliteTeledeclarationSerializer

        # canteen data
        serialized_canteen = CanteenTeledeclarationSerializer(self.canteen).data
        self.canteen_snapshot = serialized_canteen

        # satellites data
        if self.canteen.is_groupe_or_central_cuisine:
            serialized_satellites = [SatelliteTeledeclarationSerializer(x).data for x in self.canteen.satellites]
            self.satellites_snapshot = serialized_satellites

        # applicant data
        self.applicant = applicant
        self.applicant_snapshot = {
            "id": applicant.id,
            "name": applicant.get_full_name(),
            "email": applicant.email,
        }

        # computed data (agg & EGalim & cout_repas)
        # see save()

        # metadata
        self.status = Diagnostic.DiagnosticStatus.SUBMITTED
        self.teledeclaration_date = timezone.now()
        self.teledeclaration_mode = self._get_teledeclaration_mode()
        self.teledeclaration_version = TELEDECLARATION_CURRENT_VERSION
        self.teledeclaration_id = self.id

        # update declaration_donnees_year to True & save (for non-SATELLITE_WITHOUT_APPRO TDs)
        canteen_id_list_to_update = []
        if self.teledeclaration_mode != Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO:
            canteen_id_list_to_update = self.canteen_and_satellites_snapshot_id_list
        with transaction.atomic():
            Canteen.all_objects.filter(id__in=canteen_id_list_to_update).update(
                **{f"declaration_donnees_{self.year}": True}
            )
            self.save()

    def cancel(self):
        """
        Cancel the teledeclared diagnostic
        """
        diagnostic_teledeclaration_validators.validate_is_in_teledeclaration_or_correction_period("cancel")
        diagnostic_teledeclaration_validators.validate_diagnostic_year_in_teledeclaration_period(self)
        diagnostic_teledeclaration_validators.validate_is_teledeclared(self)

        # before deleting the snapshots
        canteen_id_list_to_update = []
        if self.teledeclaration_mode != Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO:
            canteen_id_list_to_update = self.canteen_and_satellites_snapshot_id_list

        # reset fields
        self.status = (
            Diagnostic.DiagnosticStatus.CORRECTION
            if is_in_correction(self.year)
            else Diagnostic.DiagnosticStatus.DRAFT
        )
        self.applicant = None
        for field in self.TELEDECLARATION_SNAPSHOT_FIELDS:
            setattr(self, field, None)
        for field in self.TELEDECLARATION_FIELDS:
            setattr(self, field, None)

        # update declaration_donnees_year to True & save (for non-SATELLITE_WITHOUT_APPRO TDs)
        with transaction.atomic():
            Canteen.all_objects.filter(id__in=canteen_id_list_to_update).update(
                **{f"declaration_donnees_{self.year}": False}
            )
            self.save()
