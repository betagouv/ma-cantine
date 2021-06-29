from django.contrib import admin
from data.models import ProvisionalManager


@admin.register(ProvisionalManager)
class ProvisionalManagerAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "canteen",
        "creation_date",
    )
    list_filter = ("canteen",)
