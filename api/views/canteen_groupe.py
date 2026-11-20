from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone

from api.permissions import (
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManagerUrlParam,
    IsSatelliteManagerUrlParam,
)
from api.serializers import SatelliteCanteenSerializer, FullCanteenSerializer
from data.models import Canteen
from data.models.diagnostic_teledeclaration_dates import (
    get_current_campaign_year,
    get_year_correction_end_date_or_campaign_end_date_or_today_date,
)


@extend_schema_view(
    get=extend_schema(summary="Lister les restaurants satellites d'un groupe.", tags=["Cantines"]),
)
class CanteenGroupeSatellitesListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    model = Canteen
    serializer_class = SatelliteCanteenSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        year = get_current_campaign_year()
        canteen_groupe = self._get_canteen()
        user = self.request.user
        return (
            canteen_groupe.satellites.annotate_with_is_managed_by_user(user)
            .annotate_with_action_for_year(year)
            .order_by("name")
        )


@extend_schema_view(
    post=extend_schema(summary="Ajouter un restaurant satellite à un groupe.", tags=["Cantines"]),
)
class CanteenGroupeSatelliteLinkView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    serializer_class = FullCanteenSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def post(self, request, canteen_pk, satellite_pk):
        canteen_groupe = self._get_canteen()

        try:
            canteen_satellite = Canteen.objects.get(pk=satellite_pk)
        except Canteen.DoesNotExist:
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        if not canteen_satellite.can_be_in_groupe:
            return JsonResponse(
                {"error": "Only satellites and sites can be linked to a groupe."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if canteen_satellite.groupe_id:
            return JsonResponse(
                {"error": "This satellite is already linked to a groupe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        canteen_satellite.groupe = canteen_groupe
        try:
            canteen_satellite.save(skip_validations=True)
        except ValidationError as e:
            # the groupe has a teledeclared diagnostic during the campaign (see validate_canteen_groupe_change)
            return JsonResponse({"error": " ".join(e.message_dict["groupe"])}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FullCanteenSerializer(canteen_groupe).data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(summary="Enlever un restaurant satellite d'un groupe.", tags=["Cantines"]),
)
class CanteenGroupeSatelliteUnlinkView(APIView):
    # the groupe manager, or the satellite manager (to unlink their own satellite)
    permission_classes = [
        IsAuthenticatedOrTokenHasResourceScope,
        IsCanteenManagerUrlParam | IsSatelliteManagerUrlParam,
    ]
    required_scopes = ["canteen"]
    serializer_class = FullCanteenSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def post(self, request, canteen_pk, satellite_pk):
        canteen_groupe = self._get_canteen()

        try:
            canteen_satellite = Canteen.objects.get(pk=satellite_pk)
        except Canteen.DoesNotExist:
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        if canteen_satellite.groupe_id != canteen_groupe.id:
            return JsonResponse(
                {"error": "This satellite is not linked to this groupe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        canteen_satellite.groupe = None
        try:
            canteen_satellite.save(skip_validations=True)
        except ValidationError as e:
            # the groupe has a teledeclared diagnostic during the campaign (see validate_canteen_groupe_change)
            if canteen_groupe.managers.filter(id=request.user.id).exists():
                error = " ".join(e.message_dict["groupe"])
            else:
                # the user is the satellite manager (see permission_classes)
                correction_end_date = timezone.localtime(
                    get_year_correction_end_date_or_campaign_end_date_or_today_date(get_current_campaign_year())
                ).strftime("%d/%m/%Y")
                error = f"Vous ne pouvez pas quitter le groupe car sa télédéclaration a été validée et les données de votre cantine ont été prises en compte. Vous pouvez demander à votre groupe d'annuler sa télédéclaration, ou alors vous pourrez renouveler votre demande à la fin de la campagne à partir du {correction_end_date}"
            return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FullCanteenSerializer(canteen_groupe).data, status=status.HTTP_200_OK)
