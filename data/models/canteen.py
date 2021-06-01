from django.db import models
from django.contrib.auth import get_user_model
from .sector import Sector


class Canteen(models.Model):
    class Meta:
        verbose_name = "cantine"
        verbose_name_plural = "cantines"

    class ManagementType(models.TextChoices):
        DIRECT = "direct", "Directe"
        CONCEDED = "conceded", "Concédée"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    name = models.TextField(verbose_name="nom")
    city = models.TextField(null=True, blank=True, verbose_name="ville")
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

    def __str__(self):
        return f'Cantine "{self.name}"'
