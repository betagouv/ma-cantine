from django.contrib import admin
from data.models import CanteenSectorRelation


class CanteenSectorInline(admin.TabularInline):
    model = CanteenSectorRelation
    show_change_link = False
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False
