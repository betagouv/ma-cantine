from django.db import models

from data.fields import ChoiceArrayField
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all_years


class DiagnosticVoletDiversificationMixin(models.Model):
    """
    Volet "Diversification des sources de protéines et menus végétariens"
    """

    class ServiceType(models.TextChoices):
        MENU_UNIQUE = "MENU_UNIQUE", "Menu unique"
        CHOIX_MULTIPLE_LIBRE_SERVICE = "CHOIX_MULTIPLE_LIBRE_SERVICE", "Choix multiple en libre-service"
        CHOIX_MULTIPLE_RESERVATION = (
            "CHOIX_MULTIPLE_RESERVATION",
            "Choix multiple avec réservation à l’avance au jour le jour",
        )

    class MenuVegetarienFrequence(models.TextChoices):
        JAMAIS = "JAMAIS", "Jamais"
        MOINS_HEBDO = "MOINS_HEBDO", "Moins d'une fois par semaine"
        HEBDO = "HEBDO", "Une fois par semaine"
        PLUS_HEBDO = "PLUS_HEBDO", "Plus d'une fois par semaine"
        QUOTIDIEN = "QUOTIDIEN", "De façon quotidienne"

    class MenuVegetarienType(models.TextChoices):  # legacy
        UNIQUE = "UNIQUE", "Un menu végétarien en plat unique, sans choix"
        SEVERAL = (
            "SEVERAL",
            "Un menu végétarien composé de plusieurs choix de plats végétariens",
        )
        ALTERNATIVES = (
            "ALTERNATIVES",
            "Un menu végétarien au choix, en plus d'autres plats non végétariens",
        )

    class PlanDiversificationActions(models.TextChoices):
        PLATS_PRODUITS = (
            "PLATS_PRODUITS",
            "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
        )
        PRESENTATION = (
            "PRESENTATION",
            "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
        )
        MENU = (
            "MENU",
            "Agir sur la manière dont les menus sont conçus ces plats en soulignant leurs attributs positifs",
        )
        PROMOTION = (
            "PROMOTION",
            "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
        )
        FORMATION = (
            "FORMATION",
            "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
        )

    class MenuVegetarienBase(models.TextChoices):
        CEREALES_LEGUMINEUSES = "CEREALES_LEGUMINEUSES", "De céréales et/ou les légumes secs (hors soja)"
        SOJA = "SOJA", "De soja"
        FROMAGE = "FROMAGE", "De fromage"
        OEUFS = "OEUFS", "D’œufs"
        PLATS_PRETS_A_L_EMPLOI = "PLATS_PRETS_A_L_EMPLOI", "Plats prêts à l'emploi"

    # all the fields of the volet (all years, see diagnostic_teledeclaration_fields.py)
    DIVERSIFICATION_FIELDS = get_teledeclaration_fields_all_years("DIVERSIFICATION")

    plan_diversification_en_place = models.BooleanField(
        blank=True, null=True, verbose_name="plan de diversification en place"
    )
    plan_diversification_actions = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=PlanDiversificationActions.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions inclus dans le plan de diversification des protéines",
    )
    service_type = models.CharField(
        max_length=255,
        choices=ServiceType.choices,
        null=True,
        blank=True,
        verbose_name="type de service",
    )
    menu_vegetarien_frequence = models.CharField(
        max_length=255,
        choices=MenuVegetarienFrequence.choices,
        null=True,
        blank=True,
        verbose_name="Menus végétariens par semaine",
    )
    menu_vegetarien_type = models.CharField(  # legacy
        max_length=255,
        choices=MenuVegetarienType.choices,
        blank=True,
        null=True,
        verbose_name="Menu végétarien proposé",
    )
    menu_vegetarien_bases = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=MenuVegetarienBase.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="bases de menu végétarien",
    )

    class Meta:
        abstract = True
