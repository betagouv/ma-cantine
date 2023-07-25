from collections import OrderedDict
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from api.serializers import PartnerSerializer, PartnerShortSerializer, PartnerContactSerializer
from data.models import Partner, Sector

logger = logging.getLogger(__name__)


class PartnersPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 30
    types = []
    departments = []
    sectors = []

    def paginate_queryset(self, queryset, request, view=None):
        published_partners = Partner.objects.filter(published=True)
        self.types = published_partners.values_list("types__name", flat=True).distinct()
        self.types = [t for t in self.types if t is not None]
        self.departments = []
        departments = published_partners.values_list("departments", flat=True).distinct()
        for depList in departments:
            if depList is not None:
                for department in depList:
                    if department not in self.departments:
                        self.departments.append(department)
        self.sectors = (
            Sector.objects.filter(partner__in=list(published_partners)).values_list("id", flat=True).distinct()
        )
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("results", data),
                    ("types", self.types),
                    ("departments", self.departments),
                    ("sectors", self.sectors),
                ]
            )
        )


class PartnersView(ListCreateAPIView):
    model = Partner
    queryset = Partner.objects.filter(published=True)
    pagination_class = PartnersPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sectors"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PartnerContactSerializer
        return PartnerShortSerializer

    def get_queryset(self):
        queryset = self.queryset
        types = self.request.query_params.getlist("type", [])
        if types:
            queryset = queryset.filter(types__name__in=types)
        categories = self.request.query_params.getlist("category", [])
        if categories:
            queryset = queryset.filter(categories__overlap=categories)
        departments = self.request.query_params.getlist("department", [])
        if departments:
            queryset = queryset.filter(departments__overlap=departments)
            # TODO: add in national option ?
        only_free = self.request.query_params.get("free", None)
        # free AND/OR public ?
        if only_free:
            queryset = queryset.filter(free=True)
        return queryset


class PartnerView(RetrieveAPIView):
    model = Partner
    queryset = Partner.objects.filter(published=True)
    serializer_class = PartnerSerializer
