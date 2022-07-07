from datetime import date
from django.db import models
from data.fields import ChoiceArrayField
from .canteen import Canteen


class Purchase(models.Model):
    class Meta:
        verbose_name = "achat"
        verbose_name_plural = "achats"
        ordering = ["-date", "-creation_date"]

    class Category(models.TextChoices):
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
        PRODUITS_DE_LA_MER = "PRODUITS_DE_LA_MER", "Produits aquatiques frais et surgelés"
        FRUITS_ET_LEGUMES = "FRUITS_ET_LEGUMES", "Fruits et légumes frais et surgelés"
        PRODUITS_LAITIERS = "PRODUITS_LAITIERS", "BOF (Produits laitiers, beurre et œufs)"
        BOULANGERIE = "BOULANGERIE", "Boulangerie/Pâtisserie fraîches"
        BOISSONS = "BOISSONS", "Boissons"
        AUTRES = "AUTRES", "Autres produits frais, surgelés et d’épicerie"

    class Characteristic(models.TextChoices):
        BIO = "BIO", "Bio"
        CONVERSION_BIO = "CONVERSION_BIO", "En conversion bio"  # not used anymore
        LABEL_ROUGE = "LABEL_ROUGE", "Label rouge"
        AOCAOP = "AOCAOP", "AOC / AOP"
        # ICP here is a typo
        IGP = "ICP", "Indication géographique protégée"
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
        FRANCE = "FRANCE", "Provenance France"
        SHORT_DISTRIBUTION = "SHORT_DISTRIBUTION", "Circuit-court"
        LOCAL = "LOCAL", "Produit local"

    class Local(models.TextChoices):
        REGION = "REGION", "Région"
        DEPARTMENT = "DEPARTMENT", "Département"
        AUTOUR_SERVICE = "AUTOUR_SERVICE", "200 km autour du lieu de service"
        AUTRE = "AUTRE", "Autre"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    description = models.TextField(null=True, blank=True, verbose_name="description du produit")
    provider = models.TextField(null=True, blank=True, verbose_name="fournisseur")
    category = models.CharField(
        max_length=255, choices=Category.choices, null=True, blank=True, verbose_name="catégorie"
    )
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
    )
    invoice_file = models.FileField(null=True, blank=True, upload_to="invoices/%Y/")
    local_definition = models.CharField(
        max_length=255, choices=Local.choices, null=True, blank=True, verbose_name="définition de local"
    )
    import_source = models.TextField(null=True, blank=True, verbose_name="source de l'import du produit")

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
