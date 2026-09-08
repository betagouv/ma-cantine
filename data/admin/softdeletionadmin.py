from django.contrib import admin
from django.http import HttpResponseRedirect
from simple_history.admin import SimpleHistoryAdmin


@admin.action(description="Restaurer les objets supprimés")
def restore_objects(modeladmin, request, queryset):
    queryset.update(deletion_date=None)


class SoftDeletionAdmin(admin.ModelAdmin):
    actions = [restore_objects]

    def get_queryset(self, request):
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        # Note: it used to call obj.hard_delete()
        obj.delete(skip_validations=True)

    def delete_queryset(self, request, queryset):
        # Note: it used to return queryset.hard_delete()
        return queryset.delete()

    @admin.display(description="Supprimée")
    def deleted(self, obj):
        return "🗑️ Supprimée" if obj.deletion_date else ""

    @admin.display(description="Statut de suppression")
    def deletion_status(self, obj):
        return "🗑️ Supprimée" if obj.deletion_date else "✔️ Active"

    def response_change(self, request, obj):
        """
        Override the response_change method to handle the restore_action.
        - the restore button replaces the deletion link
        - see the change_form.html template
        """
        if "restore_action" in request.POST:
            obj.deletion_date = None
            try:
                obj.save(skip_validations=True)
            except TypeError:
                obj.save()
            self.message_user(request, "Objet restauré avec succès.")
            # Redirect to the same page to show the updated object
            return HttpResponseRedirect(request.path)
        return super().response_change(request, obj)


class SoftDeletionHistoryAdmin(SoftDeletionAdmin, SimpleHistoryAdmin):
    pass


class SoftDeletionStatusFilter(admin.SimpleListFilter):
    title = "statut de suppression par l'utilisateur"

    parameter_name = "deletion_status"

    def lookups(self, request, model_admin):
        return (
            (None, "✔️ Active"),
            ("deleted", "🗑️ Supprimée"),
            ("all", "All"),
        )

    # need to override choices otherwise django adds 'all' as the
    # None value choice, whereas in this case None is 'Active'
    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": cl.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter(deletion_date=None)
        elif self.value() in ("all"):
            return queryset
        elif self.value() in ("deleted"):
            return queryset.filter(deletion_date__isnull=False)
