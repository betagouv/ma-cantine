from django.contrib import admin
from data.models import Purchase
from .utils import get_arrayfield_list_filter
from .softdeletionadmin import SoftDeletionAdmin, SoftDeletionStatusFilter


@admin.register(Purchase)
class PurchaseAdmin(SoftDeletionAdmin):
    fields = (
        "canteen",
        "date",
        "description",
        "provider",
        "family",
        "category",
        "characteristics",
        "price_ht",
        "invoice_file",
        "local_definition",
        "deletion_date",
    )
    readonly_fields = (
        "canteen",
        "date",
        "description",
        "provider",
        "family",
        "category",
        "characteristics",
        "price_ht",
        "invoice_file",
        "local_definition",
    )
    list_display = (
        "date",
        "description",
        "family",
        "characteristics",
        "canteen",
        "price_ht",
    )
    list_filter = (
        "family",
        get_arrayfield_list_filter("characteristics", "Caractéristique"),
        SoftDeletionStatusFilter,
    )
