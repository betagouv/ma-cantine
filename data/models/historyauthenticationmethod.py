import logging

from django.dispatch import receiver
from django.db import models
from simple_history.models import HistoricalRecords
from simple_history.signals import pre_create_historical_record

from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)


class AuthenticationMethodHistoricalRecords(models.Model):
    """
    Abstract model for history models tracking the authentication method.
    """

    history_source = models.CharField(
        max_length=255,
        choices=CreationSource.choices,
        verbose_name="source de modification",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


def historical_record_add_source(history_instance):
    if not hasattr(history_instance, "history_source"):
        return

    if not hasattr(HistoricalRecords, "context") or not hasattr(HistoricalRecords.context, "request"):
        # history_instance.history_source = "AUTO"
        return

    request = HistoricalRecords.context.request
    metadata = request.META

    path_info = metadata["PATH_INFO"]
    path_parts = path_info.split("/")
    path_root = path_parts[1] if len(path_parts) > 1 else path_parts[0]
    if path_root == "admin":
        history_instance.history_source = CreationSource.ADMIN
        return
    elif "import" in path_info:
        history_instance.history_source = CreationSource.IMPORT
        return

    if request.auth and hasattr(request.auth, "application"):
        history_instance.history_source = CreationSource.API
    else:
        history_instance.history_source = CreationSource.APP


@receiver(pre_create_historical_record)
def pre_historical_record_save(sender, **kwargs):
    try:
        history_instance = kwargs["history_instance"]
        historical_record_add_source(history_instance)
    except Exception as e:
        logger.error("Error when attempting to set authentication method on a history object", e)
