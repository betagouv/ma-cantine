from django.db import models

from .canteen import Canteen
from .wasteaction import WasteAction


class ResourceAction(models.Model):
    class Meta:
        unique_together = ("resource", "canteen")
        verbose_name = "ressource : action (cantine)"
        verbose_name_plural = "ressources : actions (cantines)"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    # resource = only waste_actions for now
    # but we use the term resource to have a consistent API once we regroup resources
    resource = models.ForeignKey(WasteAction, on_delete=models.CASCADE, verbose_name="ressource")
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, verbose_name="cantine")

    is_done = models.BooleanField(null=True, blank=True, verbose_name="mis en place")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
