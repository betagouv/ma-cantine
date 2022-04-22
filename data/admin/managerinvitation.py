from django.contrib import admin
from data.models import ManagerInvitation


@admin.register(ManagerInvitation)
class ManagerInvitationAdmin(admin.ModelAdmin):

    list_display = (
        "creation_date",
        "email",
        "canteen",
        "siret",
    )
    list_filter = ("canteen",)

    def siret(self, obj):
        return obj.canteen.siret
