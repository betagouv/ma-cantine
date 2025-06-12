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
                name="sectors", type=int, many=True, description="Filter by sector(s), using their internal id"
            ),
        ]
    )
    def get(self, request):
        year = request.query_params.get("year")
        regions = request.query_params.getlist("region")
        departments = request.query_params.getlist("department")
        epcis = request.query_params.getlist("epci")
        pats = request.query_params.getlist("pat")
        sectors = request.query_params.getlist("sectors")

        if not year:
            return JsonResponse({"error": "Expected year"}, status=status.HTTP_400_BAD_REQUEST)

        canteens = self._filter_canteens(regions, departments, epcis, pats, sectors)
        teledeclarations = self._filter_teledeclarations(year, regions, departments, epcis, pats, sectors)

        data = self.serializer_class.calculate_statistics(canteens, teledeclarations)

        serializer = self.serializer_class(data)
        return JsonResponse(camelize(serializer.data), status=status.HTTP_200_OK)

    def _filter_canteens(self, regions, departments, epcis, pats, sectors):
        canteens = Canteen.objects
        if epcis:
            canteens = canteens.filter(epci__in=epcis)
        if pats:
            canteens = canteens.filter(pat_list__overlap=pats)
        if departments:
            canteens = canteens.filter(department__in=departments)
        if regions:
            canteens = canteens.filter(region__in=regions)
        if sectors:
            canteens = canteens.filter(sectors__in=[s for s in sectors if s.isdigit()])
        return canteens.distinct()

    def _filter_teledeclarations(self, year, regions, departments, epcis, pats, sectors):
        teledeclarations = Teledeclaration.objects.valid_td_by_year(year)
        if teledeclarations:
            if epcis:
                teledeclarations = teledeclarations.filter(canteen__epci__in=epcis)
            if pats:
                teledeclarations = teledeclarations.filter(canteen__pat_list__overlap=pats)
            if departments:
                teledeclarations = teledeclarations.filter(canteen__department__in=departments)
            if regions:
                teledeclarations = teledeclarations.filter(canteen__region__in=regions)
            if sectors:
                teledeclarations = teledeclarations.filter(canteen__sectors__in=sectors)
            return teledeclarations.distinct()
