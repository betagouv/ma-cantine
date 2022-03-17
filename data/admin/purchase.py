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
        "category",
        "characteristics",
        "canteen",
        "price_ht",
    )
    list_filter = ("category", get_arrayfield_list_filter("characteristics", "Caractéristique"))
