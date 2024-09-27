from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from .canteen import Canteen
from .wasteaction import WasteAction


class ResourceAction(models.Model):
    class Meta:
        verbose_name = "ressource : action utilisateur"
        verbose_name_plural = "ressources : actions utilisateurs"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    # only waste_actions for now, to generalize in the future
    resource = models.ForeignKey(WasteAction, on_delete=models.CASCADE, verbose_name="ressource")
    canteen = models.ForeignKey(Canteen, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="cantine")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name="utilisateur"
    )

    is_done = models.BooleanField(null=True, blank=True, verbose_name="mis en place")
    is_not_interested = models.BooleanField(null=True, blank=True, verbose_name="pas intéressé")
    is_favorite = models.BooleanField(default=False, verbose_name="favori")

    def clean(self):
        if not any([self.canteen_id, self.user_id]):
            raise ValidationError("L'action doit être rattachée à au moins une cantine ou un utilisateur")
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
