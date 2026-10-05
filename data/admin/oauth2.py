from django.contrib import admin
from oauth2_provider.admin import ApplicationAdmin
from oauth2_provider.models import get_application_model

Application = get_application_model()


# replace the django-oauth-toolkit admin
admin.site.unregister(Application)


@admin.register(Application)
class Oauth2ProviderApplicationAdmin(ApplicationAdmin):
    list_display = ApplicationAdmin.list_display + ("created", "updated")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]
