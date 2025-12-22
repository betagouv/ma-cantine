from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.serializers import CampaignDatesSerializer, CampaignDatesFullSerializer
from macantine.utils import (
    CAMPAIGN_DATES,
    is_in_correction,
    is_in_teledeclaration,
)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les dates des campagnes.",
        tags=["teledeclaration"],
    ),
)
class TeledeclarationCampaignDatesListView(ListAPIView):
    include_in_documentation = True
    serializer_class = CampaignDatesSerializer

    def get(self, request, format=None):
        campaign_dates = []
        for year in CAMPAIGN_DATES.keys():
            campaign_dates.append({"year": year, **CAMPAIGN_DATES[year]})
        return Response(self.get_serializer(campaign_dates, many=True).data)


@extend_schema_view(
    get=extend_schema(
        summary="Détails des dates de campagne pour une année donnée.",
        tags=["teledeclaration"],
    ),
)
class TeledeclarationCampaignDatesRetrieveView(RetrieveAPIView):
    include_in_documentation = True
    serializer_class = CampaignDatesFullSerializer

    def get(self, request, year, format=None):
        if not CAMPAIGN_DATES.get(year):
            return Response(status=status.HTTP_404_NOT_FOUND)
        campaign_dates_for_year = {
            "year": year,
            **CAMPAIGN_DATES[year],
            "in_teledeclaration": is_in_teledeclaration(),
            "in_correction": is_in_correction(),
        }
        return Response(self.get_serializer(campaign_dates_for_year).data)
