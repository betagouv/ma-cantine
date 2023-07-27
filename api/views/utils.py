import logging
import json
from django.db.models.constants import LOOKUP_SEP
from django.db.models import F
from rest_framework import filters
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.util import camel_to_underscore
from djangorestframework_camel_case.settings import api_settings
from simple_history.utils import update_change_reason

logger = logging.getLogger(__name__)


def camelize(data):
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    return json.loads(camel_case_bytes.decode("utf-8"))


def normalise_siret(siret):
    return siret.replace(" ", "").replace("\xa0", "")


def update_change_reason_with_auth(view, object):
    try:
        update_change_reason(
            object, f"{view.request.successful_authenticator.__class__.__name__[:100]}"
        )  # The max allowed chars is 100
    except Exception as e:
        logger.warning(f"Unable to set reason change on {view.__class__.__name__} for object ID : {object.id}: \n{e}")
        update_change_reason(object, "Unknown")


def read_file_by_batch(file, batch_size):
    batches = []
    while True:
        batch = file.readlines(batch_size)
        if not batch:
            break
        batches.append(batch)
    return batches


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
