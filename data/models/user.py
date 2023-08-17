from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from data.utils import optimize_image
from data.fields import ChoiceArrayField
from data.department_choices import Department


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
            "J’ai un système de saisie formalisé (SI, Excel, papier) permettant de calculer et reporter le montant annuel de mes achats répondants aux exigences de l’article 24 de la loi EGAlim (Non applicable en gestion concédée)",
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
            "J’ai établi un plan d’actions pour tendre vers les objectifs de la loi EGAlim, définissant notamment : le niveau d’ambition global et par catégories d’achats ; les échéances de renouvellement de contrat avec clauses EGAlim ; le phasage de la progression des indicateurs EGAlim",
        )
        QUALITY_ACHIEVED = (
            "QUALITY_ACHIEVED",
            "J'ai atteint les objectifs - 50% et 20%, de l’article 24 de la loi EGAlim",
        )

    class JobRoles(models.TextChoices):
        ESTABLISHMENT_MANAGER = "ESTABLISHMENT_MANAGER", "Gestionnaire d'établissement"
        CATERING_PURCHASES_MANAGER = "CATERING_PURCHASES_MANAGER", "Direction Achat Société de restauration"
        DIRECT_PURCHASES_MANAGER = "DIRECT_PURCHASES_MANAGER", "Responsable d'achats en gestion directe"
        CENTRAL_MANAGER = "CENTRAL_MANAGER", "Responsable de plusieurs établissements (type cuisine centrale)"
        MANY_ESTABLISHMENTS_MANAGER = "MANY_ESTABLISHMENTS_MANAGER", "Responsable de plusieurs établissements (SRC)"
        TECHNICAL = "TECHNICAL", "Développement logiciel, analyse de données ou autre rôle technique"
        OTHER = "OTHER", "Autre"

    class Sources(models.TextChoices):
        WEBINAIRE = "WEBINAIRE", "Webinaire"
        WEB_SEARCH = "WEB_SEARCH", "Recherche web"
        INSTITUTION = "INSTITUTION", "Communication institutionnelle (DRAAF, association régionale)"
        WORD_OF_MOUTH = "WORD_OF_MOUTH", "Bouche à oreille"
        SOCIAL_MEDIA = "SOCIAL_MEDIA", "Réseaux sociaux"
        OTHER = "OTHER", "Autre (spécifiez)"

    avatar = models.ImageField("Photo de profil", null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    email_confirmed = models.BooleanField(default="False", verbose_name="adresse email confirmée")

    opt_out_reminder_emails = models.BooleanField(default="False", verbose_name="Désactiver les emails de rappel")

    law_awareness = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=LawAwareness.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Les affirmations suivantes concernent l'article 24 de la loi EGAlim, encadrant les objectifs d'approvisionnements (50% de produits durables et de qualité dont 20% de bio). Parmi ces affirmations, plusieurs choix sont possibles. Choisissez celles qui correspondent à votre situation :",
    )

    is_dev = models.BooleanField(default="False", verbose_name="Compte développeur / technique")
    is_elected_official = models.BooleanField(default="False", verbose_name="Compte élu·e")

    # MonComptePro
    created_with_mcp = models.BooleanField(default="False", verbose_name="Compte créé avec MonComptePro")
    mcp_id = models.TextField(blank=True, null=True, verbose_name="ID MonComptePro")
    mcp_organizations = models.JSONField(blank=True, null=True, verbose_name="Organisations sous MonComptePro")

    # Email campaigns
    email_no_canteen_first_reminder = models.DateTimeField(
        null=True, blank=True, verbose_name="Date d'envoi du premier email pour manque de cantines"
    )
    email_no_canteen_second_reminder = models.DateTimeField(
        null=True, blank=True, verbose_name="Date d'envoi du second email pour manque de cantines"
    )
    phone_number = models.CharField("Numéro téléphone", max_length=50, null=True, blank=True)

    job = models.CharField(
        max_length=255,
        choices=JobRoles.choices,
        blank=True,
        null=True,
        verbose_name="Fonction",
    )
    other_job_description = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre fonction détail",
    )

    source = models.CharField(
        max_length=255,
        choices=Sources.choices,
        blank=True,
        null=True,
        verbose_name="Comment est-ce que la personne a connu ma cantine ?",
    )
    other_source_description = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre source détail",
    )

    # Campaign tracking
    creation_mtm_source = models.TextField(
        null=True, blank=True, verbose_name="mtm_source du lien tracké lors de la création"
    )
    creation_mtm_campaign = models.TextField(
        null=True, blank=True, verbose_name="mtm_campaign du lien tracké lors de la création"
    )
    creation_mtm_medium = models.TextField(
        null=True, blank=True, verbose_name="mtm_medium du lien tracké lors de la création"
    )

    # Bizdev fields
    number_of_managed_cantines = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nombre d'établissements gérés par l'utilisateur",
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        max_avatar_size = 640
        if self.avatar:
            self.avatar = optimize_image(self.avatar, self.avatar.name, max_avatar_size)
        super(User, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    # Geographical scope for elected profiles
    departments = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=Department.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="departements où l'élu·e peut regarder les cantines",
    )

    @property
    def has_mtm_data(self):
        return self.creation_mtm_source or self.creation_mtm_campaign or self.creation_mtm_medium
