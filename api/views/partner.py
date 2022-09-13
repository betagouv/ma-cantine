from collections import OrderedDict
import logging
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from api.serializers import PartnerSerializer, PartnerShortSerializer
from data.models import Partner

logger = logging.getLogger(__name__)


class PartnersPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 30
    types = []

    def paginate_queryset(self, queryset, request, view=None):
        self.types = Partner.objects.all().values_list("types__name", flat=True).distinct()
        self.types = [t for t in self.types if t is not None]
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("results", data),
                    ("types", self.types),
                ]
            )
        )


class PartnersView(ListAPIView):
    model = Partner
    serializer_class = PartnerShortSerializer
    queryset = Partner.objects.all()
    pagination_class = PartnersPagination

    def get_queryset(self):
        queryset = self.queryset
        types = self.request.query_params.getlist("type", [])
        if types:
            queryset = queryset.filter(types__name__in=types)
        departments = self.request.query_params.getlist("department", [])
        if departments:
            queryset = queryset.filter(departments__overlap=departments)
            # TODO: add in national option ?
        only_free = self.request.query_params.get("free", None)
        if only_free:
            queryset = queryset.filter(free=True)
        return queryset


class PartnerView(RetrieveAPIView):
    model = Partner
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
