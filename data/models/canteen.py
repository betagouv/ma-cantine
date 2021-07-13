from django.db import models
from django.contrib.auth import get_user_model
from data.department_choices import Department
from data.utils import optimize_image
from .sector import Sector
from .softdeletionmodel import SoftDeletionModel


class Canteen(SoftDeletionModel):
    class Meta:
        verbose_name = "cantine"
        verbose_name_plural = "cantines"
        ordering = ["-creation_date"]

    class ManagementType(models.TextChoices):
        DIRECT = "direct", "Directe"
        CONCEDED = "conceded", "Concédée"

    class ProductionType(models.TextChoices):
        CENTRAL = "central", "Cuisine centrale"
        ON_SITE = "site", "Cuisine-site"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    name = models.TextField(verbose_name="nom")

    city = models.TextField(null=True, blank=True, verbose_name="ville")
    city_insee_code = models.TextField(null=True, blank=True, verbose_name="Code INSEE")

    department = models.TextField(
        null=True, blank=True, choices=Department.choices, verbose_name="département"
    )
    postal_code = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="code postal"
    )
    sectors = models.ManyToManyField(
        Sector, blank=True, verbose_name="secteurs d'activité"
    )
    published = models.BooleanField(default=False, verbose_name="publié")
    data_is_public = models.BooleanField(
        default=False, verbose_name="données publiques"
    )
    managers = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="canteens",
        verbose_name="gestionnaires",
    )

    daily_meal_count = models.IntegerField(
        null=True, blank=True, verbose_name="repas par jour"
    )
    siret = models.TextField(null=True, blank=True)
    management_type = models.CharField(
        max_length=255,
        choices=ManagementType.choices,
        null=True,
        blank=True,
        verbose_name="mode de gestion",
    )
    production_type = models.CharField(
        max_length=255,
        choices=ProductionType.choices,
        null=True,
        blank=True,
        verbose_name="mode de production",
    )

    main_image = models.ImageField(
        null=True, blank=True, verbose_name="Image principale"
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        max_image_size = 1024
        if self.main_image:
            self.main_image = optimize_image(
                self.main_image, self.main_image.name, max_image_size
            )
        super(Canteen, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'Cantine "{self.name}"'
