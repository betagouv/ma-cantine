from django.contrib import admin

from common.kombu.models import KombuMessage, KombuQueue


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(KombuQueue)
class KombuQueueAdmin(ReadOnlyAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(KombuMessage)
class KombuMessageAdmin(ReadOnlyAdmin):
    list_display = ("id", "queue", "visible", "sent_at")
    list_filter = ("queue", "visible")
    search_fields = ("id", "payload", "queue__name")
    ordering = ("-id",)
    readonly_fields = ("id", "queue", "visible", "sent_at", "payload", "version")
