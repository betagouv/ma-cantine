from django.contrib import admin
from data.models import ManagerInvitation


@admin.register(ManagerInvitation)
class ManagerInvitationAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "canteen",
        "creation_date",
    )
    list_filter = ("canteen",)
