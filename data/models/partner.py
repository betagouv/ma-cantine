from urllib.parse import quote

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _

from data.department_choices import Department
from data.fields import ChoiceArrayField
from data.utils import optimize_image

from .partnertype import PartnerType
from .sector import Sector


class Partner(models.Model):
    class EconomicModel(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Privé"

    class GratuityOption(models.TextChoices):
        FREE = "free", "Gratuit"
        PAID = "paid", "Payant"
        MIX = "mix", "Mixte"

    class PartnerCategory(models.TextChoices):
        APPRO = "appro", "Améliorer ma part de bio / durable"
        PLASTIC = "plastic", "Substituer mes plastiques"
        ASSO = "asso", "Donner à une association"
        WASTE = "waste", "Diagnostiquer mon gaspillage"
        TRAINING = "training", "Me former ou former mon personnel"
        SUIVI = "suivi", "Assurer mon suivi d'approvisionnement"
        VEGE = "vege", "Diversifier mes sources de protéines"
        NETWORK = "network", "Mise en réseau d’acteurs de terrain"
        FINANCIAL = "financial", "Aide financière / matérielle"

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
    sector_categories = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=Sector.Categories.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Catégorie du secteur dans lequel ce partenaire situe son activité",
    )

    gratuity_option = models.CharField(
        max_length=50,
        choices=GratuityOption.choices,
        null=True,
        blank=True,
        verbose_name="Type d'offre",
    )
    economic_model = models.CharField(
        max_length=50,
        choices=EconomicModel.choices,
        null=True,
        blank=True,
        verbose_name="Secteur économique",
    )
    published = models.BooleanField(default=False, verbose_name="publié")

    contact_email = models.EmailField(_("email address"), blank=True, null=True)
    contact_name = models.TextField(verbose_name="Nom de contact", blank=True, null=True)
    contact_message = models.TextField(verbose_name="Commentaires sur la demande", blank=True, null=True)
    contact_phone_number = models.CharField("Numéro téléphone", max_length=50, null=True, blank=True)

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

    def __str__(self):
        return f'Partenaire "{self.name}"'
