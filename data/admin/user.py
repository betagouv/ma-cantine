import json

from django import forms
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from data.models import User

from .canteen import CanteenInline
from .diagnostic import UserDiagnosticInline


class UserForm(UserChangeForm):
    class Meta:
        widgets = {
            "creation_mtm_source": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_campaign": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_medium": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "other_job_description": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "other_source_description": forms.Textarea(attrs={"cols": 60, "rows": 2}),
        }


class HasTOTPDeviceFilter(admin.SimpleListFilter):
    title = _("TOTP Device ?")
    parameter_name = "has_totp_device"

    def lookups(self, request, model_admin):
        return (("yes", "Oui"), ("no", "Non"))

    def queryset(self, request, queryset):
        annotated = queryset.annotate_with_totp_device()
        if self.value() == "yes":
            return annotated.filter(has_totp_device=True)
        if self.value() == "no":
            return annotated.filter(has_totp_device=False)


@admin.register(User)
class MaCanteenUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "email_confirmed",
        "date_joined",
    )
    list_filter = (
        "email_confirmed",
        "is_elected_official",
        "is_dev",
        "is_staff",
        "is_superuser",
        HasTOTPDeviceFilter,
    )
    search_fields = (
        "id",
        "first_name",
        "last_name",
        "email",
        "username",
    )
    search_help_text = "La recherche est faite sur les champs : ID, prénom, nom, email, nom d'utilisateur."

    form = UserForm
    inlines = (CanteenInline, UserDiagnosticInline)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                    "phone_number",
                    "is_dev",
                    "job",
                    "other_job_description",
                )
            },
        ),
        (
            _("Section pour les élu·e·s"),
            {
                "fields": (
                    "is_elected_official",
                    "departments",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "email_confirmed",
                    "is_staff",
                    "is_superuser",
                    "has_totp_device",
                ),
            },
        ),
        (
            _("Brevo"),
            {
                "fields": (*User.BREVO_FIELDS,),
            },
        ),
        (
            _("EY - Connaissance de la loi EGalim"),
            {
                "fields": ("law_awareness",),
            },
        ),
        (
            "Lien tracké lors de la création",
            {
                "fields": (
                    *User.MATOMO_FIELDS,
                    "source",
                    "other_source_description",
                )
            },
        ),
        ("Données calculées", {"fields": ("data_pretty",)}),
        ("Metadonnées", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = (
        "brevo_last_update_date",
        *User.MATOMO_FIELDS,
        "data_pretty",
        "last_login",
        "date_joined",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate_with_totp_device()
        return qs

    @admin.display(description="TOTP Device ?")
    def has_totp_device(self, obj):
        return obj.has_totp_device

    has_totp_device.boolean = True

    def data_pretty(self, obj):
        data = json.dumps(obj.data, indent=2)
        return mark_safe(f"<pre>{data}</pre>")

    data_pretty.short_description = User._meta.get_field("data").verbose_name


class UserInline(admin.TabularInline):
    model = User.canteens.through
    fields = ("user", "help", "active")  # and "delete" checkbox
    autocomplete_fields = ("user",)
    readonly_fields = ("help", "active")
    extra = 0
    verbose_name_plural = "Gestionnaires"

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    @admin.display(description="Gestionnaire")
    def help(self, obj):
        return "Pour retirer le gestionnaire de la cantine cochez la case, puis sauvegardez la modification."

    @admin.display(description="Est active")
    def active(self, obj):
        return "🗑️ Supprimée par l'utilisateur" if obj.canteen.deletion_date else "✔️"
