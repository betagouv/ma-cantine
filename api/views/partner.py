from collections import OrderedDict
import logging
import random
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from api.serializers import PartnerSerializer, PartnerShortSerializer, PartnerContactSerializer
from data.models import Partner

logger = logging.getLogger(__name__)


class PartnersPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 30
    types = []
    departments = []
    sector_categories = []

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

        sector_categories = published_partners.values_list("sector_categories", flat=True).distinct()
        for sector_categories_list in sector_categories:
            if sector_categories_list is not None:
                for department in sector_categories_list:
                    if department not in self.sector_categories:
                        self.sector_categories.append(department)

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("results", data),
                    ("types", self.types),
                    ("departments", self.departments),
                    ("sector_categories", self.sector_categories),
                ]
            )
        )


class PartnersView(ListCreateAPIView):
    model = Partner
    pagination_class = PartnersPagination
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PartnerContactSerializer
        return PartnerShortSerializer

    def get_queryset(self):
        queryset = Partner.objects.filter(published=True)

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
        sector_categories = self.request.query_params.getlist("sectorCategories", [])
        if sector_categories:
            queryset = queryset.filter(sector_categories__overlap=sector_categories)
        gratuityOptions = self.request.query_params.getlist("gratuityOption", [])
        if gratuityOptions:
            queryset = queryset.filter(gratuity_option__in=gratuityOptions)
        return self.randomize_queryset(queryset)

    def randomize_queryset(self, queryset):
        seed = self.get_seed()
        cursor = connection.cursor()
        cursor.execute("SELECT setseed(%s);" % (seed))
        cursor.close()
        return queryset.order_by("?")

    def get_seed(self):
        if not self.request.session.get("seed"):
            self.request.session["seed"] = random.uniform(-1, 1)
        return self.request.session.get("seed")


class PartnerView(RetrieveAPIView):
    model = Partner
    queryset = Partner.objects.filter(published=True)
    serializer_class = PartnerSerializer
