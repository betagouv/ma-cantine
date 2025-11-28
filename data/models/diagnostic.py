from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Case, F, IntegerField, Q, Sum, When
from django.db.models.fields.json import KT
from django.db.models.functions import Cast
from django.utils import timezone
from simple_history.models import HistoricalRecords

from common.utils import utils as utils_utils
from data.fields import ChoiceArrayField
from data.models import Canteen
from data.models.creation_source import CreationSource
from data.utils import CustomJSONEncoder, make_optional_positive_decimal_field, sum_int_with_potential_null
from data.validators import diagnostic as diagnostic_validators
from macantine.utils import (
    CAMPAIGN_DATES,
    EGALIM_OBJECTIVES,
    TELEDECLARATION_CURRENT_VERSION,
    is_in_teledeclaration_or_correction,
)


def in_teledeclaration_campaign_query(year):
    year = int(year)
    return Q(
        teledeclaration_date__range=(
            CAMPAIGN_DATES[year]["teledeclaration_start_date"],
            CAMPAIGN_DATES[year]["teledeclaration_end_date"],
        )
    )


def in_correction_campaign_query(year):
    year = int(year)
    return Q(
        teledeclaration_date__range=(
            CAMPAIGN_DATES[year]["correction_start_date"],
            CAMPAIGN_DATES[year]["correction_end_date"],
        )
    )


class DiagnosticQuerySet(models.QuerySet):
    def filled(self):
        return self.filter(value_total_ht__gt=0)

    def teledeclared(self):
        return self.filter(status=Diagnostic.DiagnosticStatus.SUBMITTED)

    def in_year(self, year):
        return self.filter(year=int(year))

    def in_campaign(self, year):
        year = int(year)
        if year in CAMPAIGN_DATES.keys():
            if "correction_start_date" in CAMPAIGN_DATES[year].keys():
                return self.filter(in_teledeclaration_campaign_query(year) | in_correction_campaign_query(year))
            else:
                return self.filter(in_teledeclaration_campaign_query(year))
        else:
            return self.none()

    def teledeclared_for_year(self, year):
        return self.teledeclared().in_year(year).in_campaign(year)

    def with_meal_price(self):
        """
        Le coût denrées est calculé en divisant la valeur d'achat alimentaire total par le nombre de repas annuels.
        """
        return self.annotate(
            canteen_yearly_meal_count=Cast(KT("canteen_snapshot__yearly_meal_count"), output_field=IntegerField())
        ).annotate(
            meal_price=Case(
                When(canteen_yearly_meal_count__gt=0, then=F("value_total_ht") / F("canteen_yearly_meal_count")),
                default=None,
            )
        )

    def exclude_aberrant_values(self):
        """
        Ici nous supprimons les TD dont les déclarations paraissent erronées et sont impactantes.
        1) Coût denrées existe et > 20 euros ET valeur d'achat alimentaires > 1 million d'euros
        Dans le cas particulier où le nombre de repas annuel n'est pas renseigné,
        nous laissons la TD même si la valeur alimentaire est > 1 million d'euros)
        2) Durant la campagne 2023, nous avons aussi identifié deux TD dont les valeurs étaient aberrantes.
        """
        return (
            self.with_meal_price()
            .exclude(meal_price__isnull=False, meal_price__gt=20, value_total_ht__gt=1000000)
            .exclude(year=2022, teledeclaration_id__in=[9656, 8037])
        )

    def canteen_not_deleted_during_campaign(self, year):
        year = int(year)
        return self.exclude(
            canteen__deletion_date__range=(
                CAMPAIGN_DATES[year]["teledeclaration_start_date"],
                CAMPAIGN_DATES[year]["teledeclaration_end_date"],
            )
        )

    def canteen_has_siret_or_siren_unite_legale(self):
        return self.annotate(
            canteen_siret=F("canteen_snapshot__siret"),
            canteen_siren_unite_legale=F("canteen_snapshot__siren_unite_legale"),
        ).filter(
            ~Q(canteen_siret=None) & ~Q(canteen_siret="")
            | ~Q(canteen_siren_unite_legale=None) & ~Q(canteen_siren_unite_legale="")
        )

    def canteen_for_stat(self, year):
        return (
            self.select_related("canteen")
            .exclude(canteen_id__isnull=True)
            .canteen_not_deleted_during_campaign(year)  # Chaîne de traitement n°6
            .canteen_has_siret_or_siren_unite_legale()  # Chaîne de traitement n°7
        )

    def valid_td_by_year(self, year):
        year = int(year)
        if year in CAMPAIGN_DATES.keys():
            return (
                self.teledeclared_for_year(year)
                .exclude(teledeclaration_mode="SATELLITE_WITHOUT_APPRO")
                .filter(value_bio_ht_agg__isnull=False)  # Chaîne de traitement n°5
                .canteen_for_stat(year)  # Chaîne de traitement n°6 & n°7
                .exclude_aberrant_values()  # Chaîne de traitement n°8
            )
        else:
            return self.none()

    def historical_valid_td(self, years: list):
        results = self.none()
        for year in years:
            results = results | self.valid_td_by_year(year)
        return results.select_related("canteen")

    def publicly_visible(self):
        return self.exclude(canteen__line_ministry=Canteen.Ministries.ARMEE)

    def with_appro_percent_stats(self):
        """
        Note: we use Sum/default instead of F to better manage None values.
        """
        return self.annotate(
            bio_percent=100 * Sum("value_bio_ht_agg", default=0) / Sum("value_total_ht"),
            egalim_percent=100 * F("value_egalim_ht_agg") / Sum("value_total_ht"),
        )

    def egalim_objectives_reached(self):
        return self.filter(
            Q(
                bio_percent__gte=EGALIM_OBJECTIVES["hexagone"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["hexagone"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_OBJECTIVES["groupe_1"]["region_list"],
                bio_percent__gte=EGALIM_OBJECTIVES["groupe_1"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["groupe_1"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_OBJECTIVES["groupe_2"]["region_list"],
                bio_percent__gte=EGALIM_OBJECTIVES["groupe_2"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["groupe_2"]["egalim_percent"],
            )
            | Q(
                canteen__region__in=EGALIM_OBJECTIVES["groupe_3"]["region_list"],
                bio_percent__gte=EGALIM_OBJECTIVES["groupe_3"]["bio_percent"],
                egalim_percent__gte=EGALIM_OBJECTIVES["groupe_3"]["egalim_percent"],
            )
        )


class Diagnostic(models.Model):
    class Meta:
        verbose_name = "diagnostic"
        verbose_name_plural = "diagnostics"
        constraints = [
            models.UniqueConstraint(fields=["canteen", "year"], name="annual_diagnostic"),
        ]

    class DiagnosticStatus(models.TextChoices):
        DRAFT = "DRAFT", "Brouillon"
        SUBMITTED = "SUBMITTED", "Télédéclaré"
        # CANCELLED = "CANCELLED", "Annulé"

    # NB: if the label of the choice changes, double check that the teledeclaration PDF
    # doesn't need an update as well, since the logic in the templates is based on the label
    class DiagnosticType(models.TextChoices):
        SIMPLE = "SIMPLE", "Télédeclaration simple"
        COMPLETE = "COMPLETE", "Télédeclaration détaillée"

    class CentralKitchenDiagnosticMode(models.TextChoices):
        APPRO = (
            "APPRO",
            "Ce diagnostic concerne les données d'approvisionnement de tous les restaurants satellites",
        )
        ALL = "ALL", "Ce diagnostic concerne toutes les données des restaurants satellites"

    class ServiceType(models.TextChoices):
        UNIQUE = "UNIQUE", "Menu unique"
        MULTIPLE_SELF = "MULTIPLE_SELF", "Choix multiple en libre-service"
        MULTIPLE_RESERVATION = "MULTIPLE_RESERVATION", "Choix multiple avec réservation à l’avance au jour le jour"

    class VegetarianMenuFrequency(models.TextChoices):
        NEVER = "NEVER", "Jamais"
        LOW = "LOW", "Moins d'une fois par semaine"
        MID = "MID", "Une fois par semaine"
        HIGH = "HIGH", "Plus d'une fois par semaine"
        DAILY = "DAILY", "De façon quotidienne"

    class VegetarianMenuType(models.TextChoices):
        UNIQUE = "UNIQUE", "Un menu végétarien en plat unique, sans choix"
        SEVERAL = (
            "SEVERAL",
            "Un menu végétarien composé de plusieurs choix de plats végétariens",
        )
        ALTERNATIVES = (
            "ALTERNATIVES",
            "Un menu végétarien au choix, en plus d'autres plats non végétariens",
        )

    class CommunicationType(models.TextChoices):
        EMAIL = "EMAIL", "Envoi d'e-mail aux convives ou à leurs représentants"
        DISPLAY = "DISPLAY", "Par affichage sur le lieu de restauration"
        WEBSITE = "WEBSITE", "Sur site internet ou intranet (mairie, cantine)"
        OTHER = "OTHER", "Autres moyens d'affichage et de communication électronique"
        DIGITAL = "DIGITAL", "Par voie électronique"

    class CommunicationFrequency(models.TextChoices):
        REGULARLY = "REGULARLY", "Régulièrement au cours de l’année"
        YEARLY = "YEARLY", "Une fois par an"
        LESS_THAN_YEARLY = "LESS_THAN_YEARLY", "Moins d'une fois par an"

    class WasteActions(models.TextChoices):
        INSCRIPTION = "INSCRIPTION", "Pré-inscription des convives obligatoire"
        AWARENESS = "AWARENESS", "Sensibilisation par affichage ou autre média"
        TRAINING = "TRAINING", "Formation / information du personnel de restauration"
        DISTRIBUTION = (
            "DISTRIBUTION",
            "Réorganisation de la distribution des composantes du repas",
        )
        PORTIONS = "PORTIONS", "Choix des portions (grande faim, petite faim)"
        REUSE = "REUSE", "Réutilisation des restes de préparation / surplus"

    class DiversificationPlanActions(models.TextChoices):
        PRODUCTS = (
            "PRODUCTS",
            "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
        )
        PRESENTATION = (
            "PRESENTATION",
            "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
        )
        MENU = (
            "MENU",
            "Agir sur la manière dont les menus sont conçus ces plats en soulignant leurs attributs positifs",
        )
        PROMOTION = (
            "PROMOTION",
            "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
        )
        TRAINING = (
            "TRAINING",
            "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
        )

    class VegetarianMenuBase(models.TextChoices):
        GRAIN = "GRAIN", "De céréales et/ou les légumes secs (hors soja)"
        SOY = "SOY", "De soja"
        CHEESE = "CHEESE", "De fromage"
        EGG = "EGG", "D’œufs"
        READYMADE = "READYMADE", "Plats prêts à l'emploi"

    class TeledeclarationMode(models.TextChoices):
        SATELLITE_WITHOUT_APPRO = (
            "SATELLITE_WITHOUT_APPRO",
            "Restaurant satellite dont les données d'appro sont déclarées par la cuisine centrale",
        )
        CENTRAL_APPRO = (
            "CENTRAL_APPRO",
            "Cuisine centrale déclarant les données d'appro pour ses restaurants satellites",
        )
        CENTRAL_ALL = (
            "CENTRAL_ALL",
            "Cuisine centrale déclarant toutes les données EGalim pour ses restaurants satellites",
        )
        SITE = "SITE", "Cantine déclarant ses propres données"

    APPRO_FAMILIES = [
        "viandes_volailles",
        "produits_de_la_mer",
        "fruits_et_legumes",
        "charcuterie",
        "produits_laitiers",
        "boulangerie",
        "boissons",
        "autres",
    ]

    APPRO_LABELS_EGALIM = [
        "bio",
        # "bio_dont_commerce_equitable",
        "label_rouge",
        "aocaop_igp_stg",
        "hve",
        "peche_durable",
        "rup",
        "commerce_equitable",
        "fermier",
        "externalites",
        "performance",
    ]
    APPRO_LABELS_NON_EGALIM = [
        "non_egalim",
    ]
    APPRO_LABELS_FRANCE = [
        "france",
        "short_distribution",
        "local",
    ]
    APPRO_LABELS = APPRO_LABELS_EGALIM + APPRO_LABELS_NON_EGALIM
    APPRO_LABELS_GROUPS_MAPPING = {
        "bio": ["bio"],
        "sustainable": ["label_rouge", "aocaop_igp_stg"],
        "externality_performance": ["externalites", "performance"],
        "egalim_others": ["hve", "peche_durable", "rup", "commerce_equitable", "fermier"],
    }
    APPRO_LABELS_GROUPS_GROUPS_MAPPING = {
        "egalim_hors_bio": ["sustainable", "externality_performance", "egalim_others"],
        "egalim": ["bio", "sustainable", "externality_performance", "egalim_others"],
    }

    SIMPLE_APPRO_FIELDS = [
        "value_total_ht",
        "value_bio_ht",
        "value_bio_dont_commerce_equitable_ht",
        "value_sustainable_ht",
        "value_externality_performance_ht",
        "value_egalim_others_ht",
        "value_commerce_equitable_ht",
        "value_meat_poultry_ht",
        "value_meat_poultry_egalim_ht",
        "value_meat_poultry_france_ht",
        "value_fish_ht",
        "value_fish_egalim_ht",
    ]
    # TODO: clean up when updating the imports
    SIMPLE_APPRO_FIELDS_FOR_IMPORT = [
        field_name for field_name in SIMPLE_APPRO_FIELDS if "commerce_equitable" not in field_name
    ]

    AGGREGATED_APPRO_FIELDS = [
        "value_bio_ht_agg",
        "value_sustainable_ht_agg",
        "value_externality_performance_ht_agg",
        "value_egalim_others_ht_agg",
        # "value_egalim_hors_bio_ht_agg",
        # "value_egalim_ht_agg",
    ]

    APPRO_FIELDS = [
        "value_viandes_volailles_bio",
        "value_viandes_volailles_bio_dont_commerce_equitable",
        "value_produits_de_la_mer_bio",
        "value_produits_de_la_mer_bio_dont_commerce_equitable",
        "value_fruits_et_legumes_bio",
        "value_fruits_et_legumes_bio_dont_commerce_equitable",
        "value_charcuterie_bio",
        "value_charcuterie_bio_dont_commerce_equitable",
        "value_produits_laitiers_bio",
        "value_produits_laitiers_bio_dont_commerce_equitable",
        "value_boulangerie_bio",
        "value_boulangerie_bio_dont_commerce_equitable",
        "value_boissons_bio",
        "value_boissons_bio_dont_commerce_equitable",
        "value_autres_bio",
        "value_autres_bio_dont_commerce_equitable",
        "value_viandes_volailles_label_rouge",
        "value_produits_de_la_mer_label_rouge",
        "value_fruits_et_legumes_label_rouge",
        "value_charcuterie_label_rouge",
        "value_produits_laitiers_label_rouge",
        "value_boulangerie_label_rouge",
        "value_boissons_label_rouge",
        "value_autres_label_rouge",
        "value_viandes_volailles_aocaop_igp_stg",
        "value_produits_de_la_mer_aocaop_igp_stg",
        "value_fruits_et_legumes_aocaop_igp_stg",
        "value_charcuterie_aocaop_igp_stg",
        "value_produits_laitiers_aocaop_igp_stg",
        "value_boulangerie_aocaop_igp_stg",
        "value_boissons_aocaop_igp_stg",
        "value_autres_aocaop_igp_stg",
        "value_viandes_volailles_hve",
        "value_produits_de_la_mer_hve",
        "value_fruits_et_legumes_hve",
        "value_charcuterie_hve",
        "value_produits_laitiers_hve",
        "value_boulangerie_hve",
        "value_boissons_hve",
        "value_autres_hve",
        "value_viandes_volailles_peche_durable",
        "value_produits_de_la_mer_peche_durable",
        "value_fruits_et_legumes_peche_durable",
        "value_charcuterie_peche_durable",
        "value_produits_laitiers_peche_durable",
        "value_boulangerie_peche_durable",
        "value_boissons_peche_durable",
        "value_autres_peche_durable",
        "value_viandes_volailles_rup",
        "value_produits_de_la_mer_rup",
        "value_fruits_et_legumes_rup",
        "value_charcuterie_rup",
        "value_produits_laitiers_rup",
        "value_boulangerie_rup",
        "value_boissons_rup",
        "value_autres_rup",
        "value_viandes_volailles_commerce_equitable",
        "value_produits_de_la_mer_commerce_equitable",
        "value_fruits_et_legumes_commerce_equitable",
        "value_charcuterie_commerce_equitable",
        "value_produits_laitiers_commerce_equitable",
        "value_boulangerie_commerce_equitable",
        "value_boissons_commerce_equitable",
        "value_autres_commerce_equitable",
        "value_viandes_volailles_fermier",
        "value_produits_de_la_mer_fermier",
        "value_fruits_et_legumes_fermier",
        "value_charcuterie_fermier",
        "value_produits_laitiers_fermier",
        "value_boulangerie_fermier",
        "value_boissons_fermier",
        "value_autres_fermier",
        "value_viandes_volailles_externalites",
        "value_produits_de_la_mer_externalites",
        "value_fruits_et_legumes_externalites",
        "value_charcuterie_externalites",
        "value_produits_laitiers_externalites",
        "value_boulangerie_externalites",
        "value_boissons_externalites",
        "value_autres_externalites",
        "value_viandes_volailles_performance",
        "value_produits_de_la_mer_performance",
        "value_fruits_et_legumes_performance",
        "value_charcuterie_performance",
        "value_produits_laitiers_performance",
        "value_boulangerie_performance",
        "value_boissons_performance",
        "value_autres_performance",
        "value_viandes_volailles_non_egalim",
        "value_produits_de_la_mer_non_egalim",
        "value_fruits_et_legumes_non_egalim",
        "value_charcuterie_non_egalim",
        "value_produits_laitiers_non_egalim",
        "value_boulangerie_non_egalim",
        "value_boissons_non_egalim",
        "value_autres_non_egalim",
        "value_viandes_volailles_france",
        "value_produits_de_la_mer_france",
        "value_fruits_et_legumes_france",
        "value_charcuterie_france",
        "value_produits_laitiers_france",
        "value_boulangerie_france",
        "value_boissons_france",
        "value_autres_france",
        "value_viandes_volailles_short_distribution",
        "value_produits_de_la_mer_short_distribution",
        "value_fruits_et_legumes_short_distribution",
        "value_charcuterie_short_distribution",
        "value_produits_laitiers_short_distribution",
        "value_boulangerie_short_distribution",
        "value_boissons_short_distribution",
        "value_autres_short_distribution",
        "value_viandes_volailles_local",
        "value_produits_de_la_mer_local",
        "value_fruits_et_legumes_local",
        "value_charcuterie_local",
        "value_produits_laitiers_local",
        "value_boulangerie_local",
        "value_boissons_local",
        "value_autres_local",
    ]
    # TODO: clean up when updating the imports
    APPRO_FIELDS_FOR_IMPORT = [
        field_name for field_name in APPRO_FIELDS if "bio_dont_commerce_equitable" not in field_name
    ]

    COMPLETE_APPRO_FIELDS = ["value_total_ht", "value_meat_poultry_ht", "value_fish_ht"] + APPRO_FIELDS

    WASTE_FIELDS = [
        "has_waste_diagnostic",
        "has_waste_plan",
        "waste_actions",
        "other_waste_action",
        "has_donation_agreement",
        "has_waste_measures",
        "total_leftovers",
        "duration_leftovers_measurement",
        "bread_leftovers",
        "served_leftovers",
        "unserved_leftovers",
        "side_leftovers",
        "donation_frequency",
        "donation_quantity",
        "donation_food_type",
        "other_waste_comments",
    ]

    DIVERSIFICATION_FIELDS = [
        "has_diversification_plan",
        "diversification_plan_actions",
        "service_type",
        "vegetarian_weekly_recurrence",
        "vegetarian_menu_type",
        "vegetarian_menu_bases",
    ]

    PLASTIC_FIELDS = [
        "cooking_plastic_substituted",
        "serving_plastic_substituted",
        "plastic_bottles_substituted",
        "plastic_tableware_substituted",
    ]

    INFO_FIELDS = [
        "communication_supports",
        "other_communication_support",
        "communication_support_url",
        "communicates_on_food_plan",
        "communicates_on_food_quality",
        "communication_frequency",
    ]

    NON_APPRO_FIELDS = WASTE_FIELDS + DIVERSIFICATION_FIELDS + PLASTIC_FIELDS + INFO_FIELDS

    META_FIELDS = [
        "id",
        "canteen_id",
        "year",
        "diagnostic_type",
        "central_kitchen_diagnostic_mode",
        "is_teledeclared",
        "is_filled",
    ]

    CREATION_META_FIELDS = [
        "creation_date",
        "modification_date",
        "creation_source",
    ]

    MATOMO_FIELDS = [
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
    ]

    TUNNEL_PROGRESS_FIELDS = [
        "tunnel_appro",
        "tunnel_waste",
        "tunnel_diversification",
        "tunnel_plastic",
        "tunnel_info",
    ]

    TELEDECLARATION_FIELDS = [
        "teledeclaration_date",
        "teledeclaration_mode",
        "teledeclaration_version",
        "teledeclaration_id",
    ]
    TELEDECLARATION_SNAPSHOT_FIELDS = [
        "canteen_snapshot",
        "satellites_snapshot",
        "applicant_snapshot",
    ]

    objects = models.Manager.from_queryset(DiagnosticQuerySet)()

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(excluded_fields=["canteen_snapshot", "satellites_snapshot", "applicant_snapshot"])

    canteen = models.ForeignKey(Canteen, on_delete=models.SET_NULL, null=True, verbose_name="cantine")

    year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="année",
    )

    status = models.CharField(
        max_length=255,
        choices=DiagnosticStatus.choices,
        default=DiagnosticStatus.DRAFT,
        verbose_name="status",
    )

    creation_source = models.CharField(
        max_length=255,
        choices=CreationSource.choices,
        blank=True,
        null=True,
        verbose_name="Source de création du diagnostic",
    )

    diagnostic_type = models.CharField(
        max_length=255,
        choices=DiagnosticType.choices,
        blank=True,
        null=True,
        verbose_name="Type de diagnostic (simplifié, détaillé)",
    )

    # Relevant only for central cuisines
    central_kitchen_diagnostic_mode = models.CharField(
        max_length=255,
        choices=CentralKitchenDiagnosticMode.choices,
        blank=True,
        null=True,
        verbose_name="seulement pertinent pour les cuisines centrales : Quelles données sont déclarées par cette cuisine centrale ?",
    )

    # progress fields
    # NB None = tunnel has not been started; "complet" = tunnel has finished
    # all other values are defined by the front end
    tunnel_appro = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel appro",
    )
    tunnel_waste = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel anti-gaspi",
    )
    tunnel_diversification = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel diversification",
    )
    tunnel_plastic = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel anti-plastique",
    )
    tunnel_info = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Progrès tunnel information convives",
    )

    # Product origin
    value_total_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale annuelle HT",
    )
    value_bio_ht = make_optional_positive_decimal_field(
        verbose_name="Bio - Valeur annuelle HT",
    )
    value_bio_dont_commerce_equitable_ht = make_optional_positive_decimal_field(
        verbose_name="Bio dont commerce équitable - Valeur annuelle HT",
    )
    value_fair_trade_ht = make_optional_positive_decimal_field(  # legacy
        verbose_name="Commerce équitable - Valeur annuelle HT",
    )
    value_sustainable_ht = make_optional_positive_decimal_field(
        verbose_name="Produits SIQO (hors bio) - Valeur annuelle HT",
    )
    value_pat_ht = make_optional_positive_decimal_field(  # legacy
        verbose_name="Produits dans le cadre de Projects Alimentaires Territoriaux - Valeur annuelle HT",
    )
    value_externality_performance_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) prenant en compte les coûts imputés aux externalités environnementales ou leurs performances en matière environnementale",
    )
    value_egalim_others_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) des autres achats EGalim",
    )
    value_commerce_equitable_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) des achats commerce équitable (hors bio)",
    )
    value_meat_poultry_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées",
    )
    value_meat_poultry_egalim_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim",
    )
    value_meat_poultry_france_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France",
    )
    value_fish_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) poissons et produits aquatiques",
    )
    value_fish_egalim_ht = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) poissons et produits aquatiques EGalim",
    )

    value_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Valeur label rouge",
    )
    value_label_aoc_igp = make_optional_positive_decimal_field(
        verbose_name="Valeur label AOC/AOP/IGP",
    )
    value_label_hve = make_optional_positive_decimal_field(
        verbose_name="Valeur label HVE",
    )

    # Food waste
    has_waste_diagnostic = models.BooleanField(
        blank=True, null=True, verbose_name="diagnostic sur le gaspillage réalisé"
    )
    has_waste_plan = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="plan d'action contre le gaspillage en place",
    )
    waste_actions = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=WasteActions.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions contre le gaspillage en place",
    )
    other_waste_action = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre action contre le gaspillage alimentaire",
    )
    has_donation_agreement = models.BooleanField(blank=True, null=True, verbose_name="propose des dons alimentaires")
    has_waste_measures = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="réalise des mesures de gaspillage alimentaire",
    )
    # _leftovers fields no longer in use since waste measurement feature
    total_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        blank=True,
        null=True,
        verbose_name="total des déchets alimentaires (t)",
    )
    duration_leftovers_measurement = models.IntegerField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(365)],
        verbose_name="période de mesure (jours)",
    )
    bread_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de pain kg/an",
    )
    served_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste plateau kg/an",
    )
    unserved_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste en production (non servi) kg/an",
    )
    side_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de composantes kg/an",
    )
    donation_frequency = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="fréquence de dons dons/an",
    )
    donation_quantity = make_optional_positive_decimal_field(
        verbose_name="quantité des denrées données kg/an",
    )
    donation_food_type = models.TextField(
        null=True,
        blank=True,
        verbose_name="type de denrées données",
    )
    other_waste_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="autres commentaires (gaspillage)",
    )

    # Vegetarian menus
    has_diversification_plan = models.BooleanField(
        blank=True, null=True, verbose_name="plan de diversification en place"
    )
    diversification_plan_actions = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=DiversificationPlanActions.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions inclus dans le plan de diversification des protéines",
    )
    service_type = models.CharField(
        max_length=255,
        choices=ServiceType.choices,
        null=True,
        blank=True,
        verbose_name="type de service",
    )
    vegetarian_weekly_recurrence = models.CharField(
        max_length=255,
        choices=VegetarianMenuFrequency.choices,
        null=True,
        blank=True,
        verbose_name="Menus végétariens par semaine",
    )
    vegetarian_menu_type = models.CharField(
        max_length=255,
        choices=VegetarianMenuType.choices,
        blank=True,
        null=True,
        verbose_name="Menu végétarien proposé",
    )
    vegetarian_menu_bases = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=VegetarianMenuBase.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="bases de menu végétarien",
    )

    # Plastic replacement
    cooking_plastic_substituted = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de cuisson en plastique remplacés",
    )
    serving_plastic_substituted = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de service en plastique remplacés",
    )
    plastic_bottles_substituted = models.BooleanField(
        blank=True, null=True, verbose_name="bouteilles en plastique remplacées"
    )
    plastic_tableware_substituted = models.BooleanField(
        blank=True, null=True, verbose_name="ustensils en plastique remplacés"
    )

    # Information and communication
    communication_supports = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=CommunicationType.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Communication utilisée",
    )
    other_communication_support = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre communication utilisée",
    )
    communication_support_url = models.URLField(blank=True, null=True, verbose_name="Lien de communication")
    communicates_on_food_plan = models.BooleanField(
        blank=True, null=True, verbose_name="Communique sur le plan alimentaire"
    )
    communicates_on_food_quality = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Communique sur les démarches qualité/durables/équitables",
    )
    communication_frequency = models.CharField(
        max_length=255,
        choices=CommunicationFrequency.choices,
        blank=True,
        null=True,
        verbose_name="fréquence de communication",
    )

    # Campaign tracking
    creation_mtm_source = models.TextField(
        null=True,
        blank=True,
        verbose_name="mtm_source du lien tracké lors de la création",
    )
    creation_mtm_campaign = models.TextField(
        null=True,
        blank=True,
        verbose_name="mtm_campaign du lien tracké lors de la création",
    )
    creation_mtm_medium = models.TextField(
        null=True,
        blank=True,
        verbose_name="mtm_medium du lien tracké lors de la création",
    )

    # aggregated values
    value_bio_ht_agg = make_optional_positive_decimal_field(
        verbose_name="Bio - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    value_sustainable_ht_agg = make_optional_positive_decimal_field(
        verbose_name="Produits SIQO (hors bio) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    value_externality_performance_ht_agg = make_optional_positive_decimal_field(
        verbose_name="Externalité/performance - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)",
    )
    value_egalim_others_ht_agg = make_optional_positive_decimal_field(
        verbose_name="Autres achats EGalim - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    value_egalim_hors_bio_ht_agg = make_optional_positive_decimal_field(
        verbose_name="EGalim (Produits SIQO (hors bio) + Externalité/performance + Autres achats EGalim) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    value_egalim_ht_agg = make_optional_positive_decimal_field(
        verbose_name="EGalim (Bio + Produits SIQO (hors bio) + Externalité/performance + Autres achats EGalim) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )

    # detailed values
    value_viandes_volailles_bio = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Bio",
    )
    value_viandes_volailles_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Bio dont commerce équitable",
    )
    value_produits_de_la_mer_bio = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Bio",
    )
    value_produits_de_la_mer_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Bio dont commerce équitable",
    )
    value_fruits_et_legumes_bio = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Bio",
    )
    value_fruits_et_legumes_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Bio dont commerce équitable",
    )
    value_charcuterie_bio = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Bio",
    )
    value_charcuterie_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Bio dont commerce équitable",
    )
    value_produits_laitiers_bio = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Bio",
    )
    value_produits_laitiers_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Bio dont commerce équitable",
    )
    value_boulangerie_bio = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Bio",
    )
    value_boulangerie_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Bio dont commerce équitable",
    )
    value_boissons_bio = make_optional_positive_decimal_field(
        verbose_name="Boissons, Bio",
    )
    value_boissons_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Bio dont commerce équitable",
    )
    value_autres_bio = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Bio",
    )
    value_autres_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Bio dont commerce équitable",
    )
    value_viandes_volailles_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Label rouge",
    )
    value_produits_de_la_mer_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Label rouge",
    )
    value_fruits_et_legumes_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Label rouge",
    )
    value_charcuterie_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Label rouge",
    )
    value_produits_laitiers_label_rouge = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Label rouge",
    )
    value_boulangerie_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Label rouge",
    )
    value_boissons_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Boissons, Label rouge",
    )
    value_autres_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Label rouge",
    )
    value_viandes_volailles_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, AOC / AOP / IGP / STG",
    )
    value_produits_de_la_mer_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, AOC / AOP / IGP / STG",
    )
    value_fruits_et_legumes_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, AOC / AOP / IGP / STG",
    )
    value_charcuterie_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, AOC / AOP / IGP / STG",
    )
    value_produits_laitiers_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), AOC / AOP / IGP / STG",
    )
    value_boulangerie_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, AOC / AOP / IGP / STG",
    )
    value_boissons_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Boissons, AOC / AOP / IGP / STG",
    )
    value_autres_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, AOC / AOP / IGP / STG",
    )
    value_viandes_volailles_hve = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Haute valeur environnementale",
    )
    value_produits_de_la_mer_hve = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Haute valeur environnementale",
    )
    value_fruits_et_legumes_hve = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Haute valeur environnementale",
    )
    value_charcuterie_hve = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Haute valeur environnementale",
    )
    value_produits_laitiers_hve = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Haute valeur environnementale",
    )
    value_boulangerie_hve = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Haute valeur environnementale",
    )
    value_boissons_hve = make_optional_positive_decimal_field(
        verbose_name="Boissons, Haute valeur environnementale",
    )
    value_autres_hve = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Haute valeur environnementale",
    )
    value_viandes_volailles_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Pêche durable",
    )
    value_produits_de_la_mer_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Pêche durable",
    )
    value_fruits_et_legumes_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Pêche durable",
    )
    value_charcuterie_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Pêche durable",
    )
    value_produits_laitiers_peche_durable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Pêche durable",
    )
    value_boulangerie_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Pêche durable",
    )
    value_boissons_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Pêche durable",
    )
    value_autres_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Pêche durable",
    )
    value_viandes_volailles_rup = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Région ultrapériphérique",
    )
    value_produits_de_la_mer_rup = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Région ultrapériphérique",
    )
    value_fruits_et_legumes_rup = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Région ultrapériphérique",
    )
    value_charcuterie_rup = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Région ultrapériphérique",
    )
    value_produits_laitiers_rup = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Région ultrapériphérique",
    )
    value_boulangerie_rup = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Région ultrapériphérique",
    )
    value_boissons_rup = make_optional_positive_decimal_field(
        verbose_name="Boissons, Région ultrapériphérique",
    )
    value_autres_rup = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Région ultrapériphérique",
    )
    value_viandes_volailles_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Commerce équitable",
    )
    value_produits_de_la_mer_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Commerce équitable",
    )
    value_fruits_et_legumes_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Commerce équitable",
    )
    value_charcuterie_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Commerce équitable",
    )
    value_produits_laitiers_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Commerce équitable",
    )
    value_boulangerie_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Commerce équitable",
    )
    value_boissons_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Commerce équitable",
    )
    value_autres_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Commerce équitable",
    )
    value_viandes_volailles_fermier = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Fermier",
    )
    value_produits_de_la_mer_fermier = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Fermier",
    )
    value_fruits_et_legumes_fermier = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Fermier",
    )
    value_charcuterie_fermier = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Fermier",
    )
    value_produits_laitiers_fermier = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Fermier",
    )
    value_boulangerie_fermier = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Fermier",
    )
    value_boissons_fermier = make_optional_positive_decimal_field(
        verbose_name="Boissons, Fermier",
    )
    value_autres_fermier = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Fermier",
    )
    value_viandes_volailles_externalites = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_produits_de_la_mer_externalites = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_fruits_et_legumes_externalites = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_charcuterie_externalites = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_produits_laitiers_externalites = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_boulangerie_externalites = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_boissons_externalites = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_autres_externalites = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_viandes_volailles_performance = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_produits_de_la_mer_performance = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_fruits_et_legumes_performance = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_charcuterie_performance = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_produits_laitiers_performance = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_boulangerie_performance = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_boissons_performance = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_autres_performance = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_viandes_volailles_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, non-EGalim.",
    )
    value_produits_de_la_mer_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, non-EGalim.",
    )
    value_fruits_et_legumes_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, non-EGalim.",
    )
    value_charcuterie_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, non-EGalim.",
    )
    value_produits_laitiers_non_egalim = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), non-EGalim.",
    )
    value_boulangerie_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, non-EGalim.",
    )
    value_boissons_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Boissons, non-EGalim.",
    )
    value_autres_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, non-EGalim.",
    )
    value_viandes_volailles_france = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Provenance France",
    )
    value_produits_de_la_mer_france = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Provenance France",
    )
    value_fruits_et_legumes_france = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Provenance France",
    )
    value_charcuterie_france = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Provenance France",
    )
    value_produits_laitiers_france = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Provenance France",
    )
    value_boulangerie_france = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Provenance France",
    )
    value_boissons_france = make_optional_positive_decimal_field(
        verbose_name="Boissons, Provenance France",
    )
    value_autres_france = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Provenance France",
    )
    value_viandes_volailles_short_distribution = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Circuit-court",
    )
    value_produits_de_la_mer_short_distribution = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Circuit-court",
    )
    value_fruits_et_legumes_short_distribution = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Circuit-court",
    )
    value_charcuterie_short_distribution = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Circuit-court",
    )
    value_produits_laitiers_short_distribution = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Circuit-court",
    )
    value_boulangerie_short_distribution = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Circuit-court",
    )
    value_boissons_short_distribution = make_optional_positive_decimal_field(
        verbose_name="Boissons, Circuit-court",
    )
    value_autres_short_distribution = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Circuit-court",
    )
    value_viandes_volailles_local = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produit local",
    )
    value_produits_de_la_mer_local = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Produit local",
    )
    value_fruits_et_legumes_local = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produit local",
    )
    value_charcuterie_local = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produit local",
    )
    value_produits_laitiers_local = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produit local",
    )
    value_boulangerie_local = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Produit local",
    )
    value_boissons_local = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produit local",
    )
    value_autres_local = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produit local",
    )

    # Télédéclaration
    teledeclaration_date = models.DateTimeField(
        verbose_name="date de télédéclaration",
        blank=True,
        null=True,
    )
    # a TD can use SATELLITE_WITHOUT_APPRO mode, as well as have some appro data of its own if,
    # for example, the manager of the satellite canteen started completing a diagnostic and then the
    # central kitchen decided to declare for its satellites.
    # We are leaving it up to the team to interpret the data in this case.
    teledeclaration_mode = models.CharField(
        verbose_name="mode de télédéclaration",
        max_length=255,
        choices=TeledeclarationMode.choices,
        null=True,
        blank=True,
    )
    teledeclaration_version = models.IntegerField(
        verbose_name="version de la télédéclaration",
        blank=True,
        null=True,
    )
    teledeclaration_id = models.IntegerField(
        verbose_name="ancien identifiant de la télédéclaration (concerne la période 2021-2024)",
        blank=True,
        null=True,
    )
    applicant = models.ForeignKey(
        get_user_model(),
        verbose_name="déclarant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    canteen_snapshot = models.JSONField(
        verbose_name="cantine (copie au moment de la télédéclaration)",
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
    )
    satellites_snapshot = models.JSONField(
        verbose_name="satellites (copie au moment de la télédéclaration)",
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
    )
    applicant_snapshot = models.JSONField(
        verbose_name="déclarant (copie au moment de la télédéclaration)",
        blank=True,
        null=True,
        encoder=CustomJSONEncoder,
    )

    def __str__(self):
        return f"Diagnostic pour {self.canteen.name} ({self.year})"

    def clean(self):
        if self.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
            self.populate_simplified_diagnostic_values()

        validation_errors = utils_utils.merge_validation_errors(
            diagnostic_validators.validate_year(self),
            diagnostic_validators.validate_approvisionment_total(self),
            diagnostic_validators.validate_meat_total(self),
            diagnostic_validators.validate_fish_total(self),
            diagnostic_validators.validate_meat_fish_egalim(self),
        )
        if validation_errors:
            raise ValidationError(validation_errors)

        return super().clean()

    def populate_simplified_diagnostic_values(self):
        self.value_bio_ht = self.label_group_sum("bio")
        self.value_bio_dont_commerce_equitable_ht = self.label_sum("bio_dont_commerce_equitable")
        self.value_sustainable_ht = self.label_group_sum("sustainable")
        self.value_externality_performance_ht = self.label_group_sum("externality_performance")
        self.value_egalim_others_ht = self.label_group_sum("egalim_others")
        self.value_commerce_equitable_ht = self.label_sum("commerce_equitable")

        total_meat_egalim = total_meat_france = total_fish_egalim = 0
        for label in Diagnostic.APPRO_LABELS_EGALIM:
            family = "viandes_volailles"
            # need to do or 0 and not give a default value because the value can be explicitly set to None
            total_meat_egalim = total_meat_egalim + (getattr(self, f"value_{family}_{label}") or 0)

            family = "produits_de_la_mer"
            total_fish_egalim = total_fish_egalim + (getattr(self, f"value_{family}_{label}") or 0)

        for label in Diagnostic.APPRO_LABELS_FRANCE:
            family = "viandes_volailles"
            total_meat_france = total_meat_france + (getattr(self, f"value_{family}_{label}") or 0)

        self.value_meat_poultry_egalim_ht = total_meat_egalim
        self.value_meat_poultry_france_ht = total_meat_france
        self.value_fish_egalim_ht = total_fish_egalim

    def populate_aggregated_values(self):
        self.value_bio_ht_agg = self.label_group_sum("bio")
        self.value_sustainable_ht_agg = self.label_group_sum("sustainable")
        self.value_externality_performance_ht_agg = self.label_group_sum("externality_performance")
        self.value_egalim_others_ht_agg = self.label_group_sum("egalim_others")
        # group_group
        self.value_egalim_hors_bio_ht_agg = self.label_group_group_sum("egalim_hors_bio")
        self.value_egalim_ht_agg = self.label_group_group_sum("egalim")

    def label_sum(self, label: str):
        sum = 0
        is_null = True
        for family in Diagnostic.APPRO_FAMILIES:
            value = getattr(self, f"value_{family}_{label}")
            if value is not None:
                is_null = False
                sum = sum + value
        if not is_null:
            return sum

    def label_group_sum(self, label_group: str):
        if self.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE:
            return sum_int_with_potential_null(
                [self.label_sum(label) for label in Diagnostic.APPRO_LABELS_GROUPS_MAPPING[label_group]]
            )
        return getattr(self, f"value_{label_group}_ht")

    def label_group_group_sum(self, label_group_group: str):
        return sum_int_with_potential_null(
            [
                self.label_group_sum(label_group)
                for label_group in Diagnostic.APPRO_LABELS_GROUPS_GROUPS_MAPPING[label_group_group]
            ]
        )

    def family_sum(self, family: str):
        """
        NOTE: APPRO_LABELS does not include APPRO_LABELS_FRANCE
        """
        sum = 0
        for label in Diagnostic.APPRO_LABELS:
            value = getattr(self, f"value_{family}_{label}")
            if value:
                sum = sum + value
        return sum

    @property
    def is_filled(self):
        return self.value_total_ht > 0 if self.value_total_ht else False

    @property
    def is_teledeclared(self):
        return self.status == Diagnostic.DiagnosticStatus.SUBMITTED

    @property
    def is_teledeclared_by_cc(self):
        return self.teledeclaration_mode and self.teledeclaration_mode in [
            Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO,
            Diagnostic.TeledeclarationMode.CENTRAL_APPRO,
            Diagnostic.TeledeclarationMode.CENTRAL_ALL,
        ]

    @property
    def latest_submitted_teledeclaration(self):
        submitted_teledeclarations = self.teledeclaration_set.submitted()
        if submitted_teledeclarations.count() == 0:
            return None
        return submitted_teledeclarations.order_by("-creation_date").first()

    @property
    def appro_badge(self) -> bool | None:
        total = self.value_total_ht
        if total:
            bio_percent = (self.value_bio_ht or 0) / total
            egalim_sum = (
                (self.value_bio_ht or 0)
                + (self.value_sustainable_ht or 0)
                + (self.value_externality_performance_ht or 0)
                + (self.value_egalim_others_ht or 0)
            )
            egalim_percent = egalim_sum / total

            bio_threshold = EGALIM_OBJECTIVES["hexagone"]["bio_percent"]
            combined_threshold = EGALIM_OBJECTIVES["hexagone"]["egalim_percent"]
            if self.canteen.region in EGALIM_OBJECTIVES["groupe_1"]["region_list"]:
                bio_threshold = EGALIM_OBJECTIVES["groupe_1"]["bio_percent"]
                combined_threshold = EGALIM_OBJECTIVES["groupe_1"]["egalim_percent"]
            elif self.canteen.region in EGALIM_OBJECTIVES["groupe_2"]["region_list"]:
                bio_threshold = EGALIM_OBJECTIVES["groupe_2"]["bio_percent"]
                combined_threshold = EGALIM_OBJECTIVES["groupe_2"]["egalim_percent"]
            elif self.canteen.region in EGALIM_OBJECTIVES["groupe_3"]["region_list"]:
                bio_threshold = EGALIM_OBJECTIVES["groupe_3"]["bio_percent"]
                combined_threshold = EGALIM_OBJECTIVES["groupe_3"]["egalim_percent"]

            # * 100 to get around floating point errors when we are on the cusp
            if bio_percent * 100 >= bio_threshold and egalim_percent * 100 >= combined_threshold:
                return True
        if self.tunnel_appro:
            return False

    @property
    def waste_badge(self) -> bool | None:
        if self.has_waste_diagnostic and self.waste_actions and len(self.waste_actions) > 0:
            if self.has_donation_agreement or (self.canteen.daily_meal_count and self.canteen.daily_meal_count < 3000):
                return True
        if self.tunnel_waste:
            return False

    @property
    def diversification_badge(self) -> bool | None:
        has_daily_frequency = self.vegetarian_weekly_recurrence == Diagnostic.VegetarianMenuFrequency.DAILY
        has_weekly_or_more_frequency = self.vegetarian_weekly_recurrence in [
            Diagnostic.VegetarianMenuFrequency.DAILY,
            Diagnostic.VegetarianMenuFrequency.MID,
            Diagnostic.VegetarianMenuFrequency.HIGH,
        ]
        # Only the canteens is in the administration sector must have a daily frequency
        if self.canteen.in_administration and has_daily_frequency:
            return True
        if not self.canteen.in_administration and has_weekly_or_more_frequency:
            return True
        if self.tunnel_diversification:
            return False

    @property
    def plastic_badge(self) -> bool | None:
        if (
            self.cooking_plastic_substituted
            and self.serving_plastic_substituted
            and self.plastic_bottles_substituted
            and self.plastic_tableware_substituted
        ):
            return True
        if self.tunnel_plastic:
            return False

    @property
    def info_badge(self) -> bool | None:
        if self.communicates_on_food_quality:
            return True
        if self.tunnel_info:
            return False

    def _should_use_central_kitchen_appro(self):
        if self.canteen.is_satellite and self.canteen.central_producer_siret:
            try:
                central_kitchen = Canteen.objects.get(siret=self.canteen.central_producer_siret)
                existing_diagnostic = central_kitchen.diagnostic_set.get(year=self.year)
                handles_satellite_data = existing_diagnostic.central_kitchen_diagnostic_mode in [
                    Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                    Diagnostic.CentralKitchenDiagnosticMode.ALL,
                ]
                return central_kitchen.is_central_cuisine and handles_satellite_data
            except (Canteen.DoesNotExist, Canteen.MultipleObjectsReturned, Diagnostic.DoesNotExist):
                pass
        return False

    def _get_teledeclaration_mode(self):
        uses_central_kitchen_appro = self._should_use_central_kitchen_appro()
        if uses_central_kitchen_appro:
            return Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO
        if self.canteen.is_central_cuisine:
            if self.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.ALL:
                return Diagnostic.TeledeclarationMode.CENTRAL_ALL
            if self.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO:
                return Diagnostic.TeledeclarationMode.CENTRAL_APPRO
        return Diagnostic.TeledeclarationMode.SITE

    def teledeclare(self, applicant):
        """
        Teledeclare the diagnostic
        """
        if not is_in_teledeclaration_or_correction():
            raise ValidationError("Ce n'est pas possible de télédéclarer hors de la période de la campagne")
        if not is_in_teledeclaration_or_correction(self.year):
            raise ValidationError("Ce diagnostic n'est pas dans la bonne année de télédéclaration")
        if self.is_teledeclared:
            raise ValidationError("Ce diagnostic a déjà été télédéclaré")
        if not self.is_filled:
            raise ValidationError("Ce diagnostic n'est pas rempli")

        from api.serializers import CanteenTeledeclarationSerializer, SatelliteTeledeclarationSerializer

        # canteen data
        serialized_canteen = CanteenTeledeclarationSerializer(self.canteen).data
        self.canteen_snapshot = serialized_canteen

        # satellites data
        if self.canteen.is_central_cuisine:
            serialized_satellites = [SatelliteTeledeclarationSerializer(x).data for x in self.canteen.satellites]
            self.satellites_snapshot = serialized_satellites

        # applicant data
        self.applicant = applicant
        self.applicant_snapshot = {
            "id": applicant.id,
            "name": applicant.get_full_name(),
            "email": applicant.email,
        }

        # aggregated data
        # TODO: compute on save() instead
        self.populate_aggregated_values()

        # metadata
        self.status = Diagnostic.DiagnosticStatus.SUBMITTED
        self.teledeclaration_date = timezone.now()
        self.teledeclaration_mode = self._get_teledeclaration_mode()
        self.teledeclaration_version = TELEDECLARATION_CURRENT_VERSION

        # save
        self.save()

    def cancel(self):
        """
        Cancel the teledeclared diagnostic
        """
        if not is_in_teledeclaration_or_correction():
            raise ValidationError(
                "Ce n'est pas possible d'annuler une télédéclaration hors de la période de la campagne"
            )
        if not is_in_teledeclaration_or_correction(self.year):
            raise ValidationError("Ce diagnostic n'est pas dans la bonne année de télédéclaration")
        if not self.is_teledeclared:
            raise ValidationError("Ce diagnostic doit avoir été télédéclaré")

        self.status = Diagnostic.DiagnosticStatus.DRAFT
        self.applicant = None
        self.teledeclaration_date = None
        self.teledeclaration_mode = None
        self.teledeclaration_version = None

        self.save()
