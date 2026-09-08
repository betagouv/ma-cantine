# Imports needed to help Django discover the models in the subfolders

from django.db import models

from common.cache.models import Cache  # noqa


class CommandLog(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Succès"
        FAILURE = "FAILURE", "Échec"

    CREATION_META_FIELDS = ["creation_date", "modification_date"]

    command_name = models.CharField(max_length=255, db_index=True)
    input_data = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUCCESS)
    output_data = models.TextField(blank=True, null=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(blank=True, null=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creation_date"]

    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).total_seconds()
        return None
