from django.db import models

from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_all_years,
    get_teledeclaration_fields_required,
)


class DiagnosticVoletPlastiqueMixin(models.Model):
    """
    Volet "Substitution des plastiques"
    """

    # all the fields of the volet (all years, see diagnostic_teledeclaration_fields.py)
    PLASTIC_FIELDS = get_teledeclaration_fields_all_years("PLASTIQUE")

    plastique_contenant_cuisson_remplace = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de cuisson en plastique remplacés",
    )
    plastique_contenant_service_remplace = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de service en plastique remplacés",
    )
    plastique_bouteille_remplace = models.BooleanField(
        blank=True, null=True, verbose_name="bouteilles en plastique remplacées"
    )
    plastique_ustensile_remplace = models.BooleanField(
        blank=True, null=True, verbose_name="ustensils en plastique remplacés"
    )

    # new in 2026 (see diagnostic_teledeclaration_fields.py)
    plastique_bouteille_boisson_remplace = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="La cantine est équipée d’au moins une fontaine d'eau potable accessible au public et n’assure aucune distribution gratuite de bouteilles en plastique contenant des boissons",
    )
    plastique_vaisselle_jetable_remplace = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Aucune vaisselle jetable n’est utilisée pour les repas consommés sur place (gobelets, assiette et récipients, couverts)",
    )
    plastique_contenant_remplace = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Aucun contenant alimentaire de cuisson, de réchauffage et de service en plastique sont utilisés au sein de l’établissement",
    )
    plastique_contenant_emporter_remplace = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Des contenants réutilisables ou composés de matières recyclables sont proposés pour l’ensemble des repas à emporter",
    )

    class Meta:
        abstract = True

    @property
    def is_filled_plastique(self) -> bool:
        # the volet must be started (at least one of its fields filled)
        is_started = any(
            getattr(self, field) is not None for field in get_teledeclaration_fields_all(self.year, "PLASTIQUE")
        )
        return is_started and all(
            getattr(self, field) is not None for field in get_teledeclaration_fields_required(self.year, "PLASTIQUE")
        )
