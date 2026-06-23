from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from data.admin.softdeletionadmin import SoftDeletionAdmin, SoftDeletionStatusFilter
from data.admin.utils import get_arrayfield_list_filter
from data.models import Purchase
from data.models.creation_source import CreationSource


@admin.register(Purchase)
class PurchaseAdmin(SoftDeletionAdmin):
    list_display = (
        "date",
        "canteen_with_link",
        "description",
        "famille_produits",
        "caracteristiques",
        "prix_ht",
        "deleted",
        "creation_date",
    )
    list_filter = (
        "famille_produits",
        get_arrayfield_list_filter("caracteristiques", "Caractéristique"),
        SoftDeletionStatusFilter,
        "deletion_date",
    )
    search_fields = (
        "canteen__siret",
        "canteen__siren_unite_legale",
        "description",
        "import_source",
    )
    search_help_text = f"Cherche sur les champs : Cantine (SIRET), {Purchase._meta.get_field('description').verbose_name.capitalize()}, {Purchase._meta.get_field('import_source').verbose_name.capitalize()}"

    fields = (
        "date",
        "canteen",
        "description",
        "fournisseur",
        "famille_produits",
        "category",
        "caracteristiques",
        "prix_ht",
        "definition_local",
        "definition_local_km",
        "facture",
        *Purchase.CREATION_META_FIELDS,
        "deletion_date",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("canteen")
        return qs

    def get_readonly_fields(self, request, obj=None):
        return [field for field in self.fields if field not in ("deletion_date",)]

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        """
        - run validation (will be run on save())
        - set creation_source (on create)
        """
        if not change:
            obj.creation_user = request.user
            obj.creation_source = CreationSource.ADMIN
        super().save_model(request, obj, form, change)

    def canteen_name(self, obj):
        return obj.canteen.name

    def canteen_with_link(self, obj):
        url = reverse("admin:data_canteen_change", args=[obj.canteen_id])
        return format_html(f'<a href="{url}">{obj.canteen}</a>')

    canteen_with_link.short_description = Purchase._meta.get_field("canteen").verbose_name
