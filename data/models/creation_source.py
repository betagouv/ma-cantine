from django.db import models


class CreationSource(models.TextChoices):
    APP = "APP", "APP"
    API = "API", "API"
    IMPORT = "IMPORT", "IMPORT"
    ADMIN = "ADMIN", "ADMIN"
