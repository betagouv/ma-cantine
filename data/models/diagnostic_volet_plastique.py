from django.db import models

from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all_years


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

    class Meta:
        abstract = True
