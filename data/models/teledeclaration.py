import logging
import decimal
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from data.models import Canteen, Diagnostic

logger = logging.getLogger(__name__)


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(CustomJSONEncoder, self).default(o)


class Teledeclaration(models.Model):
    class Meta:
        verbose_name = "télédéclaration"
        verbose_name_plural = "télédéclarations"

    class TeledeclarationStatus(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Télédéclaré"
        CANCELLED = "CANCELLED", "Annulé"

    class TeledeclarationMode(models.TextChoices):
        SATELLITE_WITHOUT_APPRO = (
            "SATELLITE_WITHOUT_APPRO",
            "Cantine satellite dont les données d'appro sont déclarées par la cuisine centrale",
        )
        CENTRAL_APPRO = "CENTRAL_APPRO", "Cuisine centrale déclarant les données d'appro pour ses cuisines satellites"
        CENTRAL_ALL = (
            "CENTRAL_ALL",
            "Cuisine centrale déclarant toutes les données EGAlim pour ses cuisines satellites",
        )
        SITE = "SITE", "Cantine déclarant ses propres données"

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

    @receiver(pre_delete, sender=Diagnostic)
    def cancel_teledeclaration(sender, instance, **kwargs):
        try:
            teledeclaration = Teledeclaration.objects.get(diagnostic=instance)
            teledeclaration.status = Teledeclaration.TeledeclarationStatus.CANCELLED
            teledeclaration.save()
        except Exception:
            pass

    def clean(self):
        """
        Verify there is only one submitted declaration per year/canteen
        at any given time.
        """
        if self.status == self.TeledeclarationStatus.SUBMITTED:
            duplicates = Teledeclaration.objects.filter(canteen=self.canteen, year=self.year, status=self.status)
            message = "Il existe déjà une télédéclaration en cours pour cette année"
            if duplicates.count() > 0:
                raise ValidationError({"year": message})
        return super().clean()

    @staticmethod
    def should_use_central_kitchen_appro(diagnostic):
        is_satellite = diagnostic.canteen.production_type == Canteen.ProductionType.ON_SITE_CENTRAL
        if is_satellite and diagnostic.canteen.central_producer_siret:
            try:
                central_kitchen = Canteen.objects.get(siret=diagnostic.canteen.central_producer_siret)
                existing_diagnostic = central_kitchen.diagnostic_set.get(year=diagnostic.year)
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
        check_total_value = not Teledeclaration.should_use_central_kitchen_appro(diagnostic)
        if check_total_value and not diagnostic.value_total_ht:
            raise ValidationError("Données d'approvisionnement manquantes")

    @staticmethod
    def create_from_diagnostic(diagnostic, applicant, status=None):
        """
        Create a teledeclaration object from a diagnostic
        """
        from data.factories import TeledeclarationFactory  # Avoids circular import
        from api.serializers import (
            SimpleTeledeclarationDiagnosticSerializer,
            CompleteTeledeclarationDiagnosticSerializer,
            ApproDeferredTeledeclarationDiagnosticSerializer,
        )

        version = "7"  # Helps identify which data will be present. Use incremental int values
        # Version 7 - contains all diagnostic fields relevant to the diagnostic type in JSON serialized object

        status = status or Teledeclaration.TeledeclarationStatus.SUBMITTED

        uses_central_kitchen_appro = Teledeclaration.should_use_central_kitchen_appro(diagnostic)

        teledeclaration_mode = None
        canteen = diagnostic.canteen
        is_central_cuisine = canteen.is_central_cuisine
        if uses_central_kitchen_appro:
            teledeclaration_mode = Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO
        elif (
            is_central_cuisine
            and diagnostic.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.ALL
        ):
            teledeclaration_mode = Teledeclaration.TeledeclarationMode.CENTRAL_ALL
        elif (
            is_central_cuisine
            and diagnostic.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO
        ):
            teledeclaration_mode = Teledeclaration.TeledeclarationMode.CENTRAL_APPRO
        else:
            teledeclaration_mode = Teledeclaration.TeledeclarationMode.SITE

        serialized_diagnostic = None
        if uses_central_kitchen_appro:
            serialized_diagnostic = ApproDeferredTeledeclarationDiagnosticSerializer(diagnostic)
        else:
            if diagnostic.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
                serialized_diagnostic = CompleteTeledeclarationDiagnosticSerializer(diagnostic)
            else:
                serialized_diagnostic = SimpleTeledeclarationDiagnosticSerializer(diagnostic)

        json_fields = {
            "version": version,
            "year": diagnostic.year,
            "canteen": {
                "id": canteen.id,
                "name": canteen.name,
                "siret": canteen.siret,
                "city_insee_code": canteen.city_insee_code,
                "production_type": canteen.production_type,
            },
            "applicant": {
                "name": applicant.get_full_name(),
                "email": applicant.email,
            },
            "central_kitchen_siret": canteen.central_producer_siret,
            "teledeclaration": serialized_diagnostic.data,
        }

        if is_central_cuisine:
            json_fields["satellites"] = [{"id": x.id, "siret": x.siret, "name": x.name} for x in canteen.satellites]
            json_fields["satellite_canteens_count"] = canteen.satellite_canteens_count

        return TeledeclarationFactory.create(
            applicant=applicant,
            year=diagnostic.year,
            canteen=canteen,
            canteen_siret=canteen.siret,
            status=status,
            diagnostic=diagnostic,
            declared_data=json_fields,
            teledeclaration_mode=teledeclaration_mode,
        )

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
