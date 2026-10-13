from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class EventLog(models.Model):
    class Category(models.TextChoices):
        IMPORT = "IMPORT", "Import de masse"
        API = "API", "Requête API (OAuth2)"
        TASK = "TASK", "Tâche asynchrone (Celery)"

    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Succès"
        FAILURE = "FAILURE", "Échec"

    category = models.TextField(choices=Category.choices, verbose_name="catégorie")
    name = models.TextField(verbose_name="nom")
    status = models.TextField(choices=Status.choices, verbose_name="statut")
    user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="utilisateur",
    )
    api_oauth2_application = models.ForeignKey(
        settings.OAUTH2_PROVIDER_APPLICATION_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Application OAuth2 (API)",
    )
    data = models.JSONField(default=dict, blank=True, verbose_name="données")

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="date de création")
    modification_date = models.DateTimeField(auto_now=True, verbose_name="date de modification")

    class Meta:
        verbose_name = "journal d'événements"
        verbose_name_plural = "journal d'événements"

    def __str__(self):
        return f"{self.get_category_display()} - {self.name} ({self.get_status_display()})"

    @property
    def message_short(self):
        message = self.data.get("message") if isinstance(self.data, dict) else None
        if message and len(message) > 75:
            return message[:75] + "..."
        return message
