from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from macantine.utils import (
    CAMPAIGN_DATES,
    is_in_correction,
    is_in_teledeclaration,
)


@extend_schema_view(
    get=extend_schema(summary="Lister les dates des campagnes.", tags=["teledeclaration"]),
)
class TeledeclarationCampaignDatesListView(APIView):
    include_in_documentation = True

    def get(self, request, format=None):
        campaign_dates = []
        for year in CAMPAIGN_DATES.keys():
            campaign_dates.append({"year": year, **CAMPAIGN_DATES[year]})
        return Response(campaign_dates)


@extend_schema_view(
    get=extend_schema(summary="Détails des dates de campagne pour une année donnée.", tags=["teledeclaration"]),
)
class TeledeclarationCampaignDatesRetrieveView(APIView):
    include_in_documentation = True

    def get(self, request, year, format=None):
        if not CAMPAIGN_DATES.get(year):
            return Response(status=status.HTTP_404_NOT_FOUND)
        campaign_dates_for_year = {
            "year": year,
            **CAMPAIGN_DATES[year],
            "in_teledeclaration": is_in_teledeclaration(),
            "in_correction": is_in_correction(),
        }
        return Response(campaign_dates_for_year)
