import logging

from django.http import JsonResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.views import APIView

from api.serializers import CanteenStatisticsSerializer
from api.views.utils import camelize
from common.api.decoupage_administratif import fetch_communes_from_epci
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
            OpenApiParameter(name="region", type=str, description="Filter by regions, using their INSEE code"),
            OpenApiParameter(name="department", type=str, description="Filter by departments, using their INSEE code"),
            OpenApiParameter(name="epci", type=str, description="Filter by EPCIS, using their INSEE code"),
            OpenApiParameter(name="sectors", type=int, description="Filter by sectors, using their id"),
        ]
    )
    def get(self, request):
        year = request.query_params.get("year")
        regions = request.query_params.getlist("region")
        departments = request.query_params.getlist("department")
        epcis = request.query_params.getlist("epci")
        sectors = request.query_params.getlist("sectors")

        if not year:
            return JsonResponse({"error": "Expected year"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            city_insee_codes = self._get_city_insee_codes(epcis)
        except Exception as e:
            logger.warning(f"Error when fetching INSEE codes for EPCI for canteen stats: {str(e)}")
            city_insee_codes = None
            epci_error = "Une erreur est survenue"
        else:
            epci_error = None

        canteens = self._filter_canteens(regions, departments, city_insee_codes, sectors)
        teledeclarations = self._filter_teledeclarations(year, regions, departments, city_insee_codes, sectors)

        data = self.serializer_class.calculate_statistics(canteens, teledeclarations)
        if epci_error:
            data["epci_error"] = epci_error

        serializer = self.serializer_class(data)
        return JsonResponse(camelize(serializer.data), status=status.HTTP_200_OK)

    def _get_city_insee_codes(self, epcis):
        city_insee_codes = []
        for e in epcis:
            response = fetch_communes_from_epci(e)
            city_insee_codes.extend(commune["code"] for commune in response)
        return city_insee_codes

    def _filter_canteens(self, regions, departments, city_insee_codes, sectors):
        canteens = Canteen.objects
        if city_insee_codes:
            canteens = canteens.filter(city_insee_code__in=city_insee_codes)
        elif departments:
            canteens = canteens.filter(department__in=departments)
        elif regions:
            canteens = canteens.filter(region__in=regions)
        if sectors:
            canteens = canteens.filter(sectors__in=[s for s in sectors if s.isdigit()])
        return canteens.distinct()

    def _filter_teledeclarations(self, year, regions, departments, city_insee_codes, sectors):
        teledeclarations = Teledeclaration.objects.valid_td_by_year(year)
        if teledeclarations:
            if city_insee_codes:
                teledeclarations = teledeclarations.filter(canteen__city_insee_code__in=city_insee_codes)
            elif departments:
                teledeclarations = teledeclarations.filter(canteen__department__in=departments)
            elif regions:
                teledeclarations = teledeclarations.filter(canteen__region__in=regions)
            if sectors:
                teledeclarations = teledeclarations.filter(canteen__sectors__in=sectors)
            return teledeclarations.distinct()
