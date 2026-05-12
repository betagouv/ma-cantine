from django.db import models
from django.utils.translation import gettext_lazy as _

from .canteen import Canteen


class ManagerInvitation(models.Model):
    email = models.EmailField(_("email address"))
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "invitation de gestion"
        verbose_name_plural = "invitations de gestion"
        constraints = [
            models.UniqueConstraint(fields=["canteen", "email"], name="deduplicate_invitation"),
        ]

    def __str__(self):
        return f"{self.email}"
