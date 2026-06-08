from datetime import date
from decimal import Decimal

from django.core.validators import MinValueValidator, ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import ExtractYear
from django.contrib.auth import get_user_model

from macantine.etl import utils
from common.utils import utils as utils_utils
from data.fields import ChoiceArrayField
from data.models import Canteen
from data.models.creation_source import CreationSource
from data.validators import purchase as purchase_validators

from .softdeletionmodel import SoftDeletionManager, SoftDeletionModel, SoftDeletionQuerySet


def bio_query():
    return Q(caracteristiques__overlap=Purchase.CHARACTERISTIC_LABELS_BIO)


def siqo_query():
    return Q(caracteristiques__overlap=Purchase.CHARACTERISTIC_LABELS_SIQO)


def egalim_autres_query():
    return Q(caracteristiques__overlap=Purchase.CHARACTERISTIC_LABELS_EGALIM_AUTRES)


def valeur_externalites_performance_query():
    return Q(caracteristiques__overlap=Purchase.CHARACTERISTIC_LABELS_EXTERNALITES_PERFORMANCE)


class PurchaseQuerySet(SoftDeletionQuerySet):
    def for_user(self, user):
        return self.select_related("canteen").filter(canteen__managers=user)

    def for_year(self, year):
        return self.filter(date__year=year)

    def filter_for_stats(self, canteen, year):
        return (
            self.only("id", "famille_produits", "caracteristiques", "prix_ht").filter(canteen=canteen).for_year(year)
        )

    def aggregated_stats(self):
        return self.aggregate(
            valeur_totale=Sum("prix_ht"),
            valeur_bio=Sum("prix_ht", filter=bio_query()),
            valeur_bio_dont_commerce_equitable=Sum(
                "prix_ht",
                filter=bio_query() & Q(caracteristiques__contains=[Purchase.Characteristic.COMMERCE_EQUITABLE]),
            ),
            # valeur_siqo should ignore any bio products
            valeur_siqo=Sum("prix_ht", filter=~bio_query() & siqo_query()),
            # valeur_egalim_autres & valeur_egalim_autres_dont_commerce_equitable should ignore any bio & siqo products
            valeur_egalim_autres=Sum(
                "prix_ht",
                filter=~bio_query() & ~siqo_query() & egalim_autres_query(),
            ),
            valeur_egalim_autres_dont_commerce_equitable=Sum(
                "prix_ht",
                filter=~bio_query()
                & ~siqo_query()
                & egalim_autres_query()
                & Q(caracteristiques__contains=[Purchase.Characteristic.COMMERCE_EQUITABLE]),
            ),
            # valeur_externalites_performance should ignore any bio, siqo, and egalim_autres products
            valeur_externalites_performance=Sum(
                "prix_ht",
                filter=~bio_query() & ~siqo_query() & ~egalim_autres_query() & valeur_externalites_performance_query(),
            ),
            # misc totals
            valeur_viandes_volailles=Sum("prix_ht", filter=Q(famille_produits=Purchase.Family.VIANDES_VOLAILLES)),
            valeur_viandes_volailles_egalim=Sum(
                "prix_ht",
                filter=Q(famille_produits=Purchase.Family.VIANDES_VOLAILLES)
                & Q(caracteristiques__overlap=Purchase.CHARACTERISTIC_LABELS_EGALIM),
            ),
            valeur_viandes_volailles_france=Sum(
                "prix_ht",
                filter=Q(famille_produits=Purchase.Family.VIANDES_VOLAILLES)
                & Q(caracteristiques__contains=[Purchase.Characteristic.FRANCE]),
            ),
            valeur_produits_de_la_mer=Sum("prix_ht", filter=Q(famille_produits=Purchase.Family.PRODUITS_DE_LA_MER)),
            valeur_produits_de_la_mer_egalim=Sum(
                "prix_ht",
                filter=Q(famille_produits=Purchase.Family.PRODUITS_DE_LA_MER)
                & Q(caracteristiques__overlap=Purchase.CHARACTERISTIC_LABELS_EGALIM),
            ),
        )


class PurchaseManager(SoftDeletionManager):
    queryset_model = PurchaseQuerySet


class Purchase(SoftDeletionModel):
    class PurchaseCategory(models.TextChoices):  # not used anymore
        VIANDES_VOLAILLES = "VIANDES_VOLAILLES", "Viandes, volailles"
        PRODUITS_DE_LA_MER = "PRODUITS_DE_LA_MER", "Produits de la mer"
        FRUITS_ET_LEGUMES = "FRUITS_ET_LEGUMES", "Fruits, légumes, légumineuses et oléagineux"
        PRODUITS_CEREALIERS = "PRODUITS_CEREALIERS", "Produits céréaliers"
        ENTREES = "ENTREES", "Entrées et plats composés"
        PRODUITS_LAITIERS = "PRODUITS_LAITIERS", "Lait et produits laitiers"
        BOISSONS = "BOISSONS", "Boissons"
        AIDES = "AIDES", "Aides culinaires et ingrédients divers"
        BEURRE_OEUF_FROMAGE = "BEURRE_OEUF_FROMAGE", "Beurre, oeuf, fromage"
        PRODUITS_SUCRES = "PRODUITS_SUCRES", "Produits sucrés"
        ALIMENTS_INFANTILES = "ALIMENTS_INFANTILES", "Aliments infantiles"
        GLACES_SORBETS = "GLACES_SORBETS", "Glaces et sorbets"
        AUTRES = "AUTRES", "Autres"

    class Family(models.TextChoices):
        VIANDES_VOLAILLES = "VIANDES_VOLAILLES", "Viandes et volailles fraîches et surgelées"
        CHARCUTERIE = "CHARCUTERIE", "Charcuterie"
        PRODUITS_DE_LA_MER = "PRODUITS_DE_LA_MER", "Poissons, produits de la mer et de l'aquaculture"
        FRUITS_ET_LEGUMES = "FRUITS_ET_LEGUMES", "Fruits et légumes frais et surgelés"
        PRODUITS_LAITIERS = "PRODUITS_LAITIERS", "BOF (Produits laitiers, beurre et œufs)"
        BOULANGERIE = "BOULANGERIE", "Boulangerie/Pâtisserie fraîches et surgelées"
        BOISSONS = "BOISSONS", "Boissons"
        AUTRES = "AUTRES", "Autres produits frais, surgelés et d'épicerie"

    class Characteristic(models.TextChoices):
        BIO = "BIO", "Bio"
        CONVERSION_BIO = "CONVERSION_BIO", "En conversion bio"  # not used anymore
        LABEL_ROUGE = "LABEL_ROUGE", "Label rouge"
        AOCAOP = "AOCAOP", "AOC / AOP"
        IGP = "IGP", "Indication géographique protégée"
        STG = "STG", "Spécialité traditionnelle garantie"
        HVE = "HVE", "Haute valeur environnementale"
        PECHE_DURABLE = "PECHE_DURABLE", "Pêche durable"
        RUP = "RUP", "Région ultrapériphérique"
        FERMIER = "FERMIER", "Fermier"
        EXTERNALITES = (
            "EXTERNALITES",
            "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
        )
        COMMERCE_EQUITABLE = "COMMERCE_EQUITABLE", "Commerce équitable"
        PERFORMANCE = "PERFORMANCE", "Produits acquis sur la base de leurs performances en matière environnementale"
        EQUIVALENTS = "EQUIVALENTS", "Produits équivalents"  # not used anymore
        EUROPE = "EUROPE", "Origine Europe"
        FRANCE = "FRANCE", "Origine France"
        CIRCUIT_COURT = "CIRCUIT_COURT", "Circuit-court"
        LOCAL = "LOCAL", "Produit local"

    class Local(models.TextChoices):
        REGION = "REGION", "Région"
        DEPARTEMENT = "DEPARTEMENT", "Département"
        AUTOUR_SERVICE = "AUTOUR_SERVICE", "200 km autour du lieu de service"
        PAT = "PAT", "Issu du Projet Alimentaire Territorial (PAT)"
        AUTRE = "AUTRE", "Autre"

    CHARACTERISTIC_LABELS_BIO = [
        Characteristic.BIO,
        Characteristic.CONVERSION_BIO,  # not used anymore
    ]

    CHARACTERISTIC_LABELS_AOCAOP_IGP_STG = [
        Characteristic.AOCAOP,
        Characteristic.IGP,
        Characteristic.STG,
    ]

    CHARACTERISTIC_LABELS_SIQO = [Characteristic.LABEL_ROUGE] + CHARACTERISTIC_LABELS_AOCAOP_IGP_STG

    CHARACTERISTIC_LABELS_EXTERNALITES_PERFORMANCE = [
        Characteristic.EXTERNALITES,
        Characteristic.PERFORMANCE,
        Characteristic.EQUIVALENTS,  # not used anymore
    ]

    CHARACTERISTIC_LABELS_EGALIM_AUTRES = [
        Characteristic.HVE,
        Characteristic.PECHE_DURABLE,
        Characteristic.RUP,
        Characteristic.FERMIER,
        Characteristic.COMMERCE_EQUITABLE,
    ]

    CHARACTERISTIC_LABELS_FRANCE_CIRCUIT_COURT_LOCAL = [
        Characteristic.FRANCE,
        Characteristic.CIRCUIT_COURT,
        Characteristic.LOCAL,
    ]

    CHARACTERISTIC_LABELS_EGALIM = (
        CHARACTERISTIC_LABELS_BIO
        + CHARACTERISTIC_LABELS_SIQO
        + CHARACTERISTIC_LABELS_EXTERNALITES_PERFORMANCE
        + CHARACTERISTIC_LABELS_EGALIM_AUTRES
    )

    CREATION_META_FIELDS = [
        "creation_date",
        "modification_date",
        "creation_user",
        "creation_source",
        "import_source",
    ]

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, related_name="purchases", verbose_name="cantine")
    date = models.DateField(default=date.today)
    description = models.TextField(null=True, blank=True, verbose_name="description du produit")
    fournisseur = models.TextField(null=True, blank=True, verbose_name="fournisseur")
    category = models.CharField(
        max_length=255, choices=PurchaseCategory.choices, null=True, blank=True, verbose_name="catégorie"
    )  # not used anymore
    famille_produits = models.CharField(
        max_length=255, choices=Family.choices, null=True, blank=True, verbose_name="famille de produits"
    )
    caracteristiques = ChoiceArrayField(
        base_field=models.CharField(
            max_length=255, choices=Characteristic.choices, null=True, blank=True, verbose_name="caractéristiques"
        ),
        blank=True,
        null=True,
        size=None,
        verbose_name="caractéristiques",
    )
    prix_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="prix HT",
        validators=[MinValueValidator(Decimal("0"))],
    )
    facture = models.FileField(null=True, blank=True, upload_to="invoices/%Y/")
    definition_local = models.CharField(
        max_length=255, choices=Local.choices, null=True, blank=True, verbose_name="définition de local"
    )

    import_source = models.TextField(null=True, blank=True, verbose_name="source de l'import de l'achat")

    creation_user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="purchases_created",
        verbose_name="utilisateur qui a créé l'achat",
    )
    creation_source = models.CharField(
        max_length=255,
        choices=CreationSource.choices,
        blank=True,
        null=True,
        verbose_name="Source de création de l'achat",
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    objects = PurchaseManager.from_queryset(PurchaseQuerySet)()
    all_objects = PurchaseManager.from_queryset(PurchaseQuerySet)(alive_only=False)

    class Meta:
        verbose_name = "achat"
        verbose_name_plural = "achats"
        ordering = ["-date", "-creation_date"]
        indexes = [models.Index(fields=["import_source"])]

    def clean(self, *args, **kwargs):
        validation_errors = utils_utils.merge_validation_errors(
            purchase_validators.validate_purchase_definition_local(self),
        )
        if validation_errors:
            raise ValidationError(validation_errors)

    def save(self, **kwargs):
        """
        - full_clean(): run validations (with extra validations in clean())
        """
        self.full_clean()
        super().save(**kwargs)

    @property
    def famille_produits_display(self):
        if not self.famille_produits:
            return None
        try:
            return Purchase.Family(self.famille_produits).label
        except Exception:
            return None

    @property
    def caracteristiques_display(self):
        if not self.caracteristiques:
            return None
        caracteristiques_display = []
        for c in self.caracteristiques:
            try:
                caracteristiques_display.append(Purchase.Characteristic(c).label)
            except Exception:
                pass
        return ", ".join(caracteristiques_display) if caracteristiques_display else None

    @classmethod
    def canteen_summary_for_year(cls, canteen, year):
        purchases = cls.objects.filter_for_stats(canteen, year)
        data = {"year": year}
        cls._simple_diag_data(purchases, data)
        cls._complete_diag_data(purchases, data, year)
        cls._misc_totals(purchases, data)

        return data

    @classmethod
    def canteen_percentage_summary_for_year(cls, canteen, year):
        data = cls.canteen_summary_for_year(canteen, year)
        data["percentage_valeur_totale"] = 1
        data["percentage_valeur_bio"] = utils.compute_percentage(
            data.get("valeur_bio"), data.get("valeur_totale"), ratio=True
        )
        data["percentage_valeur_siqo"] = utils.compute_percentage(
            data.get("valeur_siqo"), data.get("valeur_totale"), ratio=True
        )
        data["percentage_valeur_externalites_performance"] = utils.compute_percentage(
            data.get("valeur_externalites_performance"), data.get("valeur_totale"), ratio=True
        )
        data["percentage_valeur_egalim_autres"] = utils.compute_percentage(
            data.get("valeur_egalim_autres"), data.get("valeur_totale"), ratio=True
        )
        data["percentage_valeur_viandes_volailles_egalim"] = utils.compute_percentage(
            data.get("valeur_viandes_volailles_egalim"), data.get("valeur_viandes_volailles"), ratio=True
        )
        data["percentage_valeur_viandes_volailles_france"] = utils.compute_percentage(
            data.get("valeur_viandes_volailles_france"), data.get("valeur_viandes_volailles"), ratio=True
        )
        data["percentage_valeur_produits_de_la_mer_egalim"] = utils.compute_percentage(
            data.get("valeur_produits_de_la_mer_egalim"), data.get("valeur_produits_de_la_mer"), ratio=True
        )
        data["percentage_valeur_produits_de_la_mer_france"] = utils.compute_percentage(
            data.get("valeur_produits_de_la_mer_france"), data.get("valeur_produits_de_la_mer"), ratio=True
        )
        return data

    @classmethod
    def canteen_summary(cls, canteen):
        data = {"results": []}
        years = (
            cls.objects.filter(canteen=canteen).annotate(year=ExtractYear("date")).order_by("year").distinct("year")
        )
        years = [y["year"] for y in years.values()]
        for year in years:
            year_data = {"year": year}
            purchases = cls.objects.filter_for_stats(canteen, year)
            cls._simple_diag_data(purchases, year_data)
            data["results"].append(year_data)

        return data

    @classmethod
    def _simple_diag_data(cls, purchases, data):
        stats = purchases.aggregated_stats()
        data["valeur_totale"] = stats["valeur_totale"] or 0
        data["valeur_bio"] = stats["valeur_bio"] or 0
        data["valeur_bio_dont_commerce_equitable"] = stats["valeur_bio_dont_commerce_equitable"] or 0
        data["valeur_siqo"] = stats["valeur_siqo"] or 0
        data["valeur_egalim_autres"] = stats["valeur_egalim_autres"] or 0
        data["valeur_egalim_autres_dont_commerce_equitable"] = (
            stats["valeur_egalim_autres_dont_commerce_equitable"] or 0
        )
        data["valeur_externalites_performance"] = stats["valeur_externalites_performance"] or 0

    @classmethod
    def _complete_diag_data(cls, purchases, data, year):
        """
        Summary for detailed teledeclaration totals, by family and label.
        """
        cls._complete_diag_data_appro_labels(purchases, data)
        cls._complete_diag_data_appro_label_bio_dont_commerce_equitable(purchases, data)
        if int(year) == 2025:
            cls._complete_diag_appro_labels_france_circuit_court_local_2025(purchases, data)
        else:
            cls._complete_diag_appro_labels_france_circuit_court_local(purchases, data)
        cls._complete_diag_appro_labels_non_egalim(purchases, data)

    @classmethod
    def _complete_diag_data_appro_labels(cls, purchases, data):
        """
        How we manage APPRO_LABELS_EGALIM:
        - order of APPRO_LABELS_EGALIM is significant
        - determines which labels trump others when aggregating purchases
        - (purchases are not double-counted across labels)
        """
        from data.models import Diagnostic

        for family in Diagnostic.APPRO_FAMILIES:
            purchase_family = purchases.filter(famille_produits=family.upper())
            for label in Diagnostic.APPRO_LABELS_EGALIM:
                if label.upper() == "AOCAOP_IGP_STG":
                    purchase_family_label = purchase_family.filter(
                        caracteristiques__overlap=cls.CHARACTERISTIC_LABELS_AOCAOP_IGP_STG
                    ).distinct()
                    # the remaining stats should ignore already counted labels
                    purchase_family = purchase_family.exclude(
                        caracteristiques__overlap=cls.CHARACTERISTIC_LABELS_AOCAOP_IGP_STG
                    ).distinct()
                else:
                    purchase_family_label = purchase_family.filter(
                        Q(caracteristiques__contains=[cls.Characteristic[label.upper()]])
                    ).distinct()
                    # the remaining stats should ignore already counted labels
                    purchase_family = purchase_family.exclude(
                        Q(caracteristiques__contains=[cls.Characteristic[label.upper()]])
                    ).distinct()
                key = "valeur_" + family + "_" + label
                data[key] = purchase_family_label.aggregate(total=Sum("prix_ht"))["total"] or 0

    @classmethod
    def _complete_diag_data_appro_label_bio_dont_commerce_equitable(cls, purchases, data):
        """
        How we manage bio_dont_commerce_equitable:
        - outside of APPRO_LABELS_EGALIM
        - products can be counted twice across characteristics
        """
        from data.models import Diagnostic

        for family in Diagnostic.APPRO_FAMILIES:
            purchase_family = purchases.filter(famille_produits=family.upper())
            purchase_family_label = purchase_family.filter(
                Q(caracteristiques__contains=[cls.Characteristic.BIO])
                & Q(caracteristiques__contains=[cls.Characteristic.COMMERCE_EQUITABLE])
            )
            key = "valeur_" + family + "_" + "bio_dont_commerce_equitable"
            data[key] = purchase_family_label.aggregate(total=Sum("prix_ht"))["total"] or 0

    @classmethod
    def _complete_diag_appro_labels_france_circuit_court_local_2025(cls, purchases, data):
        """
        How we manage France/Circuit court/local:
        - outside of APPRO_LABELS_EGALIM
        - products can be counted in multiple of these characteristics
        - NOTE: in 2025, circuit_court & local were part of France, so we count them as France
        - NOTE: in 2025, Europe did not exist yet
        """
        from data.models import Diagnostic

        for family in Diagnostic.APPRO_FAMILIES:
            purchase_family = purchases.filter(famille_produits=family.upper())
            other_labels_characteristics = []
            for label in Diagnostic.APPRO_LABELS_FRANCE_SUBCATEGORIES:
                characteristic = cls.Characteristic[label.upper()]
                purchase_family_label = purchase_family.filter(Q(caracteristiques__contains=[characteristic]))
                key = "valeur_" + family + "_" + label
                data[key] = purchase_family_label.aggregate(total=Sum("prix_ht"))["total"] or 0
                other_labels_characteristics.append(characteristic)
            # France total
            purchase_family_label = purchase_family.filter(
                caracteristiques__overlap=cls.CHARACTERISTIC_LABELS_FRANCE_CIRCUIT_COURT_LOCAL
            ).distinct()
            key = "valeur_" + family + "_france"
            data[key] = purchase_family_label.aggregate(total=Sum("prix_ht"))["total"] or 0

    @classmethod
    def _complete_diag_appro_labels_france_circuit_court_local(cls, purchases, data):
        """
        How we manage France/Circuit court/local:
        - outside of APPRO_LABELS_EGALIM
        - products can be counted in multiple of these characteristics
        - NOTE: circuit_court & local are not counted as France
        - TODO: in 2026, Europe was added
        """
        from data.models import Diagnostic

        for family in Diagnostic.APPRO_FAMILIES:
            purchase_family = purchases.filter(famille_produits=family.upper())
            for label in cls.CHARACTERISTIC_LABELS_FRANCE_CIRCUIT_COURT_LOCAL:
                characteristic = cls.Characteristic[label]
                purchase_family_label = purchase_family.filter(Q(caracteristiques__contains=[characteristic]))
                key = "valeur_" + family + "_" + label.lower()
                data[key] = purchase_family_label.aggregate(total=Sum("prix_ht"))["total"] or 0

    @classmethod
    def _complete_diag_appro_labels_non_egalim(cls, purchases, data):
        """
        How we manage Non-EGalim:
        """
        from data.models import Diagnostic

        for family in Diagnostic.APPRO_FAMILIES:
            non_egalim_purchases = purchases.filter(famille_produits=family.upper()).exclude(
                caracteristiques__overlap=cls.CHARACTERISTIC_LABELS_EGALIM
            )
            key = "valeur_" + family + "_non_egalim"
            data[key] = non_egalim_purchases.aggregate(total=Sum("prix_ht"))["total"] or 0

    @classmethod
    def _misc_totals(cls, purchases, data):
        stats = purchases.aggregated_stats()
        data["valeur_viandes_volailles"] = stats["valeur_viandes_volailles"] or 0
        data["valeur_viandes_volailles_egalim"] = stats["valeur_viandes_volailles_egalim"] or 0
        data["valeur_viandes_volailles_france"] = stats["valeur_viandes_volailles_france"] or 0
        data["valeur_produits_de_la_mer"] = stats["valeur_produits_de_la_mer"] or 0
        data["valeur_produits_de_la_mer_egalim"] = stats["valeur_produits_de_la_mer_egalim"] or 0
