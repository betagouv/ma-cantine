from urllib.parse import quote
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from data.department_choices import Department
from data.utils import optimize_image
from data.fields import ChoiceArrayField
from .partnertype import PartnerType
from .sector import Sector


class Partner(models.Model):
    class EconomicModel(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Privé"

    class PartnerCategory(models.TextChoices):
        APPRO = "appro", "Améliorer ma part de bio / durable"
        PLASTIC = "plastic", "Substituer mes plastiques"
        ASSO = "asso", "Donner à une association"
        WASTE = "waste", "Diagnostiquer mon gaspillage"
        TRAINING = "training", "Me former ou former mon personnel"
        SUIVI = "suivi", "Assurer mon suivi d'approvisionnement"
        VEGE = "vege", "Diversifier mes sources de protéines"

    class Meta:
        verbose_name = "partenaire"
        verbose_name_plural = "partenaires"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    name = models.TextField(verbose_name="nom")
    short_description = models.TextField(verbose_name="description courte")
    long_description = RichTextUploadingField(null=True, blank=True, verbose_name="description longue")
    image = models.ImageField(null=True, blank=True, verbose_name="Photo / image")
    website = models.URLField(blank=True, null=True, verbose_name="Site web")

    types = models.ManyToManyField(PartnerType, blank=True, verbose_name="types d'acteur")
    categories = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=PartnerCategory.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Besoin(s) comblé(s) par ce partenaire",
    )

    departments = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=Department.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="departements où le partenaire est présent (sauf si national)",
    )
    national = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Le partenaire est présent dans tout le territoire national (tous les departements)",
    )
    sectors = models.ManyToManyField(Sector, blank=True, verbose_name="secteurs d'activité")
    free = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Gratuit",
    )
    economic_model = models.CharField(
        max_length=50,
        choices=EconomicModel.choices,
        null=True,
        blank=True,
        verbose_name="Secteur économique",
    )
    published = models.BooleanField(default=False, verbose_name="publié")

    @property
    def url_slug(self):
        return f"{self.id}--{quote(self.name)}"

    @property
    def url_path(self):
        return f"/acteurs-de-l-eco-systeme/{self.url_slug}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        max_image_size = 1600
        if self.image:
            self.image = optimize_image(self.image, self.image.name, max_image_size)
        super(Partner, self).save(force_insert, force_update, using, update_fields)
