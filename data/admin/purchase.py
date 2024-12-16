from django.contrib import admin

from data.models import Purchase

from .softdeletionadmin import SoftDeletionAdmin, SoftDeletionStatusFilter
from .utils import get_arrayfield_list_filter


@admin.register(Purchase)
class PurchaseAdmin(SoftDeletionAdmin):
    fields = (
        "date",
        "canteen",
        "description",
        "provider",
        "family",
        "category",
        "characteristics",
        "price_ht",
        "invoice_file",
        "local_definition",
        "import_source",
        "deletion_date",
        "creation_date",
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
        "import_source",
        "creation_date",
    )
    list_display = (
        "date",
        "canteen",
        "description",
        "family",
        "characteristics",
        "price_ht",
        "deletion_status",
        "creation_date",
    )
    list_filter = (
        "family",
        get_arrayfield_list_filter("characteristics", "Caractéristique"),
        SoftDeletionStatusFilter,
        "deletion_date",
    )
    search_fields = (
        "description",
        "canteen__name",
        "canteen__siret",
        "import_source",
    )

    def canteen_name(self, obj):
        return obj.canteen.name
