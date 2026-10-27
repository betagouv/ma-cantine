from django.core.validators import MaxValueValidator
from django.db import models

from data.fields import ChoiceArrayField
from data.utils import make_optional_positive_decimal_field


class DiagnosticVoletGaspillageMixin(models.Model):
    """
    Volet gaspillage alimentaire
    """

    class WasteActions(models.TextChoices):
        INSCRIPTION = "INSCRIPTION", "Pré-inscription des convives obligatoire"
        AWARENESS = "AWARENESS", "Sensibilisation par affichage ou autre média"
        TRAINING = "TRAINING", "Formation / information du personnel de restauration"
        DISTRIBUTION = (
            "DISTRIBUTION",
            "Réorganisation de la distribution des composantes du repas",
        )
        PORTIONS = "PORTIONS", "Choix des portions (grande faim, petite faim)"
        REUSE = "REUSE", "Réutilisation des restes de préparation / surplus"

    has_waste_diagnostic = models.BooleanField(
        blank=True, null=True, verbose_name="diagnostic sur le gaspillage réalisé"
    )
    has_waste_plan = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="plan d'action contre le gaspillage en place",
    )
    waste_actions = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=WasteActions.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions contre le gaspillage en place",
    )
    other_waste_action = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre action contre le gaspillage alimentaire",
    )
    has_donation_agreement = models.BooleanField(blank=True, null=True, verbose_name="propose des dons alimentaires")
    has_waste_measures = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="réalise des mesures de gaspillage alimentaire",
    )
    # _leftovers fields no longer in use since waste measurement feature
    total_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        blank=True,
        null=True,
        verbose_name="total des déchets alimentaires (t)",
    )
    duration_leftovers_measurement = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(365)],
        verbose_name="période de mesure (jours)",
    )
    bread_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de pain kg/an",
    )
    served_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste plateau kg/an",
    )
    unserved_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste en production (non servi) kg/an",
    )
    side_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de composantes kg/an",
    )
    donation_frequency = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="fréquence de dons dons/an",
    )
    donation_quantity = make_optional_positive_decimal_field(
        verbose_name="quantité des denrées données kg/an",
    )
    donation_food_type = models.TextField(
        null=True,
        blank=True,
        verbose_name="type de denrées données",
    )
    other_waste_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="autres commentaires (gaspillage)",
    )

    class Meta:
        abstract = True
