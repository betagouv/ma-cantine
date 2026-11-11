from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam
from api.serializers import (
    DiagnosticGroupeCouvertsAnnuelsUpdateSerializer,
    DiagnosticGroupeSatelliteCouvertsAnnuelsSerializer,
)
from api.views.utils import update_change_reason_with_auth
from data.models import Canteen
from data.models.diagnostic import Diagnostic


@extend_schema_view(
    get=extend_schema(
        summary="Lister les nombres de repas par an des restaurants satellites d'un groupe.",
        description="Seulement pour les bilans des groupes.",
        tags=["Bilans"],
        responses=DiagnosticGroupeSatelliteCouvertsAnnuelsSerializer(many=True),
    ),
    patch=extend_schema(
        summary="Modifier le nombre de repas par an d'un restaurant satellite d'un groupe.",
        description="Seulement pour les bilans des groupes non télédéclarés.",
        tags=["Bilans"],
        request=DiagnosticGroupeCouvertsAnnuelsUpdateSerializer,
        responses=DiagnosticGroupeSatelliteCouvertsAnnuelsSerializer(many=True),
    ),
)
class DiagnosticGroupeCouvertsAnnuelsView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def _get_diagnostic(self, canteen):
        return get_object_or_404(Diagnostic, pk=self.kwargs["pk"], canteen=canteen)

    def _get_response(self, canteen, diagnostic):
        serializer = DiagnosticGroupeSatelliteCouvertsAnnuelsSerializer(
            canteen.satellites.order_by("name"),
            many=True,
            context={"satellites_nombre_repas_an": diagnostic.satellites_nombre_repas_an},
        )
        return Response(serializer.data)

    def get(self, request, canteen_pk, pk):
        canteen = self._get_canteen()
        diagnostic = self._get_diagnostic(canteen)
        if not canteen.is_groupe:
            return JsonResponse({"error": "Seuls les groupes ont des satellites."}, status=status.HTTP_400_BAD_REQUEST)
        return self._get_response(canteen, diagnostic)

    def patch(self, request, canteen_pk, pk):
        canteen = self._get_canteen()
        diagnostic = self._get_diagnostic(canteen)
        if not canteen.is_groupe:
            return JsonResponse({"error": "Seuls les groupes ont des satellites."}, status=status.HTTP_400_BAD_REQUEST)
        if diagnostic.is_teledeclared:
            return JsonResponse(
                {"error": "Le bilan est déjà télédéclaré : il faut d'abord annuler la télédéclaration."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DiagnosticGroupeCouvertsAnnuelsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        satellite_id = serializer.validated_data["id"]
        nombre_repas_an = serializer.validated_data["nombre_repas_an"]

        if not canteen.satellites.filter(id=satellite_id).exists():
            return JsonResponse(
                {"error": "Cette cantine n'est pas un satellite de ce groupe."}, status=status.HTTP_400_BAD_REQUEST
            )

        satellites_nombre_repas_an = diagnostic.satellites_nombre_repas_an or {}
        satellites_nombre_repas_an[str(satellite_id)] = nombre_repas_an
        diagnostic.satellites_nombre_repas_an = satellites_nombre_repas_an
        diagnostic.save()  # also computes satellites_nombre_repas_an_total (see populate_computed_fields)
        update_change_reason_with_auth(self, diagnostic)

        return self._get_response(canteen, diagnostic)
