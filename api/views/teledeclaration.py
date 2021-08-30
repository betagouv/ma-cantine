import logging
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from data.models import Diagnostic, Teledeclaration
from api.serializers import FullDiagnosticSerializer
from .utils import camelize

logger = logging.getLogger(__name__)


class TeledeclarationCreateView(APIView):
    """
    This view allows creating a teledeclaration from an
    existing diagnostic.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            diagnostic_id = data.get("diagnostic_id")
            if not diagnostic_id:
                raise ValidationError("diagnosticId manquant")
            diagnostic = Diagnostic.objects.get(pk=diagnostic_id)
            TeledeclarationCreateView.validateDiagnostic(diagnostic)

            if request.user not in diagnostic.canteen.managers.all():
                raise PermissionDenied()

            Teledeclaration.createFromDiagnostic(diagnostic, request.user)

            data = FullDiagnosticSerializer(diagnostic).data
            return JsonResponse(camelize(data), status=status.HTTP_201_CREATED)

        except Diagnostic.DoesNotExist:
            raise ValidationError("Le diagnostic specifié n'existe pas")

        except DjangoValidationError as e:
            message = "Il existe déjà une télédéclaration en cours pour cette année"
            raise ValidationError(message) from e

    @staticmethod
    def validateDiagnostic(diagnostic):
        total_ht = diagnostic.value_total_ht
        breakdown = [
            diagnostic.value_fair_trade_ht,
            diagnostic.value_sustainable_ht,
            diagnostic.value_bio_ht,
        ]
        if not total_ht or None in breakdown:
            raise ValidationError("Données d'approvisionnement manquantes")


class TeledeclarationCancelView(APIView):
    """
    This view cancels a submitted teledeclaration
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            teledeclaration_id = data.get("teledeclaration_id")
            if not teledeclaration_id:
                raise ValidationError("teledeclarationId manquant")

            teledeclaration = Teledeclaration.objects.get(pk=teledeclaration_id)

            if request.user not in teledeclaration.canteen.managers.all():
                raise PermissionDenied()

            teledeclaration.status = Teledeclaration.TeledeclarationStatus.CANCELLED
            teledeclaration.save()

            data = FullDiagnosticSerializer(teledeclaration.diagnostic).data
            return JsonResponse(camelize(data), status=status.HTTP_200_OK)

        except Teledeclaration.DoesNotExist:
            raise ValidationError("La télédéclaration specifiée n'existe pas")
