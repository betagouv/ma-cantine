from django.contrib import admin

from common.kombu.models import KombuMessage, KombuQueue
from data.admin.utils import ReadOnlyAdminMixin
from macantine.celery import ensure_sqlalchemy_broker_schema


@admin.register(KombuQueue)
class KombuQueueAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        ensure_sqlalchemy_broker_schema()
        return super().get_queryset(request)

    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(KombuMessage)
class KombuMessageAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        ensure_sqlalchemy_broker_schema()
        return super().get_queryset(request)

    list_display = ("id", "queue", "visible", "sent_at")
    list_filter = ("queue", "visible")
    search_fields = ("id", "payload", "queue__name")
    ordering = ("-id",)
    readonly_fields = ("id", "queue", "visible", "sent_at", "payload", "version")
