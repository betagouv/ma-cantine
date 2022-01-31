from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from data.models import Canteen, Diagnostic


class Teledeclaration(models.Model):
    class Meta:
        verbose_name = "télédéclaration"
        verbose_name_plural = "télédéclarations"

    class TeledeclarationStatus(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Télédéclaré"
        CANCELLED = "CANCELLED", "Annulé"

    # Fields that pertain to the teledeclaration. These fields
    # will not change and should contain all information to be
    # sent to the system that will treat the teledeclarations.

    declared_data = models.JSONField(verbose_name="Champs")

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
    def createFromDiagnostic(diagnostic, applicant, status=None):
        """
        Create a teledeclaration object from a diagnostic
        """
        from data.factories import TeledeclarationFactory  # Avoids circular import

        status = status or Teledeclaration.TeledeclarationStatus.SUBMITTED
        canteen = diagnostic.canteen
        jsonFields = {
            "year": diagnostic.year,
            "canteen": {
                "name": canteen.name,
                "siret": canteen.siret,
                "city_insee_code": canteen.city_insee_code,
            },
            "applicant": {
                "name": applicant.get_full_name(),
                "email": applicant.email,
            },
            "teledeclaration": {
                "value_bio_ht": float(diagnostic.value_bio_ht),
                "value_sustainable_ht": float(diagnostic.value_sustainable_ht),
                "value_total_ht": float(diagnostic.value_total_ht),
                "has_waste_diagnostic": diagnostic.has_waste_diagnostic,
                "has_waste_plan": diagnostic.has_waste_plan,
                "has_donation_agreement": diagnostic.has_donation_agreement,
                "has_waste_measures": diagnostic.has_waste_measures,
                "has_diversification_plan": diagnostic.has_diversification_plan,
                "cooking_plastic_substituted": diagnostic.cooking_plastic_substituted,
                "serving_plastic_substituted": diagnostic.serving_plastic_substituted,
                "plastic_bottles_substituted": diagnostic.plastic_bottles_substituted,
                "plastic_tableware_substituted": diagnostic.plastic_tableware_substituted,
                "communicates_on_food_plan": diagnostic.communicates_on_food_plan,
                "communicates_on_food_quality": diagnostic.communicates_on_food_quality,
            },
        }
        return TeledeclarationFactory.create(
            applicant=applicant,
            year=diagnostic.year,
            canteen=diagnostic.canteen,
            canteen_siret=canteen.siret,
            status=status,
            diagnostic=diagnostic,
            declared_data=jsonFields,
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
