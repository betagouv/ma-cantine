from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from wagtail.models import RevisionMixin

from data.fields import ChoiceArrayField


class WasteAction(RevisionMixin, models.Model):
    class Meta:
        verbose_name = "Action anti-gaspi"
        verbose_name_plural = "Actions anti-gaspi"
        ordering = ["-modification_date"]

    class Effort(models.TextChoices):
        SMALL = "SMALL", "Petit pas"
        MEDIUM = "MEDIUM", "Moyen"
        LARGE = "LARGE", "Grand projet"

    class WasteOrigin(models.TextChoices):
        PREP = "PREP", "Préparation"
        UNSERVED = "UNSERVED", "Non servi"
        PLATE = "PLATE", "Retour assiette"

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    modification_date = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    title = models.TextField(verbose_name="Titre")
    subtitle = models.TextField(null=True, blank=True, verbose_name="Sous-titre")
    description = RichTextField(
        verbose_name="Description",
        default="<h2>Description</h2><h2>Conseils pratiques</h2><ul><li></li></ul>",
    )
    effort = models.CharField(max_length=255, choices=Effort.choices, verbose_name="Niveau d'effort")
    waste_origins = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=WasteOrigin.choices),
        size=None,
        verbose_name="Origines du gaspillage",
    )
    lead_image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True, blank=True, verbose_name="Image"
    )

    # not using revisions directly in case we want to add custom logic in the property in the future
    _revisions = GenericRelation("wagtailcore.Revision", related_query_name="wasteaction")

    @property
    def revisions(self):
        return self._revisions

    def __str__(self):
        return f'Action anti-gaspi "{self.title}"'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def effort_display(self):
        return dict(WasteAction.Effort.choices)[self.effort]

    effort_display.short_description = "Niveau d'effort"
    effort_display.admin_order_field = "effort"

    def waste_origins_display(self):
        return ", ".join([dict(WasteAction.WasteOrigin.choices)[origin] for origin in self.waste_origins])

    waste_origins_display.short_description = "Origines du gaspillage"
    waste_origins_display.admin_order_field = "waste_origins"

    def has_lead_image(self):
        return "Oui" if self.lead_image else "Non"

    has_lead_image.short_description = "Image"
    has_lead_image.admin_order_field = "lead_image"
