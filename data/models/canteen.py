from urllib.parse import quote
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from data.department_choices import Department
from data.utils import optimize_image
from .sector import Sector
from .softdeletionmodel import SoftDeletionModel


def validate_siret(siret):
    """
    Performs length and Luhn validation
    (https://portal.hardis-group.com/pages/viewpage.action?pageId=120357227)
    """
    if siret is None or siret == "":
        return
    if len(siret) != 14:
        raise ValidationError("14 caractères numériques sont attendus")
    odd_digits = [int(n) for n in siret[-1::-2]]
    even_digits = [int(n) for n in siret[-2::-2]]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(int(n) for n in str(digit * 2))
    luhn_checksum_valid = checksum % 10 == 0

    if not luhn_checksum_valid:
        raise ValidationError("Le numéro SIRET n'est pas valide.")


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

    class PublicationStatus(models.TextChoices):
        DRAFT = "draft", "🔒 Non publié"
        PENDING = "pending", "❓ En attente de vérification"
        PUBLISHED = "published", "✅ Publié"

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
    publication_status = models.CharField(
        max_length=50,
        choices=PublicationStatus.choices,
        default="draft",
        verbose_name="état de publication",
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
    # TODO: once have a standardised format (see _normalise_siret), index by siret if given
    siret = models.TextField(null=True, blank=True, validators=[validate_siret])
    central_producer_siret = models.TextField(
        null=True,
        blank=True,
        verbose_name="siret de la cuisine centrale",
        validators=[validate_siret],
    )
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

    @property
    def url_path(self):
        slug = f"{quote(self.name)}--{self.id}"
        return f"/nos-cantines/{slug}"

    def __str__(self):
        return f'Cantine "{self.name}"'
