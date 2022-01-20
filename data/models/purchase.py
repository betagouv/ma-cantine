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
        VIANDES_VOLAILLES = "VIANDES_VOLAILLES", "Viandes / volailles"
        FRUITS_ET_LEGUMES = "FRUITS_ET_LEGUMES", "Fruits, légumes"
        PECHE = "PECHE", "Pêche"
        PRODUITS_LAITIERS = "PRODUITS_LAITIERS", "Produits laitiers"
        PRODUITS_TRANSFORMES = "PRODUITS_TRANSFORMES", "Produits transformés"

    class Characteristic(models.TextChoices):
        BIO = "BIO", "Bio"
        AOCAOP = "AOCAOP", "AOC / AOP"
        RUP = "RUP", "RUP"
        LABEL_ROUGE = "LABEL_ROUGE", "Label rouge"
        PECHE_DURABLE = "PECHE_DURABLE", "Pêche durable"
        LOCAL = "LOCAL", "Local"
        HVE = "HVE", "HVE"
        COMMERCE_EQUITABLE = "COMMERCE_EQUITABLE", "Commerce équitable"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    provider = models.TextField(null=True, blank=True, verbose_name="Fournisseur")
    category = models.CharField(
        max_length=255, choices=Category.choices, null=True, blank=True, verbose_name="Catégorie"
    )
    characteristics = ChoiceArrayField(
        base_field=models.CharField(
            max_length=255, choices=Characteristic.choices, null=True, blank=True, verbose_name="Caractéristique"
        ),
        blank=True,
        null=True,
        size=None,
        verbose_name="Caractéristiques",
    )
    price_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Prix HT",
    )
    invoice_file = models.FileField(null=True, blank=True, upload_to="invoices/%Y/")
