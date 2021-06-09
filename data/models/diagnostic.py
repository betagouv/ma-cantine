from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from data.fields import ChoiceArrayField
from .canteen import Canteen


class Diagnostic(models.Model):
    class Meta:
        verbose_name = "diagnostic"
        verbose_name_plural = "diagnostics"

    class MenuFrequency(models.TextChoices):
        LOW = "LOW", "Moins d'une fois par semaine"
        MID = "MID", "Une fois par semaine"
        HIGH = "HIGH", "Plus d'une fois par semaine"

    class MenuType(models.TextChoices):
        UNIQUE = "UNIQUE", "Un menu végétarien unique"
        SEVERAL = "SEVERAL", "Plusieurs menus végétariens alternatifs"
        ALTERNATIVES = (
            "ALTERNATIVES",
            "Un menu végétarien alternatif à d'autres menus non-végétariens",
        )

    class CommunicationType(models.TextChoices):
        EMAIL = "EMAIL", "Envoi d'e-mail aux convives ou à leurs représentants"
        DISPLAY = "DISPLAY", "Par affichage sur le lieu de restauration"
        WEBSITE = "WEBSITE", "Sur site internet ou intranet (mairie, cantine)"
        OTHER = "OTHER", "Autres moyens d'affichage et de communication électronique"

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

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    year = models.IntegerField(
        validators=[MinValueValidator(1970), MaxValueValidator(2100)],
        null=True,
        blank=True,
    )

    # Product origin
    value_bio_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Bio - Valeur annuelle HT",
    )
    value_fair_trade_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Commerce équitable - Valeur annuelle HT",
    )
    value_sustainable_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits durables (hors bio) - Valeur annuelle HT",
    )
    value_total_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valeur totale annuelle HT",
    )

    # Food waste
    has_waste_diagnostic = models.BooleanField(
        null=True, verbose_name="diagnostic sur le gaspillage réalisé"
    )
    has_waste_plan = models.BooleanField(
        null=True, verbose_name="plan d'action contre le gaspillage en place"
    )
    waste_actions = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=WasteActions.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions contre le gaspillage en place",
    )
    has_donation_agreement = models.BooleanField(
        null=True, verbose_name="propose des dons alimentaires"
    )

    # Vegetarian menus
    has_diversification_plan = models.BooleanField(
        null=True, verbose_name="plan de diversification en place"
    )
    vegetarian_weekly_recurrence = models.CharField(
        max_length=255,
        choices=MenuFrequency.choices,
        null=True,
        blank=True,
        verbose_name="Menus végétariens par semaine",
    )
    vegetarian_menu_type = models.CharField(
        max_length=255,
        choices=MenuType.choices,
        blank=True,
        null=True,
        verbose_name="Menu végétarien proposé",
    )

    # Plastic replacement
    cooking_plastic_substituted = models.BooleanField(
        null=True, verbose_name="contenants de cuisson en plastique remplacés"
    )
    serving_plastic_substituted = models.BooleanField(
        null=True, verbose_name="contenants de service en plastique remplacés"
    )
    plastic_bottles_substituted = models.BooleanField(
        null=True, verbose_name="bouteilles en plastique remplacées"
    )
    plastic_tableware_substituted = models.BooleanField(
        null=True, verbose_name="ustensils en plastique remplacés"
    )

    # Information and communication
    communication_supports = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=CommunicationType.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Communication utilisée",
    )
    communication_support_url = models.URLField(
        blank=True, null=True, verbose_name="Lien de communication"
    )
    communicates_on_food_plan = models.BooleanField(
        null=True, verbose_name="Communique sur le plan alimentaire"
    )

    def __str__(self):
        return f"Diagnostic pour {self.canteen.name} ({self.year})"
