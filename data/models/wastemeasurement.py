from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from .canteen import Canteen


def validate_before_today(value):
    if value > datetime.now().date():
        raise ValidationError("La date doit être dans le passé")


class WasteMeasurement(models.Model):
    class Meta:
        verbose_name = "évaluation du gaspillage alimentaire"
        verbose_name_plural = "évaluations du gaspillage alimentaire"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    period_start_date = models.DateField(verbose_name="date de début")
    period_end_date = models.DateField(verbose_name="date de fin", validators=[validate_before_today])
    meal_count = models.IntegerField(verbose_name="couverts sur la période", null=True, blank=True)

    total_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Masse totale (kg)",
    )
    is_sorted_by_source = models.BooleanField(blank=True, null=True, verbose_name="trié en fonctionne de source ?")

    preparation_total_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="préparation - masse totale (kg)",
    )
    preparation_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="préparation - trié en fonction de comestible/non-comestible ?"
    )
    preparation_edible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="préparation - masse comestible (kg)",
    )
    preparation_inedible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="préparation - masse non-comestible (kg)",
    )

    unserved_total_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="non-servi - masse totale (kg)",
    )
    unserved_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="non-servi - trié en fonction de comestible/non-comestible ?"
    )
    unserved_edible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="non-servi - masse comestible (kg)",
    )
    unserved_inedible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="non-servi - masse non-comestible (kg)",
    )

    leftovers_total_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="restes assiette - masse totale (kg)",
    )
    leftovers_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="restes assiette - trié en fonction de comestible/non-comestible ?"
    )
    leftovers_edible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="restes assiette - masse comestible (kg)",
    )
    leftovers_inedible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="restes assiette - masse non-comestible (kg)",
    )

    @property
    def days_in_period(self):
        # + 1 because python is exclusive but period dates are inclusive
        return (self.period_end_date - self.period_start_date).days + 1

    @property
    def total_yearly_waste_estimation(self):
        canteen_yearly_meal_count = self.canteen.yearly_meal_count
        has_total_mass = self.total_mass and self.total_mass >= 0
        if not canteen_yearly_meal_count or not self.meal_count or not has_total_mass:
            return None
        return self.total_mass / self.meal_count * canteen_yearly_meal_count

    def clean(self):
        self.validate_dates()
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def validate_dates(self):
        start_date = self.period_start_date
        end_date = self.period_end_date
        start_date_changed = start_date is not None
        end_date_changed = end_date is not None

        # if this is an update, check which date(s) have been changed so that we can raise relevant errors
        if self.id:
            original_object = WasteMeasurement.objects.get(id=self.id)
            start_date_changed = original_object.period_start_date != start_date
            end_date_changed = original_object.period_end_date != end_date

        WasteMeasurement._validate_start_before_end(start_date, end_date, start_date_changed, end_date_changed)

        other_measurements = WasteMeasurement.objects.filter(canteen=self.canteen)
        if self.id:
            other_measurements = other_measurements.exclude(id=self.id)

        if start_date_changed:
            WasteMeasurement._validate_start_not_in_other_period(other_measurements, start_date)

        if end_date_changed:
            WasteMeasurement._validate_end_not_in_other_period(other_measurements, end_date)

        if start_date_changed or end_date_changed:
            WasteMeasurement._validate_period_not_in_other_period(other_measurements, start_date, end_date)

    def _validate_start_before_end(start_date, end_date, start_date_changed, end_date_changed):
        if start_date_changed and start_date >= end_date:
            raise ValidationError({"period_start_date": ["La date de début doit être avant la date de fin"]})
        elif end_date_changed and end_date <= start_date:
            raise ValidationError({"period_end_date": ["La date de fin doit être après la date de début"]})

    def _validate_start_not_in_other_period(other_measurements, start_date):
        measurement_containing_start_date = other_measurements.filter(
            period_start_date__lte=start_date, period_end_date__gte=start_date
        )
        if measurement_containing_start_date.exists():
            wm = measurement_containing_start_date.first()
            raise ValidationError(
                {
                    "period_start_date": [
                        f"Il existe déjà une autre évaluation pour la période {wm.period_start_date} à {wm.period_end_date}. Veuillez modifier la évaluation existante ou corriger la date de début."
                    ]
                }
            )

    def _validate_end_not_in_other_period(other_measurements, end_date):
        measurement_containing_end_date = other_measurements.filter(
            period_start_date__lte=end_date, period_end_date__gte=end_date
        )
        if measurement_containing_end_date.exists():
            wm = measurement_containing_end_date.first()
            raise ValidationError(
                {
                    "period_end_date": [
                        f"Il existe déjà une autre évaluation pour la période {wm.period_start_date} à {wm.period_end_date}. Veuillez modifier la évaluation existante ou corriger la date de fin."
                    ]
                }
            )

    def _validate_period_not_in_other_period(other_measurements, start_date, end_date):
        measurements_within_period = other_measurements.filter(
            period_start_date__gte=start_date, period_end_date__lte=end_date
        )
        if measurements_within_period.exists():
            wm_count = measurements_within_period.count()
            measure_count_str = "une autre évaluation" if wm_count == 1 else f"{wm_count} autres évaluations"
            raise ValidationError(
                f"Il existe déjà {measure_count_str} dans la période {start_date} à {end_date}. Veuillez modifier les évaluations existantes ou corriger les dates de la période."
            )
