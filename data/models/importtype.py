from django.db import models


class ImportType(models.TextChoices):
    CANTEEN_ONLY = "CANTEEN_ONLY", "Cantines seules"  # plus utilisé
    CANTEEN_CREATE = "CANTEEN_CREATE", "Cantines créées"
    CANTEEN_UPDATE = "CANTEEN_UPDATE", "Cantines mises à jour"
    CANTEEN_MANAGERS = "CANTEEN_MANAGERS", "Cantines avec gestionnaires"
    CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE = (
        "CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE",
        "Cantines seules ou avec un diagnostic simple",
    )  # plus utilisé
    DIAGNOSTIC_SIMPLE_SIRET = "DIAGNOSTIC_SIMPLE_SIRET", "Bilans simples par SIRET"
    DIAGNOSTIC_SIMPLE_ID = "DIAGNOSTIC_SIMPLE_ID", "Bilans simples par ID"
    DIAGNOSTIC_COMPLETE = "DIAGNOSTIC_COMPLETE", "Cantines avec diagnostic complet"
    CC_SIMPLE = "CC_SIMPLE", "Cuisines centrales avec un diagnostic simple et leurs restaurants satellites"
    CC_COMPLETE = "CC_COMPLETE", "Cuisines centrales avec un diagnostic complet et leurs restaurants satellites"
    PURCHASE = "PURCHASE_SIRET", "Achats par SIRET"
    PURCHASE_ID = "PURCHASE_ID", "Achats par ID"
