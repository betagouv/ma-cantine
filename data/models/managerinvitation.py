from django.utils.translation import gettext_lazy as _
from django.db import models
from .canteen import Canteen


class ManagerInvitation(models.Model):
    class Meta:
        verbose_name = "nouveau gestionnaire"
        verbose_name_plural = "nouveaux gestionnaires"
        constraints = [
            models.UniqueConstraint(
                fields=["canteen", "email"], name="deduplicate_manager"
            ),
        ]

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    email = models.EmailField(_("email address"))
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email}"
