from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from data.utils import optimize_image
from data.fields import ChoiceArrayField


class User(AbstractUser):
    class LawAwareness(models.TextChoices):
        LAW_AWARENESS_1_CHOICE = "LAW_AWARENESS_1_CHOICE", "LAW_AWARENESS_1_TEXT"
        LAW_AWARENESS_2_CHOICE = "LAW_AWARENESS_2_CHOICE", "LAW_AWARENESS_2_TEXT"
        LAW_AWARENESS_3_CHOICE = "LAW_AWARENESS_3_CHOICE", "LAW_AWARENESS_3_TEXT"
        LAW_AWARENESS_4_CHOICE = "LAW_AWARENESS_4_CHOICE", "LAW_AWARENESS_4_TEXT"
        LAW_AWARENESS_5_CHOICE = "LAW_AWARENESS_5_CHOICE", "LAW_AWARENESS_5_TEXT"
        LAW_AWARENESS_6_CHOICE = "LAW_AWARENESS_6_CHOICE", "LAW_AWARENESS_6_TEXT"

    avatar = models.ImageField("Photo de profil", null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    email_confirmed = models.BooleanField(default="False", verbose_name="adresse email confirmée")

    law_awareness = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=LawAwareness.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="LAW_AWARENESS_DESCRIPTION",
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        max_avatar_size = 640
        if self.avatar:
            self.avatar = optimize_image(self.avatar, self.avatar.name, max_avatar_size)
        super(User, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
