from django.contrib.auth import get_user_model
from django.db import models

from .canteen import Canteen


class Invitation(models.Model):
    class Category(models.TextChoices):
        ADD_SATELLITE = "ADD_SATELLITE", "Ajouter un restaurant satellite"

    class Status(models.TextChoices):
        SENT = "SENT", "Envoyée"
        ACCEPTED = "ACCEPTED", "Acceptée"
        DECLINED = "DECLINED", "Refusée"
        CANCELLED = "CANCELLED", "Annulée"

    category = models.CharField(max_length=50, choices=Category.choices, verbose_name="catégorie")
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.SENT, verbose_name="statut")

    creation_canteen = models.ForeignKey(
        Canteen,
        on_delete=models.CASCADE,
        related_name="invitations_sent",
        verbose_name="cantine qui a envoyé l'invitation",
    )
    creation_user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invitations_created",
        verbose_name="utilisateur qui a envoyé l'invitation",
    )

    invited_canteen = models.ForeignKey(
        Canteen,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="invitations_received",
        verbose_name="cantine invitée",
    )

    answer_user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invitations_answered",
        verbose_name="utilisateur qui a répondu à l'invitation",
    )
    answer_date = models.DateTimeField(null=True, blank=True, verbose_name="date de la réponse")

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "invitation"
        verbose_name_plural = "invitations"

    def __str__(self):
        return f"Invitation {self.get_category_display()} de {self.creation_canteen} ({self.get_status_display()})"
