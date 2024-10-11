from django.db import models
from simple_history.models import HistoricalRecords

from .canteen import Canteen
from .wasteaction import WasteAction


class ResourceActionQuerySet(models.QuerySet):
    def for_user_canteens(self, user):
        return self.filter(canteen__in=user.canteens.all())


class ResourceAction(models.Model):
    class Meta:
        unique_together = ("resource", "canteen")
        verbose_name = "ressource : action (cantine)"
        verbose_name_plural = "ressources : actions (cantines)"

    objects = models.Manager.from_queryset(ResourceActionQuerySet)()

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # resource = only waste_actions for now
    # but we use the term resource to have a consistent API once we regroup resources
    resource = models.ForeignKey(
        WasteAction, related_name="actions", on_delete=models.CASCADE, verbose_name="ressource"
    )
    canteen = models.ForeignKey(
        Canteen, related_name="resource_actions", on_delete=models.CASCADE, verbose_name="cantine"
    )

    is_done = models.BooleanField(null=True, blank=True, verbose_name="mis en place")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
