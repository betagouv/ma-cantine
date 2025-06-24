import logging

from django.http import JsonResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.views import APIView

from api.serializers import CanteenStatisticsSerializer
from api.views.utils import camelize
from data.models import Canteen, Teledeclaration

logger = logging.getLogger(__name__)


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
        year = request.query_params.get("year")
        regions = request.query_params.getlist("region")
        departments = request.query_params.getlist("department")
        epcis = request.query_params.getlist("epci")
        pats = request.query_params.getlist("pat")
        cities = request.query_params.getlist("city")
        sectors = request.query_params.getlist("sectors")
        sectors = [s for s in sectors if s.isdigit()]
        management_types = request.query_params.getlist("management_type")
        production_types = request.query_params.getlist("production_type")
        economic_models = request.query_params.getlist("economic_model")

        if not year:
            return JsonResponse({"error": "Expected year"}, status=status.HTTP_400_BAD_REQUEST)

        canteens = self._filter_canteens(
            regions, departments, epcis, pats, cities, sectors, management_types, production_types, economic_models
        )
        teledeclarations = self._filter_teledeclarations(
            year,
            regions,
            departments,
            epcis,
            pats,
            cities,
            sectors,
            management_types,
            production_types,
            economic_models,
        )

        data = self.serializer_class.calculate_statistics(canteens, teledeclarations)

        serializer = self.serializer_class(data)
        return JsonResponse(camelize(serializer.data), status=status.HTTP_200_OK)

    def _filter_canteens(
        self, regions, departments, epcis, pats, cities, sectors, management_types, production_types, economic_models
    ):
        canteens = Canteen.objects.publicly_visible()
        if cities:
            canteens = canteens.filter(city_insee_code__in=cities)
        if pats:
            canteens = canteens.filter(pat_list__overlap=pats)
        if epcis:
            canteens = canteens.filter(epci__in=epcis)
        if departments:
            canteens = canteens.filter(department__in=departments)
        if regions:
            canteens = canteens.filter(region__in=regions)
        if sectors:
            canteens = canteens.filter(sectors__in=sectors)
        if management_types:
            canteens = canteens.filter(management_type__in=management_types)
        if production_types:
            canteens = canteens.filter(production_type__in=production_types)
        if economic_models:
            canteens = canteens.filter(economic_model__in=economic_models)
        return canteens.distinct()

    def _filter_teledeclarations(
        self,
        year,
        regions,
        departments,
        epcis,
        pats,
        cities,
        sectors,
        management_types,
        production_types,
        economic_models,
    ):
        teledeclarations = Teledeclaration.objects.publicly_visible().valid_td_by_year(year)
        if cities:
            teledeclarations = teledeclarations.filter(canteen__city_insee_code__in=cities)
        if pats:
            teledeclarations = teledeclarations.filter(canteen__pat_list__overlap=pats)
        if epcis:
            teledeclarations = teledeclarations.filter(canteen__epci__in=epcis)
        if departments:
            teledeclarations = teledeclarations.filter(canteen__department__in=departments)
        if regions:
            teledeclarations = teledeclarations.filter(canteen__region__in=regions)
        if sectors:
            teledeclarations = teledeclarations.filter(canteen__sectors__in=sectors)
        if management_types:
            teledeclarations = teledeclarations.filter(canteen__management_type__in=management_types)
        if production_types:
            teledeclarations = teledeclarations.filter(canteen__production_type__in=production_types)
        if economic_models:
            teledeclarations = teledeclarations.filter(canteen__economic_model__in=economic_models)
        return teledeclarations.distinct()
