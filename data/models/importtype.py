from django.db import models


class ImportType(models.TextChoices):
    CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE = (
        "CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE",
        "Cantines seules ou avec un diagnostic simple",
    )
    DIAGNOSTIC_COMPLETE = "DIAGNOSTIC_COMPLETE", "Cantines avec diagnostic complet"
    CC_SIMPLE = "CC_SIMPLE", "Livreurs avec un diagnostic simple et leurs satellites"
    CC_COMPLETE = "CC_COMPLETE", "Livreurs avec un diagnostic complet et leurs satellites"
    PURCHASE = "PURCHASE", "Achats"
