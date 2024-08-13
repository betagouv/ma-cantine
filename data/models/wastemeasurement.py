# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.core.validators import MaxValueValidator
from django.db import models
from simple_history.models import HistoricalRecords
from .canteen import Canteen
from datetime import datetime
from django.core.exceptions import ValidationError

# from data.utils import get_diagnostic_lower_limit_year, get_diagnostic_upper_limit_year


def validate_before_today(value):
    if value > datetime.now().date():
        raise ValidationError("La date doit être dans le passé")


class WasteMeasurement(models.Model):
    class Meta:
        verbose_name = "waste_measurement"
        verbose_name_plural = "waste_measurements"

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
        verbose_name="Masse totale",
    )
    is_sorted_by_source = models.BooleanField(blank=True, null=True, verbose_name="trié en fonctionne de source ?")

    preparation_total_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="préparation - masse totale",
    )
    preparation_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="préparation - trié en fonction de comestible/non-comestible ?"
    )
    preparation_edible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="préparation - masse comestible",
    )
    preparation_inedible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="préparation - masse non-comestible",
    )

    unserved_total_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="non-servi - masse totale",
    )
    unserved_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="non-servi - trié en fonction de comestible/non-comestible ?"
    )
    unserved_edible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="non-servi - masse comestible",
    )
    unserved_inedible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="non-servi - masse non-comestible",
    )

    leftovers_total_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="restes assiette - masse totale",
    )
    leftovers_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="restes assiette - trié en fonction de comestible/non-comestible ?"
    )
    leftovers_edible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="restes assiette - masse comestible",
    )
    leftovers_inedible_mass = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="restes assiette - masse non-comestible",
    )
