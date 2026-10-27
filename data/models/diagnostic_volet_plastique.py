from django.db import models

from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all_years


class DiagnosticVoletPlastiqueMixin(models.Model):
    """
    Volet "Substitution des plastiques"
    """

    # all the fields of the volet (all years, see diagnostic_teledeclaration_fields.py)
    PLASTIC_FIELDS = get_teledeclaration_fields_all_years("PLASTIQUE")

    cooking_plastic_substituted = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de cuisson en plastique remplacés",
    )
    serving_plastic_substituted = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de service en plastique remplacés",
    )
    plastic_bottles_substituted = models.BooleanField(
        blank=True, null=True, verbose_name="bouteilles en plastique remplacées"
    )
    plastic_tableware_substituted = models.BooleanField(
        blank=True, null=True, verbose_name="ustensils en plastique remplacés"
    )

    class Meta:
        abstract = True
