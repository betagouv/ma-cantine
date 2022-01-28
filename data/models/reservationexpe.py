from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .canteen import Canteen


class ReservationExpe(models.Model):
    class Meta:
        verbose_name = "expérimentation réservation"
        verbose_name_plural = "expérimentations réservation"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, verbose_name="cantine")

    has_reservation_system = models.BooleanField(
        default=False, verbose_name="a déjà mis en place une solution de réservation de repas"
    )
    reservation_system_start_date = models.DateField(
        null=True, blank=True, verbose_name="date de début du système de réservation"
    )
    experimentation_start_date = models.DateField(
        null=True, blank=True, verbose_name="date de début d'expérimentation"
    )
    reservation_system_description = models.TextField(
        null=True, blank=True, verbose_name="description du système de réservation"
    )
    publicise_method = models.TextField(null=True, blank=True, verbose_name="méthode de communication aux convives")
    has_leader = models.BooleanField(default=False, verbose_name="Un responsable chargé du pilotage a été désigné")
    leader_first_name = models.CharField(
        null=True, blank=True, max_length=100, verbose_name="prénom du responsable d'expé"
    )
    leader_last_name = models.CharField(
        null=True, blank=True, max_length=100, verbose_name="nom du responsable d'expé"
    )
    leader_email = models.EmailField(null=True, blank=True, verbose_name="Email du responsable")
    has_regulations = models.BooleanField(
        default=False, verbose_name="Un réglement à destination des convives a été rédigé"
    )
    has_committee = models.BooleanField(default=False, verbose_name="Un comité de pilotage du projet a été défini")

    avg_weight_not_served_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des excédents présentés aux convives et non servis (g/ convive) sur 20 déjeuners successifs",
    )
    avg_weight_leftover_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des restes des assiettes exprimées (g/convive) sur 20 déjeuners successifs",
    )
    ratio_edible_non_edible_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Ratio de la part non comestible (g) rapportée à la part comestible (g)",
    )
    avg_weight_preparation_leftover_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des excédents de préparation (g/convive)",
    )
    avg_weight_bread_leftover_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des pains jetés sur 20 déjeuners successifs (g/convive)",
    )
    avg_attendance_from_evaluation_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Nombre moyen d'usagers à partir de l'évaluation",
    )
    solution_use_rate_t0 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Taux d’utilisation de la solution de réservation",
    )
    satisfaction_t0 = models.IntegerField(
        null=True, blank=True, verbose_name="Satisfaction", validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comments_t0 = models.TextField(null=True, blank=True, verbose_name="Commentaires")

    # T1
    avg_weight_not_served_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des excédents présentés aux convives et non servis (g/ convive) sur 20 déjeuners successifs",
    )
    avg_weight_leftover_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des restes des assiettes exprimées (g/convive) sur 20 déjeuners successifs",
    )
    ratio_edible_non_edible_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Ratio de la part non comestible (g) rapportée à la part comestible (g)",
    )
    avg_weight_preparation_leftover_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des excédents de préparation (g/convive)",
    )
    avg_weight_bread_leftover_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des pains jetés sur 20 déjeuners successifs (g/convive)",
    )
    avg_attendance_from_evaluation_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Nombre moyen d'usagers à partir de l'évaluation",
    )
    solution_use_rate_t1 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Taux d’utilisation de la solution de réservation",
    )
    satisfaction_t1 = models.IntegerField(
        null=True, blank=True, verbose_name="Satisfaction", validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comments_t1 = models.TextField(null=True, blank=True, verbose_name="Commentaires")

    # T2
    avg_weight_not_served_t2 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des excédents présentés aux convives et non servis (g/ convive) sur 20 déjeuners successifs",
    )
    avg_weight_leftover_t2 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des restes des assiettes exprimées (g/convive) sur 20 déjeuners successifs",
    )
    ratio_edible_non_edible_t2 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Ratio de la part non comestible (g) rapportée à la part comestible (g)",
    )
    avg_weight_preparation_leftover_t2 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des excédents de préparation (g/convive)",
    )
    avg_weight_bread_leftover_t2 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Moyenne des pesées des pains jetés sur 20 déjeuners successifs (g/convive)",
    )
    avg_attendance_from_evaluation_t2 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Nombre moyen d'usagers à partir de l'évaluation",
    )
    solution_use_rate_t2 = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Taux d’utilisation de la solution de réservation",
    )
    satisfaction_t2 = models.IntegerField(
        null=True, blank=True, verbose_name="Satisfaction", validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comments_t2 = models.TextField(null=True, blank=True, verbose_name="Commentaires")

    # T2 only questions
    system_cost = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Coût de la solution de réservation sur 3 ans",
    )
    participation_cost = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Coûts liés à la participation à l'expérimentation sur 3 ans",
    )
    participation_cost_details = models.TextField(
        null=True, blank=True, verbose_name="Détails des coûts liés à la participation à l'expérimentation"
    )
    money_saved = models.DecimalField(
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Gains générés par l'évitement du gaspillage laimentaire en euros sur 3 ans",
    )
