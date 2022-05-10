from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from data.fields import ChoiceArrayField
from .canteen import Canteen


class VegetarianExpe(models.Model):
    class Meta:
        verbose_name = "expérimentation repas végétariens quotidiens"
        verbose_name_plural = "expérimentations repas végétariens quotidiens"

    class MenuOptions(models.TextChoices):
        UNIQUE = "unique", "Un menu unique pour tous les convives"
        MULTIPLE = "multiple", "Une offre à choix multiples"

    class ReservationOptions(models.TextChoices):
        OPEN = "open", "Est proposée chaque jour aux convives librement"
        RESERVATION_NEEDED = "reservation_needed", "Fait l'objet d'une préinscription en amont"

    class WasteEvolutionToDate(models.TextChoices):
        HIGHER = "higher", "Oui, le gaspillage des plats végétariens a augmenté depuis la mise en place"
        LOWER = "lower", "Oui, le gaspillage des plats végétariens a diminué depuis la mise en place"
        SAME = "same", "Non, le gaspillage des plats végétariens n'a pas évolué"

    class WasteEvolution(models.TextChoices):
        HIGHER = "higher", "Oui, il y a plus de gaspillage"
        LOWER = "lower", "Non, il y a moins de gaspillage"
        SAME = "same", "Pas de différence notable"

    class CostEvolution(models.TextChoices):
        HIGHER = "higher", "Le tarif par repas a augmenté"
        LOWER = "lower", "Le tarif par repas a diminué"
        SAME = "same", "Le tarif par repas n’a pas changé"

    class AttendanceEvolution(models.TextChoices):
        HIGHER = "higher", "La fréquentation a augmenté"
        LOWER = "lower", "La fréquentation a diminué"
        SAME = "same", "Pas de différence notable"

    class SatisfactionReasonsStaff(models.TextChoices):
        CHOICE = "choice", "Liberté de choix (régime, culte...)"
        TASTE = "taste", "Goût et texture"
        NOVELTY = "novelty", "Nouveauté"
        VARIETY = "variety", "Variété des recettes"
        IGNORANCE = "ignorance", "Méconnaissance"
        REJECT = "reject", "Opposition de principe"
        HEALTH = "health", "Impact sur la santé"
        ENVIRONMENT = "environment", "Impact sur l'environnement"
        NO_EQUIPMENT = "no_equipment", "Manque de matériel adapté"

    class SatisfactionReasonsGuests(models.TextChoices):
        CHOICE = "choice", "Liberté de choix (régime, culte...)"
        TASTE = "taste", "Goût et texture"
        NOVELTY = "novelty", "Nouveauté"
        VARIETY = "variety", "Variété des recettes"
        IGNORANCE = "ignorance", "Méconnaissance"
        REJECT = "reject", "Opposition de principe"
        HEALTH = "health", "Impact sur la santé"
        ENVIRONMENT = "environment", "Impact sur l'environnement"
        DIGESTION = "digestion", "Problèmes de digestion"

    class VegetarianCost(models.TextChoices):
        HIGHER = "higher", "Plus que cher que les plats non-végétariens"
        LOWER = "lower", "Moins cher que les plats non-végétariens"
        SAME = "same", "Equivalent aux plats non-végétariens"

    class DifficultiesOptions(models.TextChoices):
        FORMATION = "formation", "Difficultés d'accès à la formation"
        APPRO = "appro", "Difficultés d'approvisionnement"
        RECIPES = "recipes", "Manque de recettes"
        COST = "cost", "Surcoût des produits"
        CLIENTS = "clients", "Réaction des convives"
        OVERWORK = "overwork", "Surcharge de travail pour le personnel"
        OTHER = "other", "Autre"

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

    menu_type_before_xp = models.CharField(
        max_length=255,
        choices=MenuOptions.choices,
        null=True,
        blank=True,
        verbose_name="Avant la mise en place de l’expérimentation, mon établissement propose chaque jour :",
    )

    vege_menu_reservation = models.CharField(
        max_length=255,
        choices=ReservationOptions.choices,
        null=True,
        blank=True,
        verbose_name="Concernant l'inscription, l’option végétarienne quotidienne :",
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
    starch_legume_composition_t0 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base de féculents, légumes et sauces (sur 20 repas)",
    )

    wholegrain_cereal_percentage_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Parmi les plats à base de céréales, pourcentage des céréales complètes et semi-complètes",
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

    # Waste evolution from start to date, T0 only
    waste_evolution_start_to_date_t0 = models.CharField(
        max_length=255,
        choices=WasteEvolutionToDate.choices,
        null=True,
        blank=True,
        verbose_name="Évolution du gaspillage avec l'option végétarienne entre le moment de sa mise en place et aujourd'hui",
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
    vegetarian_cost_qualitative_t0 = models.CharField(
        max_length=255,
        choices=VegetarianCost.choices,
        null=True,
        blank=True,
        verbose_name="En moyenne, ressenti qualitative du coût matière des plats végétariens",
    )

    cost_savings_reinvested_t0 = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Les économies réalisées ont été réinvesties pour augmenter la part de produits durables et de qualité",
    )

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
    cost_per_meal_vg_t0 = models.BooleanField(
        null=True, blank=True, verbose_name="Le tarif par repas est moins cher pour l’option végétarienne"
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
        base_field=models.CharField(max_length=255, choices=SatisfactionReasonsGuests.choices),
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
        base_field=models.CharField(max_length=255, choices=SatisfactionReasonsStaff.choices),
        null=True,
        blank=True,
        verbose_name="Principales raisons évoquées par le personnel",
    )

    # Recipe support

    has_used_recipe_documents_t0 = models.BooleanField(
        null=True, blank=True, verbose_name="A utilisé un livret de recettes végétariennes (CNRC ou autres organismes)"
    )
    recipe_document_t0 = models.TextField(null=True, blank=True, verbose_name="Livret de recette utilisé")

    # Training

    training_t0 = models.BooleanField(
        null=True, blank=True, verbose_name="Formation spécifique des cuisiniers ou gestionnaires"
    )
    training_type_t0 = models.TextField(null=True, blank=True, verbose_name="Type de formation")

    # Difficulties

    difficulties_daily_option_t0 = models.CharField(
        max_length=255,
        choices=DifficultiesOptions.choices,
        null=True,
        blank=True,
        verbose_name="Principaux freins rencontrés à la mise en place de l’option végétarienne quotidienne",
    )

    difficulties_daily_option_details_t0 = models.TextField(
        null=True,
        blank=True,
        verbose_name="Precision sur les freins rencontrés à la mise en place de l’option végétarienne quotidienne",
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
    starch_legume_composition_t1 = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Repas à base de féculents, légumes et sauces (sur 20 repas)",
    )

    wholegrain_cereal_percentage_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Parmi les plats à base de céréales, pourcentage des céréales complètes et semi-complètes",
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
    vegetarian_cost_qualitative_t1 = models.CharField(
        max_length=255,
        choices=VegetarianCost.choices,
        null=True,
        blank=True,
        verbose_name="En moyenne, ressenti qualitative du coût matière des plats végétariens",
    )
    cost_savings_reinvested_t1 = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Les économies réalisées ont été réinvesties pour augmenter la part de produits durables et de qualité",
    )
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
    cost_per_meal_vg_t1 = models.BooleanField(
        null=True, blank=True, verbose_name="Le tarif par repas est moins cher pour l’option végétarienne"
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
        base_field=models.CharField(max_length=255, choices=SatisfactionReasonsGuests.choices),
        null=True,
        blank=True,
        verbose_name="Principales raisons évoquées par les convives",
    )

    satisfaction_staff_t1 = models.IntegerField(
        null=True, blank=True, verbose_name="Satisfaction", validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    satisfaction_staff_reasons_t1 = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=SatisfactionReasonsStaff.choices),
        null=True,
        blank=True,
        verbose_name="Principales raisons évoquées par le personnel",
    )

    # Recipe support

    has_used_recipe_documents_t1 = models.BooleanField(
        null=True, blank=True, verbose_name="A utilisé un livret de recettes végétariennes (CNRC ou autres organismes)"
    )
    recipe_document_t1 = models.TextField(null=True, blank=True, verbose_name="Livret de recette utilisé")

    # Training

    training_t1 = models.BooleanField(
        null=True, blank=True, verbose_name="Formation spécifique des cuisiniers ou gestionnaires"
    )
    training_type_t1 = models.TextField(null=True, blank=True, verbose_name="Type de formation")

    # Difficulties

    difficulties_daily_option_t1 = models.CharField(
        max_length=255,
        choices=DifficultiesOptions.choices,
        null=True,
        blank=True,
        verbose_name="Principaux freins rencontrés à la mise en place de l’option végétarienne quotidienne",
    )

    difficulties_daily_option_details_t1 = models.TextField(
        null=True,
        blank=True,
        verbose_name="Precision sur les freins rencontrés à la mise en place de l’option végétarienne quotidienne",
    )
