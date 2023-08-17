from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
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
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "username",
    )
    readonly_fields = (
        "date_joined",
        "creation_mtm_source",
        "creation_mtm_campaign",
        "creation_mtm_medium",
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
                ),
            },
        ),
        (
            _("EY - Connaissance de la loi EGALIM"),
            {
                "fields": ("law_awareness",),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            "Lien tracké lors de la création",
            {
                "fields": (
                    "creation_mtm_source",
                    "creation_mtm_campaign",
                    "creation_mtm_medium",
                    "source",
                    "other_source_description",
                )
            },
        ),
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
    list_filter = (
        "is_elected_official",
        "is_dev",
        "is_staff",
    )
