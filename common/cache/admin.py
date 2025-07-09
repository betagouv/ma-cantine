from django.contrib import admin

from common.cache.models import Cache


@admin.register(Cache)
class CacheAdmin(admin.ModelAdmin):
    list_display = ("cache_key", "expires")
    search_fields = ("cache_key",)
    readonly_fields = ("cache_key", "expires")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
