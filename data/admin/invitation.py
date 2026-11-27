from django.contrib import admin

from data.models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "creation_date",
        "category",
        "status",
        "creation_canteen",
        "invited_canteen",
        "answer_date",
    )
    list_filter = (
        "category",
        "status",
        "creation_date",
    )
    search_fields = (
        "creation_canteen__name",
        "creation_canteen__siret",
        "creation_canteen__siren_unite_legale",
        "invited_canteen__name",
        "invited_canteen__siret",
        "invited_canteen__siren_unite_legale",
    )
    search_help_text = "La recherche est faite sur les champs : cantine qui a envoyé l'invitation & cantine invitée (nom, siret, siren de l'unité légale)"
    autocomplete_fields = (
        "creation_canteen",
        "invited_canteen",
    )
    raw_id_fields = (
        "creation_user",
        "answer_user",
    )
    readonly_fields = (
        "creation_date",
        "modification_date",
    )
