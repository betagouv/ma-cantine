import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q, Sum
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from simple_history.models import HistoricalRecords

from data.models import AuthenticationMethodHistoricalRecords, Canteen, Diagnostic
from data.utils import CustomJSONEncoder
from macantine.utils import CAMPAIGN_DATES, EGALIM_OBJECTIVES, is_in_teledeclaration_or_correction

logger = logging.getLogger(__name__)


def in_teledeclaration_campaign_query(year):
    year = int(year)
    return Q(
        creation_date__range=(
            CAMPAIGN_DATES[year]["teledeclaration_start_date"],
            CAMPAIGN_DATES[year]["teledeclaration_end_date"],
        )
    )


def in_correction_campaign_query(year):
    year = int(year)
    return Q(
        creation_date__range=(
            CAMPAIGN_DATES[year]["correction_start_date"],
            CAMPAIGN_DATES[year]["correction_end_date"],
        )
    )


class TeledeclarationQuerySet(models.QuerySet):
    def submitted(self):
        return self.filter(status=Teledeclaration.TeledeclarationStatus.SUBMITTED)

    def cancelled(self):
        return self.filter(status=Teledeclaration.TeledeclarationStatus.CANCELLED)

    def exclude_aberrant_values(self):
        return self.exclude(meal_price__isnull=False, meal_price__gt=20, value_total_ht__gt=1000000)

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

    def submitted_for_year(self, year):
        return self.submitted().in_year(year).in_campaign(year)

    def canteen_not_deleted_during_campaign(self, year):
        year = int(year)
        return self.exclude(
            canteen__deletion_date__range=(
                CAMPAIGN_DATES[year]["teledeclaration_start_date"],
                CAMPAIGN_DATES[year]["teledeclaration_end_date"],
            )
        )

    def canteen_has_siret_or_siren_unite_legale(self):
        return self.filter(
            ~Q(canteen_siret=None) & ~Q(canteen_siret="")
            | ~Q(canteen_siren_unite_legale=None) & ~Q(canteen_siren_unite_legale="")
        )

    def canteen_for_stat(self, year):
        return (
            self.select_related("canteen")
            .filter(canteen_id__isnull=False)
            .canteen_not_deleted_during_campaign(year)  # Chaîne de traitement n°6
            .canteen_has_siret_or_siren_unite_legale()  # Chaîne de traitement n°7
        )

    def valid_td_by_year(self, year):
        year = int(year)
        if year in CAMPAIGN_DATES.keys():
            return (
                self.submitted_for_year(year)
                .exclude(teledeclaration_mode="SATELLITE_WITHOUT_APPRO")
                .filter(value_bio_ht_agg__isnull=False)
                .canteen_for_stat(year)  # Chaîne de traitement n°6 & n°7
                .exclude_aberrant_values()  # Chaîne de traitement n°8
            )
        else:
            return self.none()

    def historical_valid_td(self, years: list):
        results = self.none()
        for year in years:
            results = results | self.valid_td_by_year(year)
        return results.select_related("canteen", "diagnostic")

    def publicly_visible(self):
        return self.exclude(canteen__production_type=Canteen.ProductionType.GROUPE).exclude(
            canteen__line_ministry=Canteen.Ministries.ARMEE
        )

    def with_appro_percent_stats(self):
        """
        Note: we use Sum/default instead of F to better manage None values.
        """
        return self.annotate(
            bio_percent=100 * Sum("value_bio_ht_agg", default=0) / Sum("value_total_ht"),
            value_egalim_ht_agg=Sum("value_bio_ht_agg", default=0)
            + Sum("value_sustainable_ht_agg", default=0)
            + Sum("value_externality_performance_ht_agg", default=0)
            + Sum("value_egalim_others_ht_agg", default=0),
            egalim_percent=100 * F("value_egalim_ht_agg") / Sum("value_total_ht"),
        )

    def egalim_objectives_reached(self):
        return self.filter(
            Q(
                bio_percent__gte=EGALIM_OBJECTIVES["hexagone"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["hexagone"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_OBJECTIVES["groupe_1"]["region_list"],
                bio_percent__gte=EGALIM_OBJECTIVES["groupe_1"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["groupe_1"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_OBJECTIVES["groupe_2"]["region_list"],
                bio_percent__gte=EGALIM_OBJECTIVES["groupe_2"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["groupe_2"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_OBJECTIVES["groupe_3"]["region_list"],
                bio_percent__gte=EGALIM_OBJECTIVES["groupe_3"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["groupe_3"]["egalim_percent"],
            )
        )


class Teledeclaration(models.Model):
    class TeledeclarationStatus(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Télédéclaré"
        CANCELLED = "CANCELLED", "Annulé"

    class Meta:
        verbose_name = "télédéclaration"
        verbose_name_plural = "télédéclarations"
        constraints = [
            models.UniqueConstraint(
                fields=["year", "canteen"], condition=models.Q(status="SUBMITTED"), name="unique_submitted_td"
            )
        ]
        indexes = [models.Index(fields=["canteen", "year"])]

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

    objects = models.Manager.from_queryset(TeledeclarationQuerySet)()

    # Fields that pertain to the teledeclaration. These fields
    # will not change and should contain all information to be
    # sent to the system that will treat the teledeclarations.

    declared_data = models.JSONField(verbose_name="Champs", encoder=CustomJSONEncoder)

    # Structured non-null fields for validation / querying.
    # These fields cannot be null and will not change if the
    # canteen or diagnostic objects change.

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    year = models.IntegerField(verbose_name="année")
    canteen_siret = models.TextField(null=True, blank=True)
    canteen_siren_unite_legale = models.TextField(null=True, blank=True)

    value_total_ht = models.IntegerField(
        null=True, blank=True, verbose_name="Champ value total (en cas de TD détaillée, ce champ est aggrégé)"
    )
    value_bio_ht_agg = models.IntegerField(
        null=True, blank=True, verbose_name="Champ value bio (en cas de TD détaillée, ce champ est aggrégé)"
    )
    value_sustainable_ht_agg = models.IntegerField(
        null=True, blank=True, verbose_name="Champ value Egalim (en cas de TD détaillée, ce champ est aggrégé)"
    )
    value_externality_performance_ht_agg = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Champ externalité/performance (en cas de TD détaillée, ce champ est aggrégé)",
    )
    value_egalim_others_ht_agg = models.IntegerField(
        null=True, blank=True, verbose_name="Champ Autres Egalim (en cas de TD détaillée, ce champ est aggrégé)"
    )
    yearly_meal_count = models.IntegerField(null=True, blank=True, verbose_name="Nombre de repas servis par an")
    meal_price = models.FloatField(null=True, blank=True, verbose_name="Coût denrées")

    history = HistoricalRecords(
        bases=[
            AuthenticationMethodHistoricalRecords,
        ]
    )

    status = models.CharField(
        max_length=255,
        choices=TeledeclarationStatus.choices,
        verbose_name="status",
    )

    # Auxiliary relation fields for querying / reporting. May
    # be null in case of deletion. Additionally, the linked model may have
    # been modified since. For the actual data see the fields above.

    applicant = models.ForeignKey(
        get_user_model(),
        verbose_name="déclarant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    canteen = models.ForeignKey(
        Canteen,
        verbose_name="cantine",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    diagnostic = models.ForeignKey(
        Diagnostic,
        verbose_name="diagnostic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # a TD can use SATELLITE_WITHOUT_APPRO mode, as well as have some appro data of its own if,
    # for example, the manager of the satellite canteen started completing a diagnostic and then the
    # central kitchen decided to declare for its satellites.
    # We are leaving it up to the team to interpret the data in this case.
    teledeclaration_mode = models.CharField(
        max_length=255,
        choices=TeledeclarationMode.choices,
        verbose_name="mode de télédéclaration",
        null=True,
        blank=True,
    )

    @property
    def is_declared_by_cc(self):
        return self.teledeclaration_mode and self.teledeclaration_mode in [
            Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO,
            Teledeclaration.TeledeclarationMode.CENTRAL_APPRO,
            Teledeclaration.TeledeclarationMode.CENTRAL_ALL,
        ]

    @receiver(pre_delete, sender=Diagnostic)
    def cancel_teledeclaration(sender, instance, **kwargs):
        try:
            teledeclaration = Teledeclaration.objects.get(diagnostic=instance)
            teledeclaration.cancel()
        except Exception:
            pass

    @staticmethod
    def should_use_central_kitchen_appro(diagnostic):
        is_satellite = diagnostic.canteen.production_type == Canteen.ProductionType.ON_SITE_CENTRAL
        if is_satellite and diagnostic.canteen.central_producer_siret:
            try:
                central_kitchen = Canteen.objects.get(siret=diagnostic.canteen.central_producer_siret)
                existing_diagnostic = central_kitchen.diagnostics.get(year=diagnostic.year)
                handles_satellite_data = existing_diagnostic.central_kitchen_diagnostic_mode in [
                    Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                    Diagnostic.CentralKitchenDiagnosticMode.ALL,
                ]
                return central_kitchen.is_central_cuisine and handles_satellite_data
            except (Canteen.DoesNotExist, Canteen.MultipleObjectsReturned, Diagnostic.DoesNotExist):
                pass
        return False

    @staticmethod
    def validate_diagnostic(diagnostic):
        if not is_in_teledeclaration_or_correction():
            raise ValidationError("Ce n'est pas possible de télédéclarer hors de la période de la campagne")
        last_year = timezone.now().date().year - 1
        if diagnostic.year != last_year:
            raise ValidationError(
                {
                    "year": f"C'est uniquement possible de télédéclarer pour l'année {last_year}. Ce diagnostic est pour l'année {diagnostic.year}"
                }
            )
        check_total_value = not Teledeclaration.should_use_central_kitchen_appro(diagnostic)
        if check_total_value and not diagnostic.valeur_totale:
            raise ValidationError("Données d'approvisionnement manquantes")
        if diagnostic.canteen.is_central_cuisine and not diagnostic.central_kitchen_diagnostic_mode:
            raise ValidationError("Question obligatoire : Quelles données sont déclarées par cette cuisine centrale ?")

    @staticmethod
    def create_from_diagnostic(diagnostic, applicant):
        """
        Create a teledeclaration object from a diagnostic
        """
        version = "15"  # Helps identify which data will be present. Use incremental int values
        # Version 15 - Changed how we store the canteen's line_ministry
        # Version 14 - New Teledeclaration.canteen_siren_unite_legale field, also add the field to the canteen serialization
        # Version 13 - Add category_name in canteen sectors serializer
        # Version 12 - New Diagnostic service_type field (and stop filling vegetarian_menu_type)
        # Version 11 - Requires diagnostic mode to be defined for central production types (in validate_diagnostic)
        # Version 10 - Add department and region fields
        # Version 9 - removes legacy fields: value_pat, value_label_hve, value_label_rouge, value_label_aoc_igp and value_pat

        teledeclaration_mode = None
        serialized_diagnostic = None
        canteen = diagnostic.canteen
        is_central_cuisine = canteen.is_central_cuisine

        teledeclaration_mode = Teledeclaration._get_teledeclaration_mode(diagnostic)
        serializer = Teledeclaration._get_diagnostic_serializer(diagnostic)
        serialized_diagnostic = serializer(diagnostic).data

        from api.serializers import CanteenTeledeclarationSerializer, SatelliteTeledeclarationSerializer

        serialized_canteen = CanteenTeledeclarationSerializer(canteen).data

        json_fields = {
            "version": version,
            "year": diagnostic.year,
            "canteen": serialized_canteen,
            "applicant": {
                "name": applicant.get_full_name(),
                "email": applicant.email,
            },
            "central_kitchen_siret": serialized_canteen.get("central_producer_siret"),
            "teledeclaration": serialized_diagnostic,
        }

        if is_central_cuisine:
            serialized_satellites = [SatelliteTeledeclarationSerializer(x).data for x in canteen.satellites]
            json_fields["satellites"] = serialized_satellites
            json_fields["satellite_canteens_count"] = canteen.satellite_canteens_count

        if diagnostic.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
            diagnostic.populate_simplified_diagnostic_values()

        if diagnostic.valeur_totale and canteen.yearly_meal_count:
            meal_price = diagnostic.valeur_totale / canteen.yearly_meal_count
        else:
            meal_price = None

        return Teledeclaration.objects.create(
            applicant=applicant,
            year=diagnostic.year,
            canteen=canteen,
            canteen_siret=canteen.siret,
            canteen_siren_unite_legale=canteen.siren_unite_legale,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            diagnostic=diagnostic,
            declared_data=json_fields,
            teledeclaration_mode=teledeclaration_mode,
            value_total_ht=diagnostic.valeur_totale,
            value_bio_ht_agg=diagnostic.valeur_bio,
            value_sustainable_ht_agg=diagnostic.valeur_siqo,
            value_externality_performance_ht_agg=diagnostic.valeur_externalites_performance,
            value_egalim_others_ht_agg=diagnostic.valeur_egalim_autres,
            yearly_meal_count=canteen.yearly_meal_count,
            meal_price=meal_price,
        )

    @staticmethod
    def _get_diagnostic_serializer(diagnostic):
        from api.serializers import (
            ApproDeferredTeledeclarationDiagnosticSerializer,
            CompleteApproOnlyTeledeclarationDiagnosticSerializer,
            CompleteTeledeclarationDiagnosticSerializer,
            SimpleApproOnlyTeledeclarationDiagnosticSerializer,
            SimpleTeledeclarationDiagnosticSerializer,
        )

        uses_central_kitchen_appro = Teledeclaration.should_use_central_kitchen_appro(diagnostic)
        if uses_central_kitchen_appro:
            return ApproDeferredTeledeclarationDiagnosticSerializer

        if (
            diagnostic.canteen.is_central_cuisine
            and diagnostic.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO
        ):
            if diagnostic.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
                return CompleteApproOnlyTeledeclarationDiagnosticSerializer
            else:
                return SimpleApproOnlyTeledeclarationDiagnosticSerializer

        # both CC declaring all and on site declaring all
        if diagnostic.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
            return CompleteTeledeclarationDiagnosticSerializer
        else:
            return SimpleTeledeclarationDiagnosticSerializer

    @staticmethod
    def _get_teledeclaration_mode(diagnostic):
        uses_central_kitchen_appro = Teledeclaration.should_use_central_kitchen_appro(diagnostic)
        if uses_central_kitchen_appro:
            return Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO

        if diagnostic.canteen.is_central_cuisine:
            if diagnostic.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.ALL:
                return Teledeclaration.TeledeclarationMode.CENTRAL_ALL
            if diagnostic.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO:
                return Teledeclaration.TeledeclarationMode.CENTRAL_APPRO

        return Teledeclaration.TeledeclarationMode.SITE

    def cancel(self):
        """
        Cancel the teledeclaration.
        """
        self.status = Teledeclaration.TeledeclarationStatus.CANCELLED
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self):
        canteen_name = self.declared_data["canteen"]["name"] if self.declared_data.get("canteen") else ""
        return f"Télédéclaration pour {self.year} '{canteen_name}'"
