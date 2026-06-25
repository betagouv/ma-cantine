from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from oauth2_provider.models import Application as OAuth2Application
from simple_history.models import HistoricalRecords

from common.utils import utils as utils_utils
from data.models.creation_source import CreationSource
from data.utils import make_optional_positive_decimal_field
from data.validators import wastemeasurement as wastemeasurement_validators

from data.models import Canteen, AuthenticationMethodHistoricalRecords


class WasteMeasurement(models.Model):
    CREATION_META_FIELDS = [
        "creation_date",
        "modification_date",
        "creation_user",
        "creation_source",
        "creation_source_api_oauth2_application",
    ]

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    period_start_date = models.DateField(verbose_name="date de début")
    period_end_date = models.DateField(verbose_name="date de fin")
    meal_count = models.IntegerField(verbose_name="couverts sur la période", null=True, blank=True)

    total_mass = make_optional_positive_decimal_field(
        verbose_name="Masse totale (kg)",
    )
    is_sorted_by_source = models.BooleanField(blank=True, null=True, verbose_name="trié en fonctionne de source ?")

    preparation_total_mass = make_optional_positive_decimal_field(
        verbose_name="préparation - masse totale (kg)",
    )
    preparation_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="préparation - trié en fonction de comestible/non-comestible ?"
    )
    preparation_edible_mass = make_optional_positive_decimal_field(
        verbose_name="préparation - masse comestible (kg)",
    )
    preparation_inedible_mass = make_optional_positive_decimal_field(
        verbose_name="préparation - masse non-comestible (kg)",
    )

    unserved_total_mass = make_optional_positive_decimal_field(
        verbose_name="non-servi - masse totale (kg)",
    )
    unserved_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="non-servi - trié en fonction de comestible/non-comestible ?"
    )
    unserved_edible_mass = make_optional_positive_decimal_field(
        verbose_name="non-servi - masse comestible (kg)",
    )
    unserved_inedible_mass = make_optional_positive_decimal_field(
        verbose_name="non-servi - masse non-comestible (kg)",
    )

    leftovers_total_mass = make_optional_positive_decimal_field(
        verbose_name="restes assiette - masse totale (kg)",
    )
    leftovers_is_sorted = models.BooleanField(
        blank=True, null=True, verbose_name="restes assiette - trié en fonction de comestible/non-comestible ?"
    )
    leftovers_edible_mass = make_optional_positive_decimal_field(
        verbose_name="restes assiette - masse comestible (kg)",
    )
    leftovers_inedible_mass = make_optional_positive_decimal_field(
        verbose_name="restes assiette - masse non-comestible (kg)",
    )

    creation_user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="waste_measurements_created",
        verbose_name="utilisateur qui a créé l'évaluation du gaspillage alimentaire",
    )
    creation_source = models.CharField(
        max_length=255,
        choices=CreationSource.choices,
        blank=True,
        null=True,
        verbose_name="Source de création de l'évaluation du gaspillage alimentaire",
    )
    creation_source_api_oauth2_application = models.ForeignKey(
        OAuth2Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="waste_measurements_created",
        verbose_name="app OAuth2 (API) qui a créé l'évaluation du gaspillage alimentaire",
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(bases=[AuthenticationMethodHistoricalRecords])

    class Meta:
        verbose_name = "évaluation du gaspillage alimentaire"
        verbose_name_plural = "évaluations du gaspillage alimentaire"

    def clean(self):
        validation_errors = utils_utils.merge_validation_errors(
            wastemeasurement_validators.validate_dates(self),
        )
        if validation_errors:
            raise ValidationError(validation_errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
