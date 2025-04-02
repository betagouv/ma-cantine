from django.db.models import F
from django.db.models.constants import LOOKUP_SEP
from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camel_to_underscore
from rest_framework import filters


class MaCantineOrderingFilter(filters.OrderingFilter):
    """
    Allows filtering with camel case parameters. More info :
    https://github.com/vbabiy/djangorestframework-camel-case/issues/87
    Also sets null values last as opposed to DRF's default value of
    setting them first.
    """

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        def make_f_object(x):
            return F(x[1:]).desc(nulls_last=True) if x[0] == "-" else F(x).asc(nulls_first=True)

        if ordering:
            ordering = map(make_f_object, ordering)
            queryset = queryset.order_by(*ordering)
            queryset = queryset.distinct()  # to solve issues with duplicate/missing results

        return queryset

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [
                camel_to_underscore(
                    field.strip(),
                    **api_settings.JSON_UNDERSCOREIZE,
                )
                for field in params.split(",")
            ]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering

        return self.get_default_ordering(view)


class UnaccentSearchFilter(filters.SearchFilter):
    def construct_search(self, field_name, queryset):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = "icontains"
        return LOOKUP_SEP.join(
            [
                field_name,
                "unaccent",
                lookup,
            ]
        )
