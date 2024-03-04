from django.db import models


class ImportType(models.TextChoices):
    CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE = "CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE", "Canteen only or simple diagnostic"
    DIAGNOSTIC_COMPLETE = "DIAGNOSTIC_COMPLETE", "Diagnostic complete"
    CC_SIMPLE = "CC_SIMPLE", "Central kitchen simple"
    CC_COMPLETE = "CC_COMPLETE", "Central kitchen complete"
    PURCHASE = "PURCHASE", "Purchase"
