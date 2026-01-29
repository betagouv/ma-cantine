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


def diagnostic_type_simple_query():
    return Q(diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)


def diagnostic_type_complete_query():
    return Q(diagnostic_type=Diagnostic.DiagnosticType.COMPLETE)


def valeur_totale_is_filled_query():
    return Q(valeur_totale__isnull=False) & ~Q(valeur_totale=0)


def diagnostic_type_simple_is_filled_query():
    """
    - common checks: diagnostic_type & valeur_totale
    - before/after 2025: required fields change
    """
    before_2025 = Q(year__lt=2025) & Q(
        **{f"{field}__isnull": False for field in Diagnostic.APPRO_FIELDS_REQUIRED_BEFORE_2025}
    )
    after_2025 = Q(year__gte=2025) & Q(
        **{f"{field}__isnull": False for field in Diagnostic.SIMPLE_APPRO_FIELDS_REQUIRED_2025}
    )
    return diagnostic_type_simple_query() & valeur_totale_is_filled_query() & (before_2025 | after_2025)


def diagnostic_type_complete_is_filled_query():
    """
    - common checks: diagnostic_type & valeur_totale
    - before/after 2025: required fields change
    """
    before_2025 = Q(year__lt=2025) & Q(
        **{f"{field}__isnull": False for field in Diagnostic.APPRO_FIELDS_REQUIRED_BEFORE_2025}
    )
    after_2025 = Q(year__gte=2025) & Q(
        **{f"{field}__isnull": False for field in Diagnostic.COMPLETE_APPRO_FIELDS_REQUIRED_2025}
    )
    return diagnostic_type_complete_query() & valeur_totale_is_filled_query() & (before_2025 | after_2025)


class DiagnosticQuerySet(models.QuerySet):
    def filled(self):
        return self.filter(diagnostic_type_simple_is_filled_query() | diagnostic_type_complete_is_filled_query())

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
                When(canteen_yearly_meal_count__gt=0, then=F("valeur_totale") / F("canteen_yearly_meal_count")),
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
            .exclude(meal_price__isnull=False, meal_price__gt=20, valeur_totale__gt=1000000)
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
                .exclude(teledeclaration_mode=Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO)
                .filter(valeur_bio_agg__isnull=False)  # Chaîne de traitement n°5
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
        return self.exclude(canteen__production_type=Canteen.ProductionType.GROUPE).exclude(
            canteen__line_ministry=Canteen.Ministries.ARMEE
        )

    def with_appro_percent_stats(self):
        """
        Note: we use Sum/default instead of F to better manage None values.
        """
        return self.annotate(
            bio_percent=100 * Sum("valeur_bio_agg", default=0) / Sum("valeur_totale"),
            egalim_percent=100 * F("valeur_egalim_agg") / Sum("valeur_totale"),
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
        "circuit_court",
        "local",
    ]
    APPRO_LABELS = APPRO_LABELS_EGALIM + APPRO_LABELS_NON_EGALIM
    APPRO_LABELS_ALL = APPRO_LABELS + ["bio_dont_commerce_equitable"] + APPRO_LABELS_FRANCE
    APPRO_LABELS_GROUPS_MAPPING = {
        "bio": ["bio"],
        "siqo": ["label_rouge", "aocaop_igp_stg"],
        "externalites_performance": ["externalites", "performance"],
        "egalim_autres": ["hve", "peche_durable", "rup", "commerce_equitable", "fermier"],
    }
    APPRO_LABELS_GROUPS_GROUPS_MAPPING = {
        "egalim_hors_bio": ["siqo", "externalites_performance", "egalim_autres"],
        "egalim": ["bio", "siqo", "externalites_performance", "egalim_autres"],
    }

    SIMPLE_APPRO_FIELDS = [
        "valeur_totale",
        "valeur_bio",
        "valeur_bio_dont_commerce_equitable",
        "valeur_siqo",
        "valeur_externalites_performance",
        "valeur_egalim_autres",
        "valeur_egalim_autres_dont_commerce_equitable",
        "valeur_viandes_volailles",
        "valeur_viandes_volailles_egalim",
        "valeur_viandes_volailles_france",
        "valeur_produits_de_la_mer",
        "valeur_produits_de_la_mer_egalim",
        "valeur_produits_de_la_mer_france",
        "valeur_fruits_et_legumes_france",
        "valeur_charcuterie_france",
        "valeur_produits_laitiers_france",
        "valeur_boulangerie_france",
        "valeur_boissons_france",
        "valeur_autres_france",
    ]

    APPRO_FIELDS_REQUIRED_BEFORE_2025 = [
        "valeur_totale",
    ]
    SIMPLE_APPRO_FIELDS_REQUIRED_2025 = [
        "valeur_totale",
        "valeur_bio",
        "valeur_siqo",
        "valeur_egalim_autres",
        "valeur_viandes_volailles",
        "valeur_viandes_volailles_egalim",
    ]

    AGGREGATED_APPRO_FIELDS = [
        "valeur_bio_agg",
        "valeur_siqo_agg",
        "valeur_externalites_performance_agg",
        "valeur_egalim_autres_agg",
        # "valeur_egalim_hors_bio_agg",
        # "valeur_egalim_agg",
    ]

    APPRO_FIELDS = [
        "valeur_viandes_volailles_bio",
        "valeur_viandes_volailles_bio_dont_commerce_equitable",
        "valeur_produits_de_la_mer_bio",
        "valeur_produits_de_la_mer_bio_dont_commerce_equitable",
        "valeur_fruits_et_legumes_bio",
        "valeur_fruits_et_legumes_bio_dont_commerce_equitable",
        "valeur_charcuterie_bio",
        "valeur_charcuterie_bio_dont_commerce_equitable",
        "valeur_produits_laitiers_bio",
        "valeur_produits_laitiers_bio_dont_commerce_equitable",
        "valeur_boulangerie_bio",
        "valeur_boulangerie_bio_dont_commerce_equitable",
        "valeur_boissons_bio",
        "valeur_boissons_bio_dont_commerce_equitable",
        "valeur_autres_bio",
        "valeur_autres_bio_dont_commerce_equitable",
        "valeur_viandes_volailles_label_rouge",
        "valeur_produits_de_la_mer_label_rouge",
        "valeur_fruits_et_legumes_label_rouge",
        "valeur_charcuterie_label_rouge",
        "valeur_produits_laitiers_label_rouge",
        "valeur_boulangerie_label_rouge",
        "valeur_boissons_label_rouge",
        "valeur_autres_label_rouge",
        "valeur_viandes_volailles_aocaop_igp_stg",
        "valeur_produits_de_la_mer_aocaop_igp_stg",
        "valeur_fruits_et_legumes_aocaop_igp_stg",
        "valeur_charcuterie_aocaop_igp_stg",
        "valeur_produits_laitiers_aocaop_igp_stg",
        "valeur_boulangerie_aocaop_igp_stg",
        "valeur_boissons_aocaop_igp_stg",
        "valeur_autres_aocaop_igp_stg",
        "valeur_viandes_volailles_hve",
        "valeur_produits_de_la_mer_hve",
        "valeur_fruits_et_legumes_hve",
        "valeur_charcuterie_hve",
        "valeur_produits_laitiers_hve",
        "valeur_boulangerie_hve",
        "valeur_boissons_hve",
        "valeur_autres_hve",
        "valeur_viandes_volailles_peche_durable",
        "valeur_produits_de_la_mer_peche_durable",
        "valeur_fruits_et_legumes_peche_durable",
        "valeur_charcuterie_peche_durable",
        "valeur_produits_laitiers_peche_durable",
        "valeur_boulangerie_peche_durable",
        "valeur_boissons_peche_durable",
        "valeur_autres_peche_durable",
        "valeur_viandes_volailles_rup",
        "valeur_produits_de_la_mer_rup",
        "valeur_fruits_et_legumes_rup",
        "valeur_charcuterie_rup",
        "valeur_produits_laitiers_rup",
        "valeur_boulangerie_rup",
        "valeur_boissons_rup",
        "valeur_autres_rup",
        "valeur_viandes_volailles_commerce_equitable",
        "valeur_produits_de_la_mer_commerce_equitable",
        "valeur_fruits_et_legumes_commerce_equitable",
        "valeur_charcuterie_commerce_equitable",
        "valeur_produits_laitiers_commerce_equitable",
        "valeur_boulangerie_commerce_equitable",
        "valeur_boissons_commerce_equitable",
        "valeur_autres_commerce_equitable",
        "valeur_viandes_volailles_fermier",
        "valeur_produits_de_la_mer_fermier",
        "valeur_fruits_et_legumes_fermier",
        "valeur_charcuterie_fermier",
        "valeur_produits_laitiers_fermier",
        "valeur_boulangerie_fermier",
        "valeur_boissons_fermier",
        "valeur_autres_fermier",
        "valeur_viandes_volailles_externalites",
        "valeur_produits_de_la_mer_externalites",
        "valeur_fruits_et_legumes_externalites",
        "valeur_charcuterie_externalites",
        "valeur_produits_laitiers_externalites",
        "valeur_boulangerie_externalites",
        "valeur_boissons_externalites",
        "valeur_autres_externalites",
        "valeur_viandes_volailles_performance",
        "valeur_produits_de_la_mer_performance",
        "valeur_fruits_et_legumes_performance",
        "valeur_charcuterie_performance",
        "valeur_produits_laitiers_performance",
        "valeur_boulangerie_performance",
        "valeur_boissons_performance",
        "valeur_autres_performance",
        "valeur_viandes_volailles_non_egalim",
        "valeur_produits_de_la_mer_non_egalim",
        "valeur_fruits_et_legumes_non_egalim",
        "valeur_charcuterie_non_egalim",
        "valeur_produits_laitiers_non_egalim",
        "valeur_boulangerie_non_egalim",
        "valeur_boissons_non_egalim",
        "valeur_autres_non_egalim",
        "valeur_viandes_volailles_france",
        "valeur_produits_de_la_mer_france",
        "valeur_fruits_et_legumes_france",
        "valeur_charcuterie_france",
        "valeur_produits_laitiers_france",
        "valeur_boulangerie_france",
        "valeur_boissons_france",
        "valeur_autres_france",
        "valeur_viandes_volailles_circuit_court",
        "valeur_produits_de_la_mer_circuit_court",
        "valeur_fruits_et_legumes_circuit_court",
        "valeur_charcuterie_circuit_court",
        "valeur_produits_laitiers_circuit_court",
        "valeur_boulangerie_circuit_court",
        "valeur_boissons_circuit_court",
        "valeur_autres_circuit_court",
        "valeur_viandes_volailles_local",
        "valeur_produits_de_la_mer_local",
        "valeur_fruits_et_legumes_local",
        "valeur_charcuterie_local",
        "valeur_produits_laitiers_local",
        "valeur_boulangerie_local",
        "valeur_boissons_local",
        "valeur_autres_local",
    ]
    # TODO: clean up when updating the imports
    APPRO_FIELDS_FOR_IMPORT = [
        field_name for field_name in APPRO_FIELDS if "bio_dont_commerce_equitable" not in field_name
    ]

    COMPLETE_APPRO_FIELDS = ["valeur_totale", "valeur_viandes_volailles", "valeur_produits_de_la_mer"] + APPRO_FIELDS

    COMPLETE_APPRO_FIELDS_REQUIRED_2025 = [
        "valeur_totale",
        "valeur_viandes_volailles",
        "valeur_produits_de_la_mer",
        "valeur_viandes_volailles_bio",
        "valeur_produits_de_la_mer_bio",
        "valeur_fruits_et_legumes_bio",
        "valeur_charcuterie_bio",
        "valeur_produits_laitiers_bio",
        "valeur_boulangerie_bio",
        "valeur_boissons_bio",
        "valeur_autres_bio",
        "valeur_viandes_volailles_label_rouge",
        "valeur_produits_de_la_mer_label_rouge",
        "valeur_fruits_et_legumes_label_rouge",
        "valeur_charcuterie_label_rouge",
        "valeur_produits_laitiers_label_rouge",
        "valeur_boulangerie_label_rouge",
        # "valeur_boissons_label_rouge",
        "valeur_autres_label_rouge",
        "valeur_viandes_volailles_aocaop_igp_stg",
        "valeur_produits_de_la_mer_aocaop_igp_stg",
        "valeur_fruits_et_legumes_aocaop_igp_stg",
        "valeur_charcuterie_aocaop_igp_stg",
        "valeur_produits_laitiers_aocaop_igp_stg",
        "valeur_boulangerie_aocaop_igp_stg",
        "valeur_boissons_aocaop_igp_stg",
        "valeur_autres_aocaop_igp_stg",
        "valeur_viandes_volailles_hve",
        "valeur_produits_de_la_mer_hve",
        "valeur_fruits_et_legumes_hve",
        "valeur_charcuterie_hve",
        "valeur_produits_laitiers_hve",
        "valeur_boulangerie_hve",
        "valeur_boissons_hve",
        "valeur_autres_hve",
        "valeur_viandes_volailles_rup",
        "valeur_produits_de_la_mer_rup",
        "valeur_fruits_et_legumes_rup",
        "valeur_charcuterie_rup",
        "valeur_produits_laitiers_rup",
        "valeur_boulangerie_rup",
        "valeur_boissons_rup",
        "valeur_autres_rup",
        "valeur_viandes_volailles_commerce_equitable",
        "valeur_produits_de_la_mer_commerce_equitable",
        "valeur_fruits_et_legumes_commerce_equitable",
        "valeur_charcuterie_commerce_equitable",
        "valeur_produits_laitiers_commerce_equitable",
        "valeur_boulangerie_commerce_equitable",
        "valeur_boissons_commerce_equitable",
        "valeur_autres_commerce_equitable",
        "valeur_viandes_volailles_fermier",
        # "valeur_produits_de_la_mer_fermier",
        # "valeur_fruits_et_legumes_fermier",
        "valeur_charcuterie_fermier",
        "valeur_produits_laitiers_fermier",
        # "valeur_boulangerie_fermier",
        # "valeur_boissons_fermier",
        # "valeur_autres_fermier",
    ]

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

    canteen = models.ForeignKey(
        Canteen, on_delete=models.SET_NULL, null=True, related_name="diagnostics", verbose_name="cantine"
    )

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
    valeur_totale = make_optional_positive_decimal_field(
        verbose_name="Valeur totale annuelle HT",
    )
    valeur_bio = make_optional_positive_decimal_field(
        verbose_name="Bio - Valeur annuelle HT",
    )
    valeur_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Bio dont commerce équitable - Valeur annuelle HT",
    )
    valeur_fair_trade = make_optional_positive_decimal_field(  # legacy
        verbose_name="Commerce équitable - Valeur annuelle HT",
    )
    valeur_siqo = make_optional_positive_decimal_field(
        verbose_name="Produits SIQO (hors bio) - Valeur annuelle HT",
    )
    valeur_pat = make_optional_positive_decimal_field(  # legacy
        verbose_name="Produits dans le cadre de Projects Alimentaires Territoriaux - Valeur annuelle HT",
    )
    valeur_externalites_performance = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) prenant en compte les coûts imputés aux externalités environnementales ou leurs performances en matière environnementale",
    )
    valeur_egalim_autres = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) des autres achats EGalim",
    )
    valeur_egalim_autres_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) des achats commerce équitable (hors bio)",
    )
    valeur_viandes_volailles = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées",
    )
    valeur_viandes_volailles_egalim = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim",
    )
    valeur_viandes_volailles_france = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées origine France",
    )
    valeur_produits_de_la_mer = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) poissons et produits aquatiques",
    )
    valeur_produits_de_la_mer_egalim = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) poissons et produits aquatiques EGalim",
    )

    valeur_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Valeur label rouge",
    )
    valeur_label_aoc_igp = make_optional_positive_decimal_field(
        verbose_name="Valeur label AOC/AOP/IGP",
    )
    valeur_label_hve = make_optional_positive_decimal_field(
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
    valeur_bio_agg = make_optional_positive_decimal_field(
        verbose_name="Bio - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_siqo_agg = make_optional_positive_decimal_field(
        verbose_name="Produits SIQO (hors bio) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_externalites_performance_agg = make_optional_positive_decimal_field(
        verbose_name="Externalité/performance - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)",
    )
    valeur_egalim_autres_agg = make_optional_positive_decimal_field(
        verbose_name="Autres achats EGalim - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_egalim_hors_bio_agg = make_optional_positive_decimal_field(
        verbose_name="EGalim (Produits SIQO (hors bio) + Externalité/performance + Autres achats EGalim) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_egalim_agg = make_optional_positive_decimal_field(
        verbose_name="EGalim (Bio + Produits SIQO (hors bio) + Externalité/performance + Autres achats EGalim) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )

    # detailed values
    valeur_viandes_volailles_bio = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Bio",
    )
    valeur_viandes_volailles_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Bio dont commerce équitable",
    )
    valeur_produits_de_la_mer_bio = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Bio",
    )
    valeur_produits_de_la_mer_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Bio dont commerce équitable",
    )
    valeur_fruits_et_legumes_bio = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Bio",
    )
    valeur_fruits_et_legumes_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Bio dont commerce équitable",
    )
    valeur_charcuterie_bio = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Bio",
    )
    valeur_charcuterie_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Bio dont commerce équitable",
    )
    valeur_produits_laitiers_bio = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Bio",
    )
    valeur_produits_laitiers_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Bio dont commerce équitable",
    )
    valeur_boulangerie_bio = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Bio",
    )
    valeur_boulangerie_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Bio dont commerce équitable",
    )
    valeur_boissons_bio = make_optional_positive_decimal_field(
        verbose_name="Boissons, Bio",
    )
    valeur_boissons_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Bio dont commerce équitable",
    )
    valeur_autres_bio = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Bio",
    )
    valeur_autres_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Bio dont commerce équitable",
    )
    valeur_viandes_volailles_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Label rouge",
    )
    valeur_produits_de_la_mer_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Label rouge",
    )
    valeur_fruits_et_legumes_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Label rouge",
    )
    valeur_charcuterie_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Label rouge",
    )
    valeur_produits_laitiers_label_rouge = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Label rouge",
    )
    valeur_boulangerie_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Label rouge",
    )
    valeur_boissons_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Boissons, Label rouge",
    )
    valeur_autres_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Label rouge",
    )
    valeur_viandes_volailles_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, AOC / AOP / IGP / STG",
    )
    valeur_produits_de_la_mer_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, AOC / AOP / IGP / STG",
    )
    valeur_fruits_et_legumes_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, AOC / AOP / IGP / STG",
    )
    valeur_charcuterie_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, AOC / AOP / IGP / STG",
    )
    valeur_produits_laitiers_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), AOC / AOP / IGP / STG",
    )
    valeur_boulangerie_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, AOC / AOP / IGP / STG",
    )
    valeur_boissons_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Boissons, AOC / AOP / IGP / STG",
    )
    valeur_autres_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, AOC / AOP / IGP / STG",
    )
    valeur_viandes_volailles_hve = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Haute valeur environnementale",
    )
    valeur_produits_de_la_mer_hve = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Haute valeur environnementale",
    )
    valeur_fruits_et_legumes_hve = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Haute valeur environnementale",
    )
    valeur_charcuterie_hve = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Haute valeur environnementale",
    )
    valeur_produits_laitiers_hve = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Haute valeur environnementale",
    )
    valeur_boulangerie_hve = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Haute valeur environnementale",
    )
    valeur_boissons_hve = make_optional_positive_decimal_field(
        verbose_name="Boissons, Haute valeur environnementale",
    )
    valeur_autres_hve = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Haute valeur environnementale",
    )
    valeur_viandes_volailles_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Pêche durable",
    )
    valeur_produits_de_la_mer_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Pêche durable",
    )
    valeur_fruits_et_legumes_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Pêche durable",
    )
    valeur_charcuterie_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Pêche durable",
    )
    valeur_produits_laitiers_peche_durable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Pêche durable",
    )
    valeur_boulangerie_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Pêche durable",
    )
    valeur_boissons_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Pêche durable",
    )
    valeur_autres_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Pêche durable",
    )
    valeur_viandes_volailles_rup = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Région ultrapériphérique",
    )
    valeur_produits_de_la_mer_rup = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Région ultrapériphérique",
    )
    valeur_fruits_et_legumes_rup = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Région ultrapériphérique",
    )
    valeur_charcuterie_rup = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Région ultrapériphérique",
    )
    valeur_produits_laitiers_rup = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Région ultrapériphérique",
    )
    valeur_boulangerie_rup = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Région ultrapériphérique",
    )
    valeur_boissons_rup = make_optional_positive_decimal_field(
        verbose_name="Boissons, Région ultrapériphérique",
    )
    valeur_autres_rup = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Région ultrapériphérique",
    )
    valeur_viandes_volailles_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Commerce équitable",
    )
    valeur_produits_de_la_mer_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Commerce équitable",
    )
    valeur_fruits_et_legumes_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Commerce équitable",
    )
    valeur_charcuterie_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Commerce équitable",
    )
    valeur_produits_laitiers_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Commerce équitable",
    )
    valeur_boulangerie_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Commerce équitable",
    )
    valeur_boissons_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Commerce équitable",
    )
    valeur_autres_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Commerce équitable",
    )
    valeur_viandes_volailles_fermier = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Fermier",
    )
    valeur_produits_de_la_mer_fermier = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Fermier",
    )
    valeur_fruits_et_legumes_fermier = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Fermier",
    )
    valeur_charcuterie_fermier = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Fermier",
    )
    valeur_produits_laitiers_fermier = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Fermier",
    )
    valeur_boulangerie_fermier = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Fermier",
    )
    valeur_boissons_fermier = make_optional_positive_decimal_field(
        verbose_name="Boissons, Fermier",
    )
    valeur_autres_fermier = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Fermier",
    )
    valeur_viandes_volailles_externalites = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_produits_de_la_mer_externalites = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_fruits_et_legumes_externalites = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_charcuterie_externalites = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_produits_laitiers_externalites = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_boulangerie_externalites = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_boissons_externalites = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_autres_externalites = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_viandes_volailles_performance = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_produits_de_la_mer_performance = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_fruits_et_legumes_performance = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_charcuterie_performance = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_produits_laitiers_performance = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_boulangerie_performance = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_boissons_performance = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_autres_performance = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_viandes_volailles_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, non-EGalim.",
    )
    valeur_produits_de_la_mer_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, non-EGalim.",
    )
    valeur_fruits_et_legumes_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, non-EGalim.",
    )
    valeur_charcuterie_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, non-EGalim.",
    )
    valeur_produits_laitiers_non_egalim = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), non-EGalim.",
    )
    valeur_boulangerie_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, non-EGalim.",
    )
    valeur_boissons_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Boissons, non-EGalim.",
    )
    valeur_autres_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, non-EGalim.",
    )
    valeur_viandes_volailles_france = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Provenance France",
    )
    valeur_produits_de_la_mer_france = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Provenance France",
    )
    valeur_fruits_et_legumes_france = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Provenance France",
    )
    valeur_charcuterie_france = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Provenance France",
    )
    valeur_produits_laitiers_france = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Provenance France",
    )
    valeur_boulangerie_france = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Provenance France",
    )
    valeur_boissons_france = make_optional_positive_decimal_field(
        verbose_name="Boissons, Provenance France",
    )
    valeur_autres_france = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Provenance France",
    )
    valeur_viandes_volailles_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Circuit-court",
    )
    valeur_produits_de_la_mer_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Circuit-court",
    )
    valeur_fruits_et_legumes_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Circuit-court",
    )
    valeur_charcuterie_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Circuit-court",
    )
    valeur_produits_laitiers_circuit_court = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Circuit-court",
    )
    valeur_boulangerie_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Circuit-court",
    )
    valeur_boissons_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Boissons, Circuit-court",
    )
    valeur_autres_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d’épicerie, Circuit-court",
    )
    valeur_viandes_volailles_local = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produit local",
    )
    valeur_produits_de_la_mer_local = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Produit local",
    )
    valeur_fruits_et_legumes_local = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produit local",
    )
    valeur_charcuterie_local = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produit local",
    )
    valeur_produits_laitiers_local = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produit local",
    )
    valeur_boulangerie_local = make_optional_positive_decimal_field(
        verbose_name="Boulangerie/Pâtisserie fraîches et surgelées, Produit local",
    )
    valeur_boissons_local = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produit local",
    )
    valeur_autres_local = make_optional_positive_decimal_field(
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
            diagnostic_validators.validate_diagnostic_type(self),
            diagnostic_validators.validate_appro_fields_required(self),
            diagnostic_validators.validate_valeur_totale(self),
            diagnostic_validators.validate_valeur_bio(self),
            diagnostic_validators.validate_valeur_egalim_autres(self),
            diagnostic_validators.validate_viandes_volailles_total(self),
            diagnostic_validators.validate_produits_de_la_mer_total(self),
            diagnostic_validators.validate_viandes_volailles_produits_de_la_mer_egalim(self),
        )
        if validation_errors:
            raise ValidationError(validation_errors)

        return super().clean()

    def populate_simplified_diagnostic_values(self):
        self.valeur_bio = self.label_group_sum("bio")
        self.valeur_bio_dont_commerce_equitable = self.label_sum("bio_dont_commerce_equitable")
        self.valeur_siqo = self.label_group_sum("siqo")
        self.valeur_externalites_performance = self.label_group_sum("externalites_performance")
        self.valeur_egalim_autres = self.label_group_sum("egalim_autres")
        self.valeur_egalim_autres_dont_commerce_equitable = self.label_sum("commerce_equitable")

        total_meat_egalim = total_fish_egalim = 0
        for label in Diagnostic.APPRO_LABELS_EGALIM:
            family = "viandes_volailles"
            # need to do or 0 and not give a default value because the value can be explicitly set to None
            total_meat_egalim = total_meat_egalim + (getattr(self, f"valeur_{family}_{label}") or 0)

            family = "produits_de_la_mer"
            total_fish_egalim = total_fish_egalim + (getattr(self, f"valeur_{family}_{label}") or 0)

        # NOTE: stop populating france from APPRO_LABELS_FRANCE
        # for label in Diagnostic.APPRO_LABELS_FRANCE:
        #     family = "viandes_volailles"
        #     total_meat_france = total_meat_france + (getattr(self, f"valeur_{family}_{label}") or 0)

        self.valeur_viandes_volailles_egalim = total_meat_egalim
        # self.valeur_viandes_volailles_france = total_meat_france
        self.valeur_produits_de_la_mer_egalim = total_fish_egalim

    def populate_aggregated_values(self):
        self.valeur_bio_agg = self.label_group_sum("bio")
        self.valeur_siqo_agg = self.label_group_sum("siqo")
        self.valeur_externalites_performance_agg = self.label_group_sum("externalites_performance")
        self.valeur_egalim_autres_agg = self.label_group_sum("egalim_autres")
        # group_group
        self.valeur_egalim_hors_bio_agg = self.label_group_group_sum("egalim_hors_bio")
        self.valeur_egalim_agg = self.label_group_group_sum("egalim")

    def label_sum(self, label: str):
        sum = 0
        is_null = True
        for family in Diagnostic.APPRO_FAMILIES:
            value = getattr(self, f"valeur_{family}_{label}")
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
        return getattr(self, f"valeur_{label_group}")

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
            value = getattr(self, f"valeur_{family}_{label}")
            if value:
                sum = sum + value
        return sum

    def egalim_sum(self):
        # return self.label_group_group_sum("egalim")
        return sum_int_with_potential_null(
            [getattr(self, f"valeur_{group}") for group in Diagnostic.APPRO_LABELS_GROUPS_GROUPS_MAPPING["egalim"]]
        )

    @property
    def valeur_totale_is_filled(self):
        return self.valeur_totale and self.valeur_totale > 0

    @property
    def is_diagnostic_type_simple(self):
        return self.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE

    @property
    def is_diagnostic_type_complete(self):
        return self.diagnostic_type == Diagnostic.DiagnosticType.COMPLETE

    @property
    def is_filled_simple(self):
        check = self.is_diagnostic_type_simple and self.valeur_totale_is_filled
        if int(self.year) >= 2025:
            return check and all(
                getattr(self, field) is not None for field in Diagnostic.SIMPLE_APPRO_FIELDS_REQUIRED_2025
            )
        return check

    @property
    def is_filled_complete(self):
        check = self.is_diagnostic_type_complete and self.valeur_totale_is_filled
        if int(self.year) >= 2025:
            return check and all(
                getattr(self, field) is not None for field in Diagnostic.COMPLETE_APPRO_FIELDS_REQUIRED_2025
            )
        return check

    @property
    def is_filled(self):
        return self.is_filled_simple or self.is_filled_complete

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
    def canteen_snapshot_sector_list_display(self):
        from data.models.sector import get_sector_label_list_from_sector_list

        if self.canteen_snapshot:
            if "sector_list" in self.canteen_snapshot:
                if len(self.canteen_snapshot["sector_list"]) > 0:
                    return ",".join(get_sector_label_list_from_sector_list(self.canteen_snapshot["sector_list"]))
            elif "sectors" in self.canteen_snapshot:
                if len(self.canteen_snapshot["sectors"]) > 0:
                    return ",".join([x["name"] for x in (self.canteen_snapshot.get("sectors") or [])])
        return None

    @property
    def latest_submitted_teledeclaration(self):
        submitted_teledeclarations = self.teledeclaration_set.submitted()
        if submitted_teledeclarations.count() == 0:
            return None
        return submitted_teledeclarations.order_by("-creation_date").first()

    @property
    def appro_badge(self) -> bool | None:
        total = self.valeur_totale
        if total:
            bio_percent = (self.valeur_bio or 0) / total
            egalim_percent = self.egalim_sum() / total

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
        # Only the canteens with more than 200 daily meals with a diversification plan
        if self.canteen.daily_meal_count and self.canteen.daily_meal_count >= 200 and self.has_diversification_plan:
            return True
        # Only the canteens in the administration sector must have a daily frequency
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
        if self.canteen.is_satellite:
            if self.canteen.groupe_id:
                try:
                    groupe = self.canteen.groupe
                    existing_diagnostic = groupe.diagnostics.get(year=self.year)
                    handles_satellite_data = existing_diagnostic.central_kitchen_diagnostic_mode in [
                        Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                        Diagnostic.CentralKitchenDiagnosticMode.ALL,
                    ]
                    return groupe.is_groupe and handles_satellite_data
                except (Canteen.DoesNotExist, Canteen.MultipleObjectsReturned, Diagnostic.DoesNotExist):
                    pass
        return False

    def _get_teledeclaration_mode(self):
        uses_central_kitchen_appro = self._should_use_central_kitchen_appro()
        if uses_central_kitchen_appro:
            return Diagnostic.TeledeclarationMode.SATELLITE_WITHOUT_APPRO
        if self.canteen.is_groupe_or_central_cuisine:
            if self.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.ALL:
                return Diagnostic.TeledeclarationMode.CENTRAL_ALL
            if self.central_kitchen_diagnostic_mode == Diagnostic.CentralKitchenDiagnosticMode.APPRO:
                return Diagnostic.TeledeclarationMode.CENTRAL_APPRO
        return Diagnostic.TeledeclarationMode.SITE

    def teledeclare(self, applicant, skip_validations=False):
        """
        Teledeclare the diagnostic
        - applicant is mandatory (User instance)
        - skip_validations: if True, skip validation checks (USE WITH CAUTION) (only for tests)
        """
        if not skip_validations:
            if not is_in_teledeclaration_or_correction():
                raise ValidationError("Ce n'est pas possible de télédéclarer hors de la période de la campagne")
            if not is_in_teledeclaration_or_correction(self.year):
                raise ValidationError("Ce diagnostic n'est pas dans la bonne année de télédéclaration")
            if self.is_teledeclared:
                raise ValidationError("Ce diagnostic a déjà été télédéclaré")
            uses_central_kitchen_appro = self._should_use_central_kitchen_appro()
            if not self.is_filled and not uses_central_kitchen_appro:
                raise ValidationError("Ce diagnostic n'est pas rempli")
            if not self.canteen.is_filled:
                raise ValidationError("La cantine associée à ce diagnostic n'est pas remplie")
            if self.canteen.is_groupe:
                if self.canteen.satellites_count == 0:
                    raise ValidationError("Le groupe associe à ce diagnostic n'a pas de cantine satellite")
                if self.canteen.satellites_missing_data_count > 0:
                    raise ValidationError(
                        f"{self.canteen.satellites_missing_data_count} satellites du groupe associée à ce diagnostic ne sont pas remplis"
                    )

        from api.serializers import CanteenTeledeclarationSerializer, SatelliteTeledeclarationSerializer

        # canteen data
        serialized_canteen = CanteenTeledeclarationSerializer(self.canteen).data
        self.canteen_snapshot = serialized_canteen

        # satellites data
        if self.canteen.is_groupe_or_central_cuisine:
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
        self.teledeclaration_id = self.id

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
        self.teledeclaration_id = None

        self.save()
