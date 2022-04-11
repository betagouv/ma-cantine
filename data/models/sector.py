from django.db import models


class Sector(models.Model):
    class Meta:
        verbose_name = "secteur d'activité"
        verbose_name_plural = "secteurs d'activité"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Categories(models.TextChoices):
        ADMINISTRATION = "administration", "Administration"
        EDUCATION = "education", "Enseignement"
        HEALTH = "health", "Santé"
        SOCIAL = "social", "Social / Médico-social"
        LEISURE = "leisure", "Loisirs"
        AUTRES = "autres", "Autres"

    name = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=Categories.choices,
        null=True,
        blank=True,
        verbose_name="catégorie",
    )
    has_line_ministry = models.BooleanField(default=False, verbose_name="Afficher le champ « Ministère de tutelle »")

    @classmethod
    def choices(self):
        return [(x.id, x.__str__()) for x in self.objects.all()]

    def __str__(self):
        return self.name
