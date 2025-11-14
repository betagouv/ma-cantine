from django.db import models


# 26 : Administration : Etablissements publics d’Etat (EPA ou EPIC)
# 24 : Administration : Restaurants des prisons
# 23 : Administration : Restaurants administratifs d’Etat (RA)
# 22 : Administration : Restaurants des armées / police / gendarmerie
# 4 : Administration : Restaurants inter-administratifs d’Etat (RIA)
# 2 : Education : Supérieur et Universitaire
SECTEURS_SPE = [26, 24, 23, 22, 4, 2]


class SectorM2M(models.Model):
    class Meta:
        verbose_name = "secteur d'activité"
        verbose_name_plural = "secteurs d'activité"

    class Categories(models.TextChoices):
        ADMINISTRATION = "administration", "Administration"
        ENTERPRISE = "enterprise", "Entreprise"
        EDUCATION = "education", "Enseignement"
        HEALTH = "health", "Santé"
        SOCIAL = "social", "Social / Médico-social"
        LEISURE = "leisure", "Loisirs"
        AUTRES = "autres", "Autres"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

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
