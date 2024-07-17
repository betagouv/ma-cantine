from django.db import models
from data.fields import ChoiceArrayField
from wagtail.fields import RichTextField

class ActionSheet(models.Model):
    class Meta:
        verbose_name = "Fiche action"
        verbose_name_plural = "Fiche actions"
        ordering = ["-modification_date"]
    class Effort(models.TextChoices):
        SMALL = "SMALL", "Petit pas"
        LARGE = "LARGE", "Grand projet"
    class WasteOrigin(models.TextChoices):
        PREP = "PREP", "Préparation"
        UNSERVED = "UNSERVED", "Non servi"
        PLATE = "PLATE", "Retour assiette"
    title = models.TextField(verbose_name="Titre")
    subtitle = models.TextField(verbose_name="Sous-titre")
    effort = models.CharField(
        max_length=255,
        choices=Effort.choices,
        verbose_name="Niveau d'effort"
    )
    waste_origin = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=WasteOrigin.choices),
        size=None,
        verbose_name="Origines du gaspillage"
    )
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    modification_date = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    description = RichTextField(verbose_name="Description", null=True, blank=True, default="<h2>Description</h2><h2>Conseils pratiques</h2><ul><li></li></ul>")
    savings_estimation = models.IntegerField(verbose_name="Estimation d'économies (€)")
    coefficient = models.IntegerField(verbose_name="Coefficient d'évolution")
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True
    )
    def __str__(self):
        return f'Fiche action "{self.title}"'