from datetime import date
from decimal import Decimal

from django.core.validators import MinValueValidator, ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import ExtractYear

from common.utils import utils as utils_utils
from data.fields import ChoiceArrayField
from data.models import Canteen
from data.models.creation_source import CreationSource
from data.validators import purchase as purchase_validators

from .softdeletionmodel import SoftDeletionModel


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
        FRANCE = "FRANCE", "Origine France"
        CIRCUIT_COURT = "CIRCUIT_COURT", "Circuit-court"
        LOCAL = "LOCAL", "Produit local"

    class Local(models.TextChoices):
        REGION = "REGION", "Région"
        DEPARTEMENT = "DEPARTEMENT", "Département"
        AUTOUR_SERVICE = "AUTOUR_SERVICE", "200 km autour du lieu de service"
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

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    description = models.TextField(null=True, blank=True, verbose_name="description du produit")
    provider = models.TextField(null=True, blank=True, verbose_name="fournisseur")
    category = models.CharField(
        max_length=255, choices=PurchaseCategory.choices, null=True, blank=True, verbose_name="catégorie"
    )  # not used anymore
    family = models.CharField(
        max_length=255, choices=Family.choices, null=True, blank=True, verbose_name="famille de produits"
    )
    characteristics = ChoiceArrayField(
        base_field=models.CharField(
            max_length=255, choices=Characteristic.choices, null=True, blank=True, verbose_name="caractéristique"
        ),
        blank=True,
        null=True,
        size=None,
        verbose_name="caractéristiques",
    )
    price_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="prix HT",
        validators=[MinValueValidator(Decimal("0"))],
    )
    invoice_file = models.FileField(null=True, blank=True, upload_to="invoices/%Y/")
    local_definition = models.CharField(
        max_length=255, choices=Local.choices, null=True, blank=True, verbose_name="définition de local"
    )
    import_source = models.TextField(null=True, blank=True, verbose_name="source de l'import du produit")

    creation_source = models.CharField(
        max_length=255,
        choices=CreationSource.choices,
        blank=True,
        null=True,
        verbose_name="Source de création de l'achat",
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "achat"
        verbose_name_plural = "achats"
        ordering = ["-date", "-creation_date"]
        indexes = [models.Index(fields=["import_source"])]

    def clean(self, *args, **kwargs):
        validation_errors = utils_utils.merge_validation_errors(
            purchase_validators.validate_purchase_local_definition(self),
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
    def readable_family(self):
        if not self.family:
            return None
        try:
            return Purchase.Family(self.family).label
        except Exception:
            return None

    @property
    def readable_characteristics(self):
        if not self.characteristics:
            return None
        valid_characteristics = []
        for characteristic in self.characteristics:
            try:
                valid_characteristics.append(Purchase.Characteristic(characteristic).label)
            except Exception:
                pass
        return ", ".join(valid_characteristics) if valid_characteristics else None

    @classmethod
    def canteen_summary_for_year(cls, canteen, year):
        purchases = cls.objects.only("id", "family", "characteristics", "price_ht").filter(
            canteen=canteen, date__year=year
        )
        data = {"year": year}
        cls._simple_diag_data(purchases, data)
        cls._complete_diag_data(purchases, data)
        cls._misc_totals(purchases, data)

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
            purchases = cls.objects.only("id", "family", "characteristics", "price_ht").filter(
                canteen=canteen, date__year=year
            )
            cls._simple_diag_data(purchases, year_data)
            data["results"].append(year_data)

        return data

    @classmethod
    def _simple_diag_data(cls, purchases, data):
        bio_filter = Q(characteristics__overlap=cls.CHARACTERISTIC_LABELS_BIO)
        bio_commerce_equitable_filter = bio_filter & Q(
            characteristics__contains=[cls.Characteristic.COMMERCE_EQUITABLE]
        )
        siqo_filter = Q(characteristics__overlap=cls.CHARACTERISTIC_LABELS_SIQO)
        egalim_autres_filter = Q(characteristics__overlap=cls.CHARACTERISTIC_LABELS_EGALIM_AUTRES)
        egalim_autres_commerce_equitable_filter = egalim_autres_filter & Q(
            characteristics__contains=[cls.Characteristic.COMMERCE_EQUITABLE]
        )
        externalities_performance_filter = Q(
            characteristics__overlap=cls.CHARACTERISTIC_LABELS_EXTERNALITES_PERFORMANCE
        )

        data["valeur_totale"] = purchases.aggregate(total=Sum("price_ht"))["total"] or 0

        bio_purchases = purchases.filter(bio_filter).distinct()
        data["valeur_bio"] = bio_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
        data["valeur_bio_dont_commerce_equitable"] = (
            bio_purchases.filter(bio_commerce_equitable_filter).aggregate(total=Sum("price_ht"))["total"] or 0
        )

        # the remaining stats should ignore any bio products
        purchases_no_bio = purchases.exclude(bio_filter)
        siqo_purchases = purchases_no_bio.filter(siqo_filter).distinct()
        data["valeur_siqo"] = siqo_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

        # the remaining stats should also ignore any sustainable (SIQO) products
        purchases_no_bio_no_siqo = purchases_no_bio.exclude(siqo_filter)
        egalim_autres_purchases = purchases_no_bio_no_siqo.filter(egalim_autres_filter).distinct()
        data["valeur_egalim_autres"] = egalim_autres_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
        data["valeur_egalim_autres_dont_commerce_equitable"] = (
            egalim_autres_purchases.filter(egalim_autres_commerce_equitable_filter).aggregate(total=Sum("price_ht"))[
                "total"
            ]
            or 0
        )

        # the remaining stats should also ignore any "other EGalim" products
        purchases_no_bio_siqo_no_egalim_autres = purchases_no_bio_no_siqo.exclude(egalim_autres_filter)
        externalities_performance_purchases = purchases_no_bio_siqo_no_egalim_autres.filter(
            externalities_performance_filter
        ).distinct()
        data["valeur_externalites_performance"] = (
            externalities_performance_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
        )

    @classmethod
    def _complete_diag_data(cls, purchases, data):
        """
        Summary for detailed teledeclaration totals, by family and label.
        Note: the order of APPRO_LABELS_EGALIM is significant - determines which
        labels trump others when aggregating purchases.
        """
        from data.models import Diagnostic

        for family in Diagnostic.APPRO_FAMILIES:
            purchase_family = purchases.filter(family=family.upper())
            for label in Diagnostic.APPRO_LABELS_EGALIM:
                if label.upper() == "AOCAOP_IGP_STG":
                    purchase_family_label = purchase_family.filter(
                        characteristics__overlap=cls.CHARACTERISTIC_LABELS_AOCAOP_IGP_STG
                    ).distinct()
                    # the remaining stats should ignore already counted labels
                    purchase_family = purchase_family.exclude(
                        characteristics__overlap=cls.CHARACTERISTIC_LABELS_AOCAOP_IGP_STG
                    ).distinct()
                else:
                    purchase_family_label = purchase_family.filter(
                        Q(characteristics__contains=[cls.Characteristic[label.upper()]])
                    ).distinct()
                    # the remaining stats should ignore already counted labels
                    purchase_family = purchase_family.exclude(
                        Q(characteristics__contains=[cls.Characteristic[label.upper()]])
                    ).distinct()
                key = "valeur_" + family + "_" + label
                data[key] = purchase_family_label.aggregate(total=Sum("price_ht"))["total"] or 0
            # special case of bio_dont_commerce_equitable (products can be counted twice across characteristics)
            purchase_family = purchases.filter(family=family.upper())
            purchase_family_label = purchase_family.filter(
                Q(characteristics__contains=[cls.Characteristic.BIO])
                & Q(characteristics__contains=[cls.Characteristic.COMMERCE_EQUITABLE])
            )
            key = "valeur_" + family + "_" + "bio_dont_commerce_equitable"
            data[key] = purchase_family_label.aggregate(total=Sum("price_ht"))["total"] or 0
            # outside of EGalim (products can be counted twice across characteristics)
            purchase_family = purchases.filter(family=family.upper())
            other_labels_characteristics = []
            for label in Diagnostic.APPRO_LABELS_FRANCE_SUBCATEGORIES:
                characteristic = cls.Characteristic[label.upper()]
                purchase_family_label = purchase_family.filter(Q(characteristics__contains=[characteristic]))
                key = "valeur_" + family + "_" + label
                data[key] = purchase_family_label.aggregate(total=Sum("price_ht"))["total"] or 0
                other_labels_characteristics.append(characteristic)
            # France total
            purchase_family_label = purchase_family.filter(
                characteristics__overlap=cls.CHARACTERISTIC_LABELS_FRANCE_CIRCUIT_COURT_LOCAL
            ).distinct()
            key = "valeur_" + family + "_france"
            data[key] = purchase_family_label.aggregate(total=Sum("price_ht"))["total"] or 0
            other_labels_characteristics.append(cls.Characteristic.FRANCE)
            # Non-EGalim totals (contains no labels or only one or more of other_labels)
            non_egalim_purchases = purchase_family.filter(
                Q(characteristics__contained_by=(other_labels_characteristics + [""])) | Q(characteristics__len=0)
            ).distinct()
            key = "valeur_" + family + "_non_egalim"
            data[key] = non_egalim_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    @classmethod
    def _misc_totals(cls, purchases, data):
        # meat_poultry
        meat_poultry_purchases = purchases.filter(family=cls.Family.VIANDES_VOLAILLES)
        data["valeur_viandes_volailles"] = meat_poultry_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
        meat_poultry_egalim = meat_poultry_purchases.filter(characteristics__overlap=cls.CHARACTERISTIC_LABELS_EGALIM)
        data["valeur_viandes_volailles_egalim"] = meat_poultry_egalim.aggregate(total=Sum("price_ht"))["total"] or 0
        meat_poultry_france = meat_poultry_purchases.filter(characteristics__contains=[cls.Characteristic.FRANCE])
        data["valeur_viandes_volailles_france"] = meat_poultry_france.aggregate(total=Sum("price_ht"))["total"] or 0
        # fish
        fish_purchases = purchases.filter(family=cls.Family.PRODUITS_DE_LA_MER)
        data["valeur_produits_de_la_mer"] = fish_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
        fish_egalim = fish_purchases.filter(characteristics__overlap=cls.CHARACTERISTIC_LABELS_EGALIM)
        data["valeur_produits_de_la_mer_egalim"] = fish_egalim.aggregate(total=Sum("price_ht"))["total"] or 0
