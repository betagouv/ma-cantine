from django.contrib import admin
from data.models import Purchase
from .utils import ReadOnlyAdminMixin, get_arrayfield_list_filter


@admin.register(Purchase)
class PurchaseAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
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
    )
    read_only_fields = fields
    list_display = (
        "date",
        "description",
        "family",
        "characteristics",
        "canteen",
        "price_ht",
    )
    list_filter = ("family", get_arrayfield_list_filter("characteristics", "Caractéristique"))
