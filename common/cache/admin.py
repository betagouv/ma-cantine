from django.contrib import admin

from common.cache.models import Cache
from data.admin.utils import ReadOnlyAdminMixin


@admin.register(Cache)
class CacheAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("cache_key", "expires")
    search_fields = ("cache_key",)

    fields = ("cache_key", "value", "expires")

    def has_delete_permission(self, request, obj=None):
        return True
