from django.db import models

from data.fields import ChoiceArrayField
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_all_years,
)


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
    # new in 2026 (replace the fields above, see diagnostic_teledeclaration_fields.py)
    information_affichage_permanent = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="La cantine dispose d’un affichage permanent à l’entrée du restaurant, actualisé au moins une fois par an et lisible par tous les usagers",
    )
    information_electronique_annuelle = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Une communication électronique (réalisée au moins une fois par an) permet aux usagers d’être informés",
    )
    information_part_egalim = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Part de produits EGalim (dont bio) entrant dans la composition des repas servis",
    )
    information_part_pat = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Part des produits issus de Projets alimentaires territoriaux (PAT)",
    )
    information_consultation_qualite = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="L’établissement informe et consulte régulièrement, par tous moyens utiles, les usagers sur le respect de la qualité alimentaire et nutritionnelle des repas servis",
    )

    class Meta:
        abstract = True

    @property
    def is_filled_information(self) -> bool:
        # At least one field of the volet is filled
        return any(
            getattr(self, field) is not None for field in get_teledeclaration_fields_all(self.year, "INFORMATION")
        )

    @property
    def is_clean_information(self) -> bool:
        return self._is_clean_volet("INFORMATION")
