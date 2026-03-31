import logging

from django.core.cache import cache
from django.http import JsonResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CanteenStatisticsSerializer
from api.views.utils import camelize
from data.models import Canteen, Diagnostic
from data.models.sector import Sector
from data.models.geo import Department, Region
from macantine.utils import get_egalim_group
from data.utils import array_overlap_query

logger = logging.getLogger(__name__)


CACHE_KEY_PREFIX = "canteen_statistics"
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours  # TODO: reduce?

FILTER_QUERY_FIELDS_IN = [
    "region",
    "department",
    "epci",
    "city",
    "management_type",
    "production_type",
    "economic_model",
]
FILTER_QUERY_FIELDS_OVERLAP = ["pat", "sector"]  # fields that are lists in the model and need an overlap query
FILTER_QUERY_FIELDS = FILTER_QUERY_FIELDS_IN + FILTER_QUERY_FIELDS_OVERLAP


@extend_schema(
    summary="Récapitulatif statistique des données de ma-cantine",
)
class CanteenStatisticsView(APIView):
    include_in_documentation = True
    serializer_class = CanteenStatisticsSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="year", type=str, description="Filter by year of declared data", required=True),
            OpenApiParameter(
                name="region",
                type=str,
                many=True,
                description="Filter by region(s), using their Insee code",
                enum=Region,
            ),
            OpenApiParameter(
                name="department",
                type=str,
                many=True,
                description="Filter by department(s), using their Insee code",
                enum=Department,
            ),
            OpenApiParameter(
                name="epci", type=str, many=True, description="Filter by EPCI(s), using their Insee code"
            ),
            OpenApiParameter(name="pat", type=str, many=True, description="Filter by PAT(s), using their id"),
            OpenApiParameter(
                name="city", type=str, many=True, description="Filter by city(ies), using their Insee code"
            ),
            OpenApiParameter(
                name="sector",
                type=str,
                many=True,
                description="Filter by sector(s), using their full name",
                enum=Sector,
            ),
            OpenApiParameter(
                name="management_type",
                type=str,
                many=True,
                description="Filter by management type(s)",
                enum=Canteen.ManagementType,
            ),
            OpenApiParameter(
                name="production_type",
                type=str,
                many=True,
                description="Filter by production type(s)",
                enum=Canteen.ProductionType,
            ),
            OpenApiParameter(
                name="economic_model",
                type=str,
                many=True,
                description="Filter by economic model(s)",
                enum=Canteen.EconomicModel,
            ),
        ]
    )
    def get(self, request):
        """
        Get statistical summary of canteens and teledeclarations, filtered by query parameters.
        """
        year = request.query_params.get("year")
        if not year:
            return JsonResponse({"error": "Expected year"}, status=status.HTTP_400_BAD_REQUEST)

        # cache mechanism: only for requests with just the year parameter
        # TODO: refactor to a dedicated cache config file?
        if len(request.query_params) == 1 and year:
            cache_key = f"{CACHE_KEY_PREFIX}_{year}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return JsonResponse(cached_data, status=status.HTTP_200_OK)

        filters = self._extract_query_filters(request)
        egalim_group = self._get_egalim_group(filters)

        canteen_qs = (
            Canteen.all_objects.publicly_visible()
            .created_before_year_campaign_end_date(year)
            .not_deleted_before_year_campaign_end_date(year)
        )
        canteens = self._apply_canteen_filters(canteen_qs, filters)

        teledeclaration_qs = Diagnostic.all_objects.publicly_visible().valid_td_site_by_year(year)
        teledeclarations = self._apply_snapshot_filters(teledeclaration_qs, filters)

        data = self.serializer_class.calculate_statistics(canteens, teledeclarations)
        data["notes"] = self.serializer_class.generate_notes(year, egalim_group)
        data = self.serializer_class.hide_data_if_report_not_published(data, year)
        serializer = self.serializer_class(data)

        # cache mechanism: store the result if it was not cached (only for requests with just the year parameter)
        if len(request.query_params) == 1 and year:
            cache_key = f"{CACHE_KEY_PREFIX}_{year}"
            if not cache.get(cache_key):
                cache.set(cache_key, camelize(serializer.data), timeout=CACHE_TIMEOUT)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def _extract_query_filters(self, request):
        """
        Extract and clean filter parameters from the request.
        """
        return {field: request.query_params.getlist(field) for field in FILTER_QUERY_FIELDS}

    def _apply_canteen_filters(self, queryset, filters):
        """
        Apply filters to the canteen queryset.
        """
        for field in FILTER_QUERY_FIELDS_IN:
            if filters[field]:
                model_field = field if field != "city" else "city_insee_code"
                queryset = queryset.filter(**{f"{model_field}__in": filters[field]})
        for field in FILTER_QUERY_FIELDS_OVERLAP:
            if filters[field]:
                model_field = f"{field}_list"
                queryset = queryset.filter(**{f"{model_field}__overlap": filters[field]})
        return queryset.distinct()

    def _apply_snapshot_filters(self, queryset, filters):
        """
        Apply filters to the diagnostic snapshot queryset.
        """
        for field in FILTER_QUERY_FIELDS_IN:
            if filters[field]:
                model_field = field if field != "city" else "city_insee_code"
                queryset = queryset.filter(**{f"canteen_snapshot__{model_field}__in": filters[field]})
        for field in FILTER_QUERY_FIELDS_OVERLAP:
            if filters[field]:
                model_field = f"{field}_list"
                queryset = queryset.filter(array_overlap_query(f"canteen_snapshot__{model_field}", filters[field]))
        return queryset.distinct()

    def _get_egalim_group(self, filters):
        region_filter = filters.get("region")
        return get_egalim_group(region_filter)
