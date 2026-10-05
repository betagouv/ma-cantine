from django.contrib import admin
from oauth2_provider.admin import ApplicationAdmin
from oauth2_provider.models import get_application_model

from data.models import Oauth2ProviderApplicationExtra

Application = get_application_model()


class Oauth2ProviderApplicationExtraInline(admin.StackedInline):
    model = Oauth2ProviderApplicationExtra
    fields = ("company_name", "creation_date", "modification_date")
    readonly_fields = ("creation_date", "modification_date")
    can_delete = False
    min_num = 1
    max_num = 1


# replace the django-oauth-toolkit admin
admin.site.unregister(Application)


@admin.register(Application)
class Oauth2ProviderApplicationAdmin(ApplicationAdmin):
    list_display = ApplicationAdmin.list_display + ("extra__company_name", "created", "updated")
    list_select_related = ("user", "extra")
    search_fields = ApplicationAdmin.search_fields + ("extra__company_name",)
    inlines = (Oauth2ProviderApplicationExtraInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]
