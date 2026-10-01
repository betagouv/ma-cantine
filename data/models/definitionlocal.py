from django.db import models


class DefinitionLocal(models.TextChoices):
    PAT = "PAT", "Issu du Projet Alimentaire Territorial (PAT)"
    COMMUNE = "COMMUNE", "Commune et/ou intercommunalité"
    DEPARTEMENT = "DEPARTEMENT", "Département"
    REGION = "REGION", "Région"
    KM = "KM", "Distance en km"
