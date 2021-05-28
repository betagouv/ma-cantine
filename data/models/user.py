from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from data.utils import optimize_image


class User(AbstractUser):
    avatar = models.ImageField("Photo de profil", null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        max_avatar_size = 640
        if self.avatar:
            self.avatar = optimize_image(self.avatar, self.avatar.name, max_avatar_size)
        super(User, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
