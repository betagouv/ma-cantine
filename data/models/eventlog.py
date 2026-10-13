import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.timezone import now

logger = logging.getLogger(__name__)


def event_log_file_upload_to(instance, filename):
    """One folder per category, e.g. event-logs/import/2026/10/13/<filename>"""
    return f"event-logs/{instance.category.lower()}/{now():%Y/%m/%d}/{filename}"


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
    file = models.FileField(null=True, blank=True, upload_to=event_log_file_upload_to, verbose_name="fichier")

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="date de création")
    modification_date = models.DateTimeField(auto_now=True, verbose_name="date de modification")

    class Meta:
        verbose_name = "journal d'événements"
        verbose_name_plural = "journal d'événements"

    @classmethod
    def log(cls, category, name, status, user=None, api_oauth2_application=None, data=None, file=None):
        """
        Create an EventLog without ever raising: logging must not break the request or task.
        The savepoint keeps a failed insert from breaking an outer transaction.
        """
        try:
            if user is not None and not user.is_authenticated:
                user = None
            with transaction.atomic():
                return cls.objects.create(
                    category=category,
                    name=name,
                    status=status,
                    user=user,
                    api_oauth2_application=api_oauth2_application,
                    data=data or {},
                    file=file,
                )
        except Exception:
            logger.exception(f"EventLog: could not log event {category} {name} ({status})")
            return None

    def __str__(self):
        return f"{self.get_category_display()} - {self.name} ({self.get_status_display()})"

    @property
    def message_short(self):
        message = self.data.get("message") if isinstance(self.data, dict) else None
        if message and len(message) > 75:
            return message[:75] + "..."
        return message
