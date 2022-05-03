from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from data.models import User
from .canteen import CanteenInline


class UserForm(forms.ModelForm):
    class Meta:
        widgets = {
            "other_job_description": forms.Textarea(attrs={"cols": 60, "rows": 2}),
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
    )
    readonly_fields = ("date_joined",)

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
                    "job",
                    "other_job_description",
                )
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
