import json
from django.db.models.constants import LOOKUP_SEP
from django.db.models import F
from rest_framework import filters
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.util import camel_to_underscore
from djangorestframework_camel_case.settings import api_settings


def camelize(data):
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    return json.loads(camel_case_bytes.decode("utf-8"))


def normalise_siret(siret):
    return siret.replace(" ", "")


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
            return F(x[1:]).desc(nulls_first=True) if x[0] == "-" else F(x).asc(nulls_first=True)

        if ordering:
            ordering = map(make_f_object, ordering)
            queryset = queryset.order_by(*ordering)

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
    def construct_search(self, field_name):
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
