from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.utils import timezone

from api.permissions import IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam
from api.serializers import SatelliteCanteenSerializer, FullCanteenSerializer
from data.models import Canteen
from macantine.utils import is_in_teledeclaration_or_correction


@extend_schema_view(
    get=extend_schema(summary="Lister les restaurants satellites d'un groupe."),
)
class CanteenGroupeSatellitesListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    model = Canteen
    serializer_class = SatelliteCanteenSerializer

    def get_queryset(self):
        year = timezone.now().year - 1
        canteen_pk = self.kwargs["canteen_pk"]
        return Canteen.objects.get(pk=canteen_pk).satellites.annotate_with_action_for_year(year).order_by("name")


@extend_schema_view(
    post=extend_schema(summary="Ajouter un restaurant satellite à un groupe."),
)
class CanteenGroupeSatelliteLinkView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    # required_scopes = ["canteen"]
    serializer_class = FullCanteenSerializer

    def post(self, request, canteen_pk, satellite_pk):
        canteen_groupe = Canteen.objects.get(pk=canteen_pk)

        try:
            canteen_satellite = Canteen.objects.get(pk=satellite_pk)
        except Canteen.DoesNotExist:
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        if not canteen_satellite.is_satellite:
            return JsonResponse(
                {"error": "Only satellites can be linked to a groupe."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if canteen_satellite.groupe_id:
            return JsonResponse(
                {"error": "This satellite is already linked to a groupe."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if is_in_teledeclaration_or_correction():
            if canteen_groupe.has_diagnostic_teledeclared_for_year(timezone.now().year - 1):
                return JsonResponse(
                    {
                        "error": "Vous ne pouvez pas ajouter de restaurant satellite à votre groupe, car il possède un bilan télédéclaré (campagne de télédéclaration en cours). Veuillez annuler la télédéclaration pour pouvoir ajouter le restaurant satellite.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        canteen_satellite.groupe = canteen_groupe
        canteen_satellite.save(skip_validations=True)
        return Response(FullCanteenSerializer(canteen_groupe).data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(summary="Enlever un restaurant satellite d'un groupe."),
)
class CanteenGroupeSatelliteUnlinkView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    # required_scopes = ["canteen"]
    serializer_class = FullCanteenSerializer

    def post(self, request, canteen_pk, satellite_pk):
        canteen_groupe = Canteen.objects.get(pk=canteen_pk)

        try:
            canteen_satellite = Canteen.objects.get(pk=satellite_pk)
        except Canteen.DoesNotExist:
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        if canteen_satellite.groupe_id != canteen_groupe.id:
            return JsonResponse(
                {"error": "This satellite is not linked to this groupe."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if is_in_teledeclaration_or_correction():
            if canteen_groupe.has_diagnostic_teledeclared_for_year(timezone.now().year - 1):
                return JsonResponse(
                    {
                        "error": "Vous ne pouvez pas retirer de restaurant satellite à votre groupe, car il possède un bilan télédéclaré (campagne de télédéclaration en cours). Veuillez annuler la télédéclaration pour pouvoir retirer le restaurant satellite.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        canteen_satellite.groupe = None
        canteen_satellite.save(skip_validations=True)
        return Response(FullCanteenSerializer(canteen_groupe).data, status=status.HTTP_200_OK)
