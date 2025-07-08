import logging

from django.core.cache import cache
from django.http import JsonResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.views import APIView

from api.serializers import CanteenStatisticsSerializer
from api.views.utils import camelize
from data.models import Canteen, Teledeclaration

logger = logging.getLogger(__name__)


CACHE_KEY_PREFIX = "canteen_statistics"
CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours


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
                name="region", type=str, many=True, description="Filter by region(s), using their Insee code"
            ),
            OpenApiParameter(
                name="department", type=str, many=True, description="Filter by department(s), using their Insee code"
            ),
            OpenApiParameter(
                name="epci", type=str, many=True, description="Filter by EPCI(s), using their Insee code"
            ),
            OpenApiParameter(name="pat", type=str, many=True, description="Filter by PAT(s), using their id"),
            OpenApiParameter(
                name="city", type=str, many=True, description="Filter by city(ies), using their Insee code"
            ),
            OpenApiParameter(
                name="sectors", type=int, many=True, description="Filter by sector(s), using their internal id"
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
        if len(request.query_params) == 1:
            cache_key = f"{CACHE_KEY_PREFIX}_{year}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return JsonResponse(cached_data, status=status.HTTP_200_OK)

        filters = self._extract_query_filters(request)

        canteen_qs = Canteen.objects.publicly_visible()
        canteens = self._apply_query_filters(canteen_qs, filters)

        teledeclaration_qs = Teledeclaration.objects.publicly_visible().valid_td_by_year(year)
        teledeclarations = self._apply_query_filters(teledeclaration_qs, filters, prefix="canteen__")

        data = self.serializer_class.calculate_statistics(canteens, teledeclarations)
        serializer = self.serializer_class(data)

        # cache mechanism: store the result if it was not cached (only for requests with just the year parameter)
        if len(request.query_params) == 1:
            cache_key = f"{CACHE_KEY_PREFIX}_{year}"
            if not cache.get(cache_key):
                cache.set(cache_key, camelize(serializer.data), timeout=CACHE_TIMEOUT)

        return JsonResponse(camelize(serializer.data), status=status.HTTP_200_OK)

    def _extract_query_filters(self, request):
        """
        Extract and clean filter parameters from the request.
        """
        sectors = [s for s in request.query_params.getlist("sectors") if str(s).isdigit()]
        return {
            "region__in": request.query_params.getlist("region"),
            "department__in": request.query_params.getlist("department"),
            "epci__in": request.query_params.getlist("epci"),
            "pat_list__overlap": request.query_params.getlist("pat"),
            "city_insee_code__in": request.query_params.getlist("city"),
            "sectors__in": sectors,
            "management_type__in": request.query_params.getlist("management_type"),
            "production_type__in": request.query_params.getlist("production_type"),
            "economic_model__in": request.query_params.getlist("economic_model"),
        }

    def _apply_query_filters(self, queryset, filters, prefix=""):
        """
        Apply filters to a queryset. If prefix is given, it is prepended to each filter key.
        """
        for key, value in filters.items():
            if value:
                filter_key = f"{prefix}{key}" if prefix else key
                queryset = queryset.filter(**{filter_key: value})
        return queryset.distinct()
