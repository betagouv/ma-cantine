from django.contrib import admin
from oauth2_provider.admin import ApplicationAdmin
from oauth2_provider.models import get_application_model

from data.models import Oauth2ProviderApplicationExtra
from data.models.oauth2 import annotate_with_created_counts, get_application_created_count_managers

Application = get_application_model()
APPLICATION_CREATED_COUNT_FIELDS = list(get_application_created_count_managers())  # annotated in get_queryset


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
    list_display = ApplicationAdmin.list_display + (
        "extra__company_name",
        *APPLICATION_CREATED_COUNT_FIELDS,
        "created",
        "updated",
    )
    list_select_related = ("user", "extra")
    search_fields = ApplicationAdmin.search_fields + ("extra__company_name",)
    inlines = (Oauth2ProviderApplicationExtraInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        application_fields = [field.name for field in self.model._meta.fields]
        return application_fields + APPLICATION_CREATED_COUNT_FIELDS

    def get_queryset(self, request):
        return annotate_with_created_counts(super().get_queryset(request))

    @admin.display(description="Cantines créées (API)", ordering="canteens_created_count")
    def canteens_created_count(self, obj):
        return obj.canteens_created_count

    @admin.display(description="Bilans créés (API)", ordering="diagnostics_created_count")
    def diagnostics_created_count(self, obj):
        return obj.diagnostics_created_count

    @admin.display(description="Achats créés (API)", ordering="purchases_created_count")
    def purchases_created_count(self, obj):
        return obj.purchases_created_count

    @admin.display(description="Évaluations gaspillage créées (API)", ordering="waste_measurements_created_count")
    def waste_measurements_created_count(self, obj):
        return obj.waste_measurements_created_count
