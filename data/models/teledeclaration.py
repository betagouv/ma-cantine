import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from data.models import Canteen, Diagnostic

logger = logging.getLogger(__name__)


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

    uses_central_kitchen_appro = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Cantine satellite dont les données d'appro ont été prises en charge par la cuisine centrale",
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
    def should_use_central_kitchen_appro(diagnostic):
        is_satellite = diagnostic.canteen.production_type == Canteen.ProductionType.ON_SITE_CENTRAL
        if is_satellite and diagnostic.canteen.central_producer_siret:
            try:
                central_kitchen = Canteen.objects.get(siret=diagnostic.canteen.central_producer_siret)
                existing_diagnostic = central_kitchen.diagnostic_set.get(year=diagnostic.year)
                if (
                    existing_diagnostic.central_kitchen_diagnostic_mode
                    == Diagnostic.CentralKitchenDiagnosticMode.APPRO
                    or existing_diagnostic.central_kitchen_diagnostic_mode
                    == Diagnostic.CentralKitchenDiagnosticMode.ALL
                ):
                    return True
            except Exception:
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

        version = "6"  # Helps identify which data will be present. Use incremental int values
        # Version 6 - allows partial teledeclarations for satellite canteens when the central cuisine has declared for them

        status = status or Teledeclaration.TeledeclarationStatus.SUBMITTED
        canteen = diagnostic.canteen
        simplified_appro_fields = [
            "value_total_ht",
            "value_bio_ht",
            "value_sustainable_ht",
            "value_externality_performance_ht",
            "value_egalim_others_ht",
            "value_meat_poultry_ht",
            "value_meat_poultry_egalim_ht",
            "value_meat_poultry_france_ht",
            "value_fish_ht",
            "value_fish_egalim_ht",
        ]
        extended_appro_fields = [
            "value_total_ht",
            "value_meat_poultry_ht",
            "value_fish_ht",
            "value_viandes_volailles_bio",
            "value_produits_de_la_mer_bio",
            "value_fruits_et_legumes_bio",
            "value_charcuterie_bio",
            "value_produits_laitiers_bio",
            "value_boulangerie_bio",
            "value_boissons_bio",
            "value_autres_bio",
            "value_viandes_volailles_label_rouge",
            "value_produits_de_la_mer_label_rouge",
            "value_fruits_et_legumes_label_rouge",
            "value_charcuterie_label_rouge",
            "value_produits_laitiers_label_rouge",
            "value_boulangerie_label_rouge",
            "value_boissons_label_rouge",
            "value_autres_label_rouge",
            "value_viandes_volailles_aocaop_igp_stg",
            "value_produits_de_la_mer_aocaop_igp_stg",
            "value_fruits_et_legumes_aocaop_igp_stg",
            "value_charcuterie_aocaop_igp_stg",
            "value_produits_laitiers_aocaop_igp_stg",
            "value_boulangerie_aocaop_igp_stg",
            "value_boissons_aocaop_igp_stg",
            "value_autres_aocaop_igp_stg",
            "value_viandes_volailles_hve",
            "value_produits_de_la_mer_hve",
            "value_fruits_et_legumes_hve",
            "value_charcuterie_hve",
            "value_produits_laitiers_hve",
            "value_boulangerie_hve",
            "value_boissons_hve",
            "value_autres_hve",
            "value_viandes_volailles_peche_durable",
            "value_produits_de_la_mer_peche_durable",
            "value_fruits_et_legumes_peche_durable",
            "value_charcuterie_peche_durable",
            "value_produits_laitiers_peche_durable",
            "value_boulangerie_peche_durable",
            "value_boissons_peche_durable",
            "value_autres_peche_durable",
            "value_viandes_volailles_rup",
            "value_produits_de_la_mer_rup",
            "value_fruits_et_legumes_rup",
            "value_charcuterie_rup",
            "value_produits_laitiers_rup",
            "value_boulangerie_rup",
            "value_boissons_rup",
            "value_autres_rup",
            "value_viandes_volailles_fermier",
            "value_produits_de_la_mer_fermier",
            "value_fruits_et_legumes_fermier",
            "value_charcuterie_fermier",
            "value_produits_laitiers_fermier",
            "value_boulangerie_fermier",
            "value_boissons_fermier",
            "value_autres_fermier",
            "value_viandes_volailles_externalites",
            "value_produits_de_la_mer_externalites",
            "value_fruits_et_legumes_externalites",
            "value_charcuterie_externalites",
            "value_produits_laitiers_externalites",
            "value_boulangerie_externalites",
            "value_boissons_externalites",
            "value_autres_externalites",
            "value_viandes_volailles_commerce_equitable",
            "value_produits_de_la_mer_commerce_equitable",
            "value_fruits_et_legumes_commerce_equitable",
            "value_charcuterie_commerce_equitable",
            "value_produits_laitiers_commerce_equitable",
            "value_boulangerie_commerce_equitable",
            "value_boissons_commerce_equitable",
            "value_autres_commerce_equitable",
            "value_viandes_volailles_performance",
            "value_produits_de_la_mer_performance",
            "value_fruits_et_legumes_performance",
            "value_charcuterie_performance",
            "value_produits_laitiers_performance",
            "value_boulangerie_performance",
            "value_boissons_performance",
            "value_autres_performance",
            "value_viandes_volailles_non_egalim",
            "value_produits_de_la_mer_non_egalim",
            "value_fruits_et_legumes_non_egalim",
            "value_charcuterie_non_egalim",
            "value_produits_laitiers_non_egalim",
            "value_boulangerie_non_egalim",
            "value_boissons_non_egalim",
            "value_autres_non_egalim",
            "value_viandes_volailles_france",
            "value_produits_de_la_mer_france",
            "value_fruits_et_legumes_france",
            "value_charcuterie_france",
            "value_produits_laitiers_france",
            "value_boulangerie_france",
            "value_boissons_france",
            "value_autres_france",
            "value_viandes_volailles_short_distribution",
            "value_produits_de_la_mer_short_distribution",
            "value_fruits_et_legumes_short_distribution",
            "value_charcuterie_short_distribution",
            "value_produits_laitiers_short_distribution",
            "value_boulangerie_short_distribution",
            "value_boissons_short_distribution",
            "value_autres_short_distribution",
            "value_viandes_volailles_local",
            "value_produits_de_la_mer_local",
            "value_fruits_et_legumes_local",
            "value_charcuterie_local",
            "value_produits_laitiers_local",
            "value_boulangerie_local",
            "value_boissons_local",
            "value_autres_local",
        ]
        appro_fields = (
            extended_appro_fields
            if diagnostic.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE
            else simplified_appro_fields
        )
        json_appro_teledeclaration = {}
        uses_central_kitchen_appro = Teledeclaration.should_use_central_kitchen_appro(diagnostic)
        if not uses_central_kitchen_appro:
            for prop in appro_fields:
                json_appro_teledeclaration[prop] = (
                    float(getattr(diagnostic, prop)) if getattr(diagnostic, prop) is not None else None
                )
        json_other_teledeclaration = {
            "diagnostic_type": diagnostic.diagnostic_type or "Unknown",
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
        }
        is_central_cuisine = (
            diagnostic.canteen.production_type == Canteen.ProductionType.CENTRAL
            or diagnostic.canteen.production_type == Canteen.ProductionType.CENTRAL_SERVING
        )
        json_fields = {
            "version": version,
            "year": diagnostic.year,
            "canteen": {
                "id": canteen.id,
                "name": canteen.name,
                "siret": canteen.siret,
                "city_insee_code": canteen.city_insee_code,
            },
            "applicant": {
                "name": applicant.get_full_name(),
                "email": applicant.email,
            },
            "uses_central_kitchen_appro": uses_central_kitchen_appro,
            "central_kitchen_siret": diagnostic.canteen.central_producer_siret,
            "teledeclaration": {**json_appro_teledeclaration, **json_other_teledeclaration},
            "central_kitchen_diagnostic_mode": diagnostic.central_kitchen_diagnostic_mode
            if is_central_cuisine
            else None,
        }
        return TeledeclarationFactory.create(
            applicant=applicant,
            year=diagnostic.year,
            canteen=diagnostic.canteen,
            canteen_siret=canteen.siret,
            status=status,
            diagnostic=diagnostic,
            declared_data=json_fields,
            uses_central_kitchen_appro=uses_central_kitchen_appro,
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
