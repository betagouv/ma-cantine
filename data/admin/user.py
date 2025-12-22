import json

from django import forms
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from data.models import User

from .canteen import CanteenInline


class UserForm(UserChangeForm):
    class Meta:
        widgets = {
            "creation_mtm_source": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_campaign": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "creation_mtm_medium": forms.Textarea(attrs={"cols": 55, "rows": 1}),
            "other_job_description": forms.Textarea(attrs={"cols": 60, "rows": 2}),
            "other_source_description": forms.Textarea(attrs={"cols": 60, "rows": 2}),
        }


@admin.register(User)
class MaCanteenUserAdmin(UserAdmin):
    form = UserForm
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "email_confirmed",
        "date_joined",
    )
    list_filter = (
        "is_elected_official",
        "is_dev",
        "is_staff",
    )
    search_fields = (
        "id",
        "first_name",
        "last_name",
        "email",
        "username",
    )
    search_help_text = "La recherche est faite sur les champs : ID, prénom, nom, email, nom d'utilisateur."
    readonly_fields = (
        *User.MATOMO_FIELDS,
        "data_pretty",
        "last_login",
        "date_joined",
    )

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
                    "number_of_managed_cantines",
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
                    "is_staff",
                    "is_superuser",
                    "email_confirmed",
                ),
            },
        ),
        (
            _("Emails automatiques"),
            {
                "fields": (
                    "opt_out_reminder_emails",
                    "email_no_canteen_first_reminder",
                    "email_no_canteen_second_reminder",
                    "last_brevo_update",
                ),
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

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
    inlines = (CanteenInline,)

    def data_pretty(self, obj):
        data = json.dumps(obj.data, indent=2)
        return mark_safe(f"<pre>{data}</pre>")

    data_pretty.short_description = User._meta.get_field("data").verbose_name


class UserInline(admin.TabularInline):
    model = User.canteens.through
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
