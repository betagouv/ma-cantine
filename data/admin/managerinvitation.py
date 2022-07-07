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
    list_filter = ("creation_date",)
    search_fields = (
        "email",
        "canteen__siret",
        "canteen__name",
    )

    def siret(self, obj):
        return obj.canteen.siret
