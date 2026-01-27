from django.db import models


class ImportType(models.TextChoices):
    CANTEEN_ONLY = "CANTEEN_ONLY", "Cantines seules"
    CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE = (
        "CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE",
        "Cantines seules ou avec un diagnostic simple",
    )  # plus utilisé
    DIAGNOSTIC_SIMPLE = "DIAGNOSTIC_SIMPLE", "Diagnostic simple"
    DIAGNOSTIC_COMPLETE = "DIAGNOSTIC_COMPLETE", "Cantines avec diagnostic complet"
    CC_SIMPLE = "CC_SIMPLE", "Cuisines centrales avec un diagnostic simple et leurs restaurants satellites"
    CC_COMPLETE = "CC_COMPLETE", "Cuisines centrales avec un diagnostic complet et leurs restaurants satellites"
    PURCHASE = "PURCHASE_SIRET", "Achats par SIRET"
    PURCHASE_ID = "PURCHASE_ID", "Achats par ID"
