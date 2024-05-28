from django.db import models


class AuthenticationMethodHistoricalRecords(models.Model):
    """
    Abstract model for history models tracking the authentication method.
    """

    class AuthMethodChoices(models.TextChoices):
        WEBSITE = "WEBSITE", "Via la plateforme en ligne"
        API = "API", "Via une intégration API"
        AUTO = "AUTO", "Via un script ou bot interne"
        ADMIN = "ADMIN", "Via site admin"

    authentication_method = models.CharField(
        max_length=255,
        choices=AuthMethodChoices.choices,
        verbose_name="méthode d'authentification",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
