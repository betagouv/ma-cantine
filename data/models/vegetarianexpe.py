from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from data.fields import ChoiceArrayField
from .canteen import Canteen


class VegetarianExpe(models.Model):
    class Meta:
        verbose_name = "expérimentation repas végétariens quotidiens"
        verbose_name_plural = "expérimentations repas végétariens quotidiens"

    class WasteEvolution(models.TextChoices):
        HIGHER = "higher", "Oui, il y a plus de gaspillage"
        LOWER = "lower", "Non, il y a moins de gaspillage"
        SAME = "same", "Pas de différence notable"

    class CostEvolution(models.TextChoices):
        HIGHER = "higher", "Le coût a augmenté"
        LOWER = "lower", "Le coût a diminué"
        SAME = "same", "Pas de différence notable"

    class AttendanceEvolution(models.TextChoices):
        HIGHER = "higher", "La fréquentation a augmenté"
        LOWER = "lower", "La fréquentation a diminué"
        SAME = "same", "Pas de différence notable"

    class SatisfactionReasons(models.TextChoices):
        CHOICE = "choice", "Liberté de choix (régime, culte...)"
        TASTE = "taste", "Goût et texture"
        NOVELTY = "novelty", "Nouveauté"
        VARIETY = "variety", "Variété des recettes"
        IGNORANCE = "ignorance", "Méconnaissance"
        REJECT = "reject", "Opposition de principe"
        HEALTH = "health", "Impact sur la santé"
        ENVIRONMENT = "environment", "Impact sur l'environnement"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, verbose_name="cantine")

    has_daily_vegetarian_offer = models.BooleanField(
        default=False, verbose_name="a déjà mis en place l'option végétarienne quotidienne"
    )

    # Start Date
    daily_vegetarian_offer_start_date = models.DateField(
        null=True, blank=True, verbose_name="date de début de l'offre végétarienne quotidienne"
    )
    experimentation_start_date = models.DateField(
        null=True, blank=True, verbose_name="date de début d'expérimentation"
    )

    # ------------- T0

    vegetarian_menu_percentage_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Pourcentage de menus végétariens servis par rapport aux autres menus",
    )

    # Plate composition
    eggs_composition_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base d'œufs (sur 20 repas)",
    )
    cheese_composition_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base de fromage (sur 20 repas)",
    )
    soy_composition_home_made_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets fait maison à base de soja (sur 20 repas)",
    )
    soy_composition_ready_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets prêt à l’emploi à base de soja (sur 20 repas)",
    )
    soyless_composition_home_made_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets fait maison sans soja (sur 20 repas)",
    )
    soyless_composition_ready_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets prêt à l’emploi sans soja (sur 20 repas)",
    )
    cereal_legume_composition_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base de céréales, légumineuses et légumes (sur 20 repas)",
    )

    # Waste
    waste_evolution_t0 = models.CharField(
        max_length=255,
        choices=WasteEvolution.choices,
        null=True,
        blank=True,
        verbose_name="Évolution ressentie du gaspillage",
    )
    waste_evolution_percentage_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Évolution du gaspillage suite au menu végétarien quotidien",
    )

    waste_vegetarian_not_served_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus végétariens : Moyenne des pesées des excédents présentés aux convives et non servis",
    )
    waste_vegetarian_components_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus végétariens : Moyenne des pesées des restes des assiettes",
    )
    waste_non_vegetarian_not_served_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus non-végétariens : Moyenne des pesées des excédents présentés aux convives et non servis",
    )
    waste_non_vegetarian_components_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus non-végétariens : Moyenne des pesées des restes des assiettes",
    )

    # Attendance
    attendance_evolution_t0 = models.CharField(
        max_length=255,
        choices=AttendanceEvolution.choices,
        null=True,
        blank=True,
        verbose_name="Évolution ressentie de la fréquentation",
    )
    attendance_evolution_percentage_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Évolution de la fréquentation suite au menu végétarien quotidien",
    )

    # Cost
    vegetarian_cost_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Coût moyen du repas végétarien (€ / assiette)",
    )
    non_vegetarian_cost_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Coût moyen du repas non-végétarien (€ / assiette)",
    )
    cost_evolution_t0 = models.CharField(
        max_length=255,
        choices=CostEvolution.choices,
        null=True,
        blank=True,
        verbose_name="Évolution ressentie du coût",
    )
    cost_evolution_percentage_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Évolution du coût en pourcentage",
    )

    # Satisfaction
    satisfaction_guests_t0 = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Satisfaction moyenne des convives",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    satisfaction_guests_reasons_t0 = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=SatisfactionReasons.choices),
        null=True,
        blank=True,
        verbose_name="Principales raisons évoquées par les convives",
    )

    satisfaction_staff_t0 = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Satisfaction moyenne du personnel",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    satisfaction_staff_reasons_t0 = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=SatisfactionReasons.choices),
        null=True,
        blank=True,
        verbose_name="Principales raisons évoquées par le personnel",
    )

    # Recipee support

    has_used_recipee_documents_t0 = models.BooleanField(
        null=True, blank=True, verbose_name="A utilisé un livret de recettes végétariennes (CNRC ou autres organismes)"
    )

    # Training

    training_t0 = models.BooleanField(
        null=True, blank=True, verbose_name="Formation spécifique des cuisiniers ou gestionnaires"
    )

    # ------------- T1

    vegetarian_menu_percentage_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Pourcentage de menus végétariens servis par rapport aux autres menus",
    )

    # Plate composition
    eggs_composition_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base d'œufs (sur 20 repas)",
    )
    cheese_composition_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base de fromage (sur 20 repas)",
    )
    soy_composition_home_made_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets fait maison à base de soja (sur 20 repas)",
    )
    soy_composition_ready_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets prêt à l’emploi à base de soja (sur 20 repas)",
    )
    soyless_composition_home_made_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets fait maison sans soja (sur 20 repas)",
    )
    soyless_composition_ready_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas basés sur galettes/boulettes/nuggets prêt à l’emploi sans soja (sur 20 repas)",
    )
    cereal_legume_composition_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base de céréales, légumineuses et légumes (sur 20 repas)",
    )

    # Waste
    waste_evolution_t1 = models.CharField(
        max_length=255,
        choices=WasteEvolution.choices,
        null=True,
        blank=True,
        verbose_name="Évolution ressentie du gaspillage",
    )
    waste_evolution_percentage_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Évolution du gaspillage suite au menu végétarien quotidien",
    )

    waste_vegetarian_not_served_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus végétariens : Moyenne des pesées des excédents présentés aux convives et non servis",
    )
    waste_vegetarian_components_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus végétariens : Moyenne des pesées des restes des assiettes",
    )
    waste_non_vegetarian_not_served_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus non-végétariens : Moyenne des pesées des excédents présentés aux convives et non servis",
    )
    waste_non_vegetarian_components_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Menus non-végétariens : Moyenne des pesées des restes des assiettes",
    )

    # Attendance
    attendance_evolution_t1 = models.CharField(
        max_length=255,
        choices=AttendanceEvolution.choices,
        null=True,
        blank=True,
        verbose_name="Évolution ressentie de la fréquentation",
    )
    attendance_evolution_percentage_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Évolution de la fréquentation suite au menu végétarien quotidien",
    )

    # Cost
    vegetarian_cost_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Coût moyen du repas végétarien (€ / assiette)",
    )
    non_vegetarian_cost_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Coût moyen du repas non-végétarien (€ / assiette)",
    )
    cost_evolution_t1 = models.CharField(
        max_length=255,
        choices=CostEvolution.choices,
        null=True,
        blank=True,
        verbose_name="Évolution ressentie du coût",
    )
    cost_evolution_percentage_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Évolution du coût en pourcentage",
    )

    # Satisfaction
    satisfaction_guests_t1 = models.IntegerField(
        null=True, blank=True, verbose_name="Satisfaction", validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    satisfaction_guests_reasons_t1 = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=SatisfactionReasons.choices),
        null=True,
        blank=True,
        verbose_name="Principales raisons évoquées par les convives",
    )

    satisfaction_staff_t1 = models.IntegerField(
        null=True, blank=True, verbose_name="Satisfaction", validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    satisfaction_staff_reasons_t1 = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=SatisfactionReasons.choices),
        null=True,
        blank=True,
        verbose_name="Principales raisons évoquées par le personnel",
    )

    # Recipee support

    has_used_recipee_documents_t1 = models.BooleanField(
        null=True, blank=True, verbose_name="A utilisé un livret de recettes végétariennes (CNRC ou autres organismes)"
    )

    # Training

    training_t1 = models.BooleanField(
        null=True, blank=True, verbose_name="Formation spécifique des cuisiniers ou gestionnaires"
    )
