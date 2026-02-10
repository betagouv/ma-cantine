from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Count, Q, F
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import macantine.brevo as brevo

from data.models.geo import Department
from data.fields import ChoiceArrayField
from data.utils import optimize_image


class UserQuerySet(models.QuerySet):
    def brevo_to_create(self):
        return self.filter(brevo_last_update_date__isnull=True)

    def brevo_to_update(self):
        one_day_ago = timezone.now() - timezone.timedelta(days=brevo.CONTACT_BULK_UPDATE_LAST_UPDATED_THRESHOLD_DAYS)
        return self.exclude(brevo_is_deleted=True).filter(brevo_last_update_date__lte=one_day_ago)

    def with_canteen_stats(self):
        from data.models import Canteen

        return self.prefetch_related("canteens").annotate(
            nb_cantines=Count("canteens", distinct=True),
            nb_cantines_groupe=Count(
                "canteens",
                filter=Q(
                    canteens__production_type__in=[
                        Canteen.ProductionType.GROUPE,
                        Canteen.ProductionType.CENTRAL,
                        Canteen.ProductionType.CENTRAL_SERVING,
                    ]
                ),
                distinct=True,
            ),
            nb_cantines_site=Count(
                "canteens", filter=Q(canteens__production_type=Canteen.ProductionType.ON_SITE), distinct=True
            ),
            nb_cantines_satellite=Count(
                "canteens", filter=Q(canteens__production_type=Canteen.ProductionType.ON_SITE_CENTRAL), distinct=True
            ),
            nb_cantines_gestion_concedee=Count(
                "canteens", filter=Q(canteens__management_type=Canteen.ManagementType.CONCEDED), distinct=True
            ),
        )

    def with_canteen_diagnostic_stats(self):
        """
        # TODO: clarify nb_cantines_td_todo_2025
        """
        return self.prefetch_related("canteens", "canteens__diagnostics").annotate(
            # bilans
            nb_cantines_bilan_2025=Count(
                "canteens__diagnostics", filter=Q(canteens__diagnostics__year=2025), distinct=True
            ),
            nb_cantines_bilan_todo_2025=Count("canteens", distinct=True) - F("nb_cantines_bilan_2025"),
            # TDs
            nb_cantines_td_2025=Count("canteens", filter=Q(canteens__declaration_donnees_2025=True), distinct=True),
            # nb_cantines_td_todo_2025=F("nb_cantines_bilan_2025") - Count(
            #     "canteens",
            #     filter=Q(
            #         canteens__declaration_donnees_2025=False
            #     ),
            #     distinct=True
            # ),
        )


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    class LawAwareness(models.TextChoices):
        NONE = (
            "NONE",
            "Je n’ai pas une connaissance détaillée de l’article 24 de la loi EGalim",
        )
        AIMS_DEADLINES = "AIMS_DEADLINES", "Je connais les objectifs et les échéances"
        ELIGIBLE_LABELS = "ELIGIBLE_LABELS", "Je connais la liste des labels éligibles et mentions valorisantes"
        MY_LABELS = (
            "MY_LABELS",
            "J’ai accès aux informations ou mon prestataire me fournit les informations sur les labels éligibles et mentions valorisantes concernant mes achats",
        )
        SYSTEM = (
            "SYSTEM",
            "J’ai un système de saisie formalisé (SI, Excel, papier) permettant de calculer et reporter le montant annuel de mes achats répondants aux exigences de l’article 24 de la loi EGalim (Non applicable en gestion concédée)",
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
            "J’ai établi un plan d’actions pour tendre vers les objectifs de la loi EGalim, définissant notamment : le niveau d’ambition global et par catégories d’achats ; les échéances de renouvellement de contrat avec clauses EGalim ; le phasage de la progression des indicateurs EGalim",
        )
        QUALITY_ACHIEVED = (
            "QUALITY_ACHIEVED",
            "J'ai atteint les objectifs - 50% et 20%, de l’article 24 de la loi EGalim",
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

    MATOMO_FIELDS = [
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
    ]

    BREVO_FIELDS = [
        "brevo_last_update_date",
        "brevo_is_deleted",
    ]

    DATA_CANTEEN_FIELDS = [
        "nb_cantines",
        "nb_cantines_site",
        "nb_cantines_satellite",
        "nb_cantines_groupe",
        "nb_cantines_gestion_concedee",
    ]
    DATA_CANTEEN_DIAGNOSTIC_FIELDS = [
        "nb_cantines_bilan_2025",
        "nb_cantines_bilan_todo_2025",
        "nb_cantines_td_2025",
        # "nb_cantines_td_todo_2025",
    ]

    objects = UserManager.from_queryset(UserQuerySet)()

    avatar = models.ImageField("Photo de profil", null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    email_confirmed = models.BooleanField(default="False", verbose_name="adresse email confirmée")

    law_awareness = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=LawAwareness.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Les affirmations suivantes concernent l'article 24 de la loi EGalim, encadrant les objectifs d'approvisionnements (50% de produits durables et de qualité dont 20% de bio). Parmi ces affirmations, plusieurs choix sont possibles. Choisissez celles qui correspondent à votre situation :",
    )

    is_dev = models.BooleanField(default="False", verbose_name="Compte développeur / technique")
    is_elected_official = models.BooleanField(default="False", verbose_name="Compte élu·e")

    # MonComptePro
    created_with_mcp = models.BooleanField(default="False", verbose_name="Compte créé avec MonComptePro")
    mcp_id = models.TextField(blank=True, null=True, verbose_name="ID MonComptePro")
    mcp_organizations = models.JSONField(blank=True, null=True, verbose_name="Organisations sous MonComptePro")

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

    # Geographical scope for elected profiles
    departments = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=Department.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="departements où l'élu·e peut regarder les cantines",
    )

    # Emails
    opt_out_reminder_emails = models.BooleanField(default="False", verbose_name="Désactiver les emails de rappel")
    brevo_last_update_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Date de la dernière mise à jour Brevo"
    )
    brevo_is_deleted = models.BooleanField(default=False, verbose_name="Indique si le contact a été supprimé de Brevo")

    data = models.JSONField(blank=True, null=True, verbose_name="Données calculées")

    # Django fields
    # last_login, date_joined, is_active, is_staff, is_superuser

    def save(self, **kwargs):
        max_avatar_size = 640
        if self.avatar:
            self.avatar = optimize_image(self.avatar, self.avatar.name, max_avatar_size)
        super().save(**kwargs)

    @property
    def has_mtm_data(self):
        return self.creation_mtm_source or self.creation_mtm_campaign or self.creation_mtm_medium

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def canteens_count(self):
        return self.canteens.count()

    def has_canteens(self):
        return self.canteens.exists()

    def has_missing_diagnostic_for_year(self, year):
        return self.canteens.exists() and any(not x.has_diagnostic_for_year(year) for x in self.canteens.all())

    def has_missing_teledeclaration_for_year(self, year):
        return self.canteens.exists() and any(
            not x.has_diagnostic_teledeclared_for_year(year) for x in self.canteens.all()
        )

    def update_data(self):
        # need to have called the user with 'with_canteen_stats' & 'with_canteen_diagnostic_stats' queryset method
        self.data = {
            field: getattr(self, field) for field in self.DATA_CANTEEN_FIELDS + self.DATA_CANTEEN_DIAGNOSTIC_FIELDS
        }
        self.data["modification_date"] = timezone.now().isoformat()
        self.save(update_fields=["data"])

    def get_brevo_data(self):
        """
        See macantine/brevo.py for usage.
        """
        data_canteen_fields_dict = {
            f"MA_CANTINE_{field.upper()}": self.data.get(field, 0) if self.data else 0
            for field in self.DATA_CANTEEN_FIELDS
        }
        data_canteen_diagnostic_fields_dict = {
            f"MA_CANTINE_{field.upper()}": self.data.get(field, 0) if self.data else 0
            for field in self.DATA_CANTEEN_DIAGNOSTIC_FIELDS
        }
        return {
            # user info
            "NOM": self.last_name,
            "PRENOM": self.first_name,
            "NOM_COMPLET": self.get_full_name(),
            "MA_CANTINE_DATE_INSCRIPTION": self.date_joined.strftime("%Y-%m-%d"),
            "MA_CANTINE_DERNIERE_CONNEXION": self.last_login.strftime("%Y-%m-%d") if self.last_login else "",
            "MA_CANTINE_COMPTE_DEV": self.is_dev,
            "MA_CANTINE_COMPTE_ELU_E": self.is_elected_official,
            # user canteen & diagnostic info
            **data_canteen_fields_dict,
            **data_canteen_diagnostic_fields_dict,
        }
