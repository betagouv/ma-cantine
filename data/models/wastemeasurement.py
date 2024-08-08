# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.core.validators import MaxValueValidator
from django.db import models
from simple_history.models import HistoricalRecords
from .canteen import Canteen

# from data.utils import get_diagnostic_lower_limit_year, get_diagnostic_upper_limit_year


class WasteMeasurement(models.Model):
    class Meta:
        verbose_name = "waste_measurement"
        verbose_name_plural = "waste_measurements"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    # period_start_date (date)
    # period_end_date (date)
    # meal_count (integer)

    # total_mass (decimal)
    # is_sorted_by_source (boolean)

    # preparation_total_mass (decimal)
    # preparation_is_sorted (boolean)
    # preparation_edible_mass (decimal)
    # preparation_inedible_mass (decimal)

    # unserved_total_mass (decimal)
    # unserved_is_sorted (boolean)
    # unserved_edible_mass (decimal)
    # unserved_inedible_mass (decimal)

    # leftovers_total_mass (decimal)
    # leftovers_is_sorted (boolean)
    # leftovers_edible_mass (decimal)
    # leftovers_inedible_mass (decimal)
