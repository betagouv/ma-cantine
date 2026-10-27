from django.core.validators import MaxValueValidator
from django.db import models

from data.fields import ChoiceArrayField
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all_years
from data.utils import make_optional_positive_decimal_field


class DiagnosticVoletGaspillageMixin(models.Model):
    """
    Volet "Lutte contre le gaspillage alimentaire"
    """

    class ActionsGaspillage(models.TextChoices):
        INSCRIPTION = "INSCRIPTION", "Pré-inscription des convives obligatoire"
        SENSIBILISATION = "SENSIBILISATION", "Sensibilisation par affichage ou autre média"
        FORMATION = "FORMATION", "Formation / information du personnel de restauration"
        DISTRIBUTION = (
            "DISTRIBUTION",
            "Réorganisation de la distribution des composantes du repas",
        )
        PORTIONS = "PORTIONS", "Choix des portions (grande faim, petite faim)"
        REUTILISATION = "REUTILISATION", "Réutilisation des restes de préparation / surplus"

    # all the fields of the volet (all years, see diagnostic_teledeclaration_fields.py)
    WASTE_FIELDS = get_teledeclaration_fields_all_years("GASPILLAGE")

    diagnostic_gaspillage_realise = models.BooleanField(
        blank=True, null=True, verbose_name="diagnostic sur le gaspillage réalisé"
    )
    plan_gaspillage_en_place = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="plan d'action contre le gaspillage en place",
    )
    actions_gaspillage_realisees = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=ActionsGaspillage.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions contre le gaspillage en place",
    )
    actions_gaspillage_autre = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre action contre le gaspillage alimentaire",
    )
    dons_convention = models.BooleanField(blank=True, null=True, verbose_name="propose des dons alimentaires")
    mesures_gaspillage_realisees = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="réalise des mesures de gaspillage alimentaire",
    )
    # legacy: dechets_* fields only filled for 2023 (replaced by the WasteMeasurement feature)
    dechets_total = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        blank=True,
        null=True,
        verbose_name="total des déchets alimentaires (t)",
    )
    dechets_mesure_duree = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(365)],
        verbose_name="période de mesure (jours)",
    )
    dechets_pain = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de pain kg/an",
    )
    dechets_plateau = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste plateau kg/an",
    )
    dechets_non_servis = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste en production (non servi) kg/an",
    )
    dechets_composantes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de composantes kg/an",
    )
    dons_frequence = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="fréquence de dons dons/an",
    )
    dons_quantite = make_optional_positive_decimal_field(
        verbose_name="quantité des denrées données kg/an",
    )
    dons_type_denrees = models.TextField(
        null=True,
        blank=True,
        verbose_name="type de denrées données",
    )
    commentaires_gaspillage_autre = models.TextField(
        null=True,
        blank=True,
        verbose_name="autres commentaires (gaspillage)",
    )

    class Meta:
        abstract = True
