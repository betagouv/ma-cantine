from django.db import models


class Sector(models.Model):
    class Meta:
        verbose_name = "secteur d'activité"
        verbose_name_plural = "secteurs d'activité"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    name = models.TextField()

    def __str__(self):
        return self.name
