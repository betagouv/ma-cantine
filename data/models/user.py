from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from data.utils import optimize_image
from data.fields import ChoiceArrayField


class User(AbstractUser):
    class LawAwareness(models.TextChoices):
        NONE = (
            "NONE",
            "Je n’ai pas une connaissance détaillée de l’article 24 de la loi EGAlim",
        )
        AIMS_DEADLINES = "AIMS_DEADLINES", "Je connais les objectifs et les échéances"
        ELIGIBLE_LABELS = "ELIGIBLE_LABELS", "Je connais la liste des labels éligibles et mentions valorisantes"
        MY_LABELS = (
            "MY_LABELS",
            "J’ai accès aux informations ou mon prestataire me fournit les informations sur les labels éligibles et mentions valorisantes concernant mes achats",
        )
        SYSTEM = (
            "SYSTEM",
            "J’ai un système de saisie formalisé (SI, Excel, papier) permettant de calculer et reporter le montant annuel de mes achats répondants aux exigences de l’article 24 de la loi EGALIM (N/A en gestion concédée)",
        )
        TAKEN_STOCK = (
            "TAKEN_STOCK",
            "J’ai réalisé un état des lieux précis de mes approvisionnements",
        )
        OPTION_DIAGNOSTIC = (
            "OPTION_DIAGNOSTIC",
            "J’ai réalisé un diagnostic de l’offre (disponibilité et caractéristiques de l’offre des différents fournisseurs sur l’ensemble des catégories d’achats)",
        )
        ACTION_PLAN = (
            "ACTION_PLAN",
            "J’ai établi un plan d’actions pour tendre vers les objectifs de la loi EGALim, définissant notamment : le niveau d’ambition global et par catégories d’achats; les échéances de renouvellement de contrat avec clauses EGALim; le phasage de la progression des indicateurs EGAlim",
        )
        QUALITY_ACHIEVED = (
            "QUALITY_ACHIEVED",
            "J'ai atteint les objectifs de l’article 24 de la loi EGAlim de porter la part de produits de qualité et durables à 50% dont au moins 20% de produits issus de l'agriculture biologique",
        )

    avatar = models.ImageField("Photo de profil", null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    email_confirmed = models.BooleanField(default="False", verbose_name="adresse email confirmée")

    law_awareness = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=LawAwareness.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Parmi ces affirmations, lesquelles correspondent le plus à votre situation :",
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        max_avatar_size = 640
        if self.avatar:
            self.avatar = optimize_image(self.avatar, self.avatar.name, max_avatar_size)
        super(User, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
