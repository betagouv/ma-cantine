from django.db import models

from data.fields import ChoiceArrayField
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all_years


class DiagnosticVoletInformationMixin(models.Model):
    """
    Volet "Information des convives"
    """

    class InformationSupport(models.TextChoices):
        EMAIL = "EMAIL", "Envoi d'e-mail aux convives ou à leurs représentants"
        AFFICHAGE = "AFFICHAGE", "Par affichage sur le lieu de restauration"
        SITE_INTERNET = "SITE_INTERNET", "Sur site internet ou intranet (mairie, cantine)"
        AUTRE = "AUTRE", "Autres moyens d'affichage et de communication électronique"
        ELECTRONIQUE = "ELECTRONIQUE", "Par voie électronique"

    class InformationFrequence(models.TextChoices):
        REGULIEREMENT = "REGULIEREMENT", "Régulièrement au cours de l’année"
        ANNUELLE = "ANNUELLE", "Une fois par an"
        MOINS_QUE_ANNUELLE = "MOINS_QUE_ANNUELLE", "Moins d'une fois par an"

    # all the fields of the volet (all years, see diagnostic_teledeclaration_fields.py)
    INFO_FIELDS = get_teledeclaration_fields_all_years("INFORMATION")

    information_supports = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=InformationSupport.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Communication utilisée",
    )
    information_supports_autre = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre communication utilisée",
    )
    information_support_url = models.URLField(blank=True, null=True, verbose_name="Lien de communication")
    information_qualite_nutritionnelle = models.BooleanField(
        blank=True, null=True, verbose_name="Communique sur le plan alimentaire"
    )
    information_qualite_durable = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Communique sur les démarches qualité/durables/équitables",
    )
    information_frequence = models.CharField(
        max_length=255,
        choices=InformationFrequence.choices,
        blank=True,
        null=True,
        verbose_name="fréquence de communication",
    )

    class Meta:
        abstract = True
