from django.contrib import admin


class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ArrayFieldListFilter(admin.SimpleListFilter):
    "Admin-filterable field for an ArrayList"

    def __init__(self, request, params, model, model_admin):
        self._choices = model._meta.get_field(self.parameter_name).base_field.choices
        super(ArrayFieldListFilter, self).__init__(request, params, model, model_admin)

    def lookups(self, request, model_admin):
        """ "Returns a list of tuples:
        (lookup value, human-readable value)
        for use in admins right sidebar
        """
        return self._choices

    def queryset(self, request, queryset):
        "Filter based on clicked value stored in self.value()"
        value = self.value()

        if value:
            queryset = queryset.filter(**{"{}__contains".format(self.parameter_name): [value]})

        return queryset


def get_arrayfield_list_filter(field_name, verbose_name):
    class ArrayFieldListFilterForField(ArrayFieldListFilter):
        parameter_name = field_name
        title = verbose_name

    return ArrayFieldListFilterForField
