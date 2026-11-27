from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Case, Q, Value, When

from common.utils import utils as utils_utils
from data.validators import invitation as invitation_validators

from .canteen import Canteen


class InvitationQuerySet(models.QuerySet):
    def for_user(self, user):
        """
        Invitations sent or received by the canteens managed by the user
        """
        user_canteen_ids = user.canteens.values("id")
        return self.filter(Q(creation_canteen_id__in=user_canteen_ids) | Q(invited_canteen_id__in=user_canteen_ids))

    def annotate_with_direction(self, user):
        """
        RECEIVED if the user manages the invited canteen, otherwise SENT
        (if the user manages both canteens: RECEIVED, because the user can accept the invitation)
        """
        user_canteen_ids = user.canteens.values("id")
        return self.annotate(
            direction=Case(
                When(invited_canteen_id__in=user_canteen_ids, then=Value(Invitation.Direction.RECEIVED)),
                default=Value(Invitation.Direction.SENT),
                output_field=models.CharField(),
            )
        )


class Invitation(models.Model):
    class Category(models.TextChoices):
        ADD_SATELLITE = "ADD_SATELLITE", "Ajouter un restaurant satellite"

    class Status(models.TextChoices):
        SENT = "SENT", "Envoyée"
        ACCEPTED = "ACCEPTED", "Acceptée"
        DECLINED = "DECLINED", "Refusée"
        CANCELLED = "CANCELLED", "Annulée"

    class Direction(models.TextChoices):
        # not a field: annotated depending on the user (see InvitationQuerySet.annotate_with_direction)
        SENT = "SENT", "Envoyée"
        RECEIVED = "RECEIVED", "Reçue"

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

    objects = InvitationQuerySet.as_manager()

    class Meta:
        verbose_name = "invitation"
        verbose_name_plural = "invitations"

    def __str__(self):
        return f"Invitation {self.get_category_display()} de {self.creation_canteen} ({self.get_status_display()})"

    def clean(self):
        validation_errors = utils_utils.merge_validation_errors(
            invitation_validators.validate_invitation_creation_canteen_field(self),
            invitation_validators.validate_invitation_invited_canteen_field(self),
            invitation_validators.validate_invitation_answer_fields(self),
        )
        if validation_errors:
            raise ValidationError(validation_errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
