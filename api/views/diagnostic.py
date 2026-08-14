import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Exists, OuterRef
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import DuplicateException
from api.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManagerUrlParam,
)
from api.serializers import (
    DiagnosticAndCanteenSerializer,
    ManagerDiagnosticSerializer,
    DiagnosticCheckSerializer,
    DiagnosticRecapSerializer,
)
from api.views.utils import get_oauth_application, update_change_reason_with_auth
from common.utils import file_import, send_mail
from data.models import Canteen, Teledeclaration
from data.models.creation_source import CreationSource
from data.models.diagnostic import Diagnostic
from macantine.utils import CAMPAIGN_DATES_VALID, is_in_correction

logger = logging.getLogger(__name__)


class LongPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


@extend_schema_view(
    get=extend_schema(
        summary="Lister les bilans d'une cantine.",
        description="Retourne la liste des bilans d'une cantine.",
        tags=["Bilans"],
    ),
    post=extend_schema(
        summary="Créer un nouveau bilan.",
        description="Un bilan doit être rattaché à une cantine.",
        tags=["Bilans"],
    ),
)
class DiagnosticListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    model = Diagnostic
    serializer_class = ManagerDiagnosticSerializer
    pagination_class = LongPagination

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return canteen.diagnostics.all().order_by("year")

    def perform_create(self, serializer):
        try:
            canteen = self._get_canteen()
            serializer.is_valid(raise_exception=True)
            creation_user = self.request.user
            creation_source = serializer.validated_data.get("creation_source") or CreationSource.API
            creation_source_api_oauth2_application = get_oauth_application(self.request)
            diagnostic = serializer.save(
                canteen=canteen,
                creation_user=creation_user,
                creation_source=creation_source,
                creation_source_api_oauth2_application=creation_source_api_oauth2_application,
            )
            update_change_reason_with_auth(self, diagnostic)
        except IntegrityError as e:
            logger.warning(
                f"Attempt to create an existing diagnostic for canteen ID {self.kwargs['canteen_pk']}:\n{e}"
            )
            raise DuplicateException()


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer un bilan existant.",
        description="",
        tags=["Bilans"],
    ),
    patch=extend_schema(
        summary="Modifier un bilan existant.",
        description="À noter qu'un bilan ne peut pas être modifié une fois qu'il a été télédéclaré. Pour ce faire, il faut d'abord annuler la télédéclaration.",
        tags=["Bilans"],
    ),
)
class DiagnosticRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    http_method_names = ["get", "patch"]  # disable "put"
    model = Diagnostic
    serializer_class = ManagerDiagnosticSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_object(self):
        canteen = self._get_canteen()
        return get_object_or_404(Diagnostic, pk=self.kwargs["pk"], canteen=canteen)

    def perform_update(self, serializer):
        if self.get_object().is_teledeclared:
            # if the user wants to cancel, see DiagnosticTeledeclarationCancelView
            raise PermissionDenied("Ce n'est pas possible de modifier un bilan télédéclaré.")
        serializer.is_valid(raise_exception=True)
        diagnostic = serializer.save()
        update_change_reason_with_auth(self, diagnostic)


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer le récapitulatif par année des bilans d'une cantine.",
        description="",
        tags=["Bilans"],
        responses=DiagnosticRecapSerializer(many=True),
    ),
)
class DiagnosticListRecapView(APIView):
    permission_classes = [IsAuthenticated, IsCanteenManagerUrlParam]

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get(self, request, canteen_pk):
        canteen = self._get_canteen()
        canteen_diagnostics = Diagnostic.all_objects.filter(canteen=canteen)
        result = []
        for year in CAMPAIGN_DATES_VALID.keys():
            # skip years where the canteen was not yet created
            if canteen.creation_date > CAMPAIGN_DATES_VALID[year]["teledeclaration_end_date"]:
                continue
            # is_teledeclared: if at least 1 of the canteen's diagnostics is SUBMITTED
            is_teledeclared = any(d.year == year and d.is_teledeclared for d in canteen_diagnostics)
            # declaration_donnees: copy the canteeen's field value
            declaration_donnees = getattr(canteen, f"declaration_donnees_{year}", None)
            # canteen_diagnostic: the canteen's own diagnostic (if it exists)
            canteen_diagnostic = next(
                (d for d in canteen_diagnostics if d.year == year and not d.generated_from_groupe_diagnostic), None
            )
            canteen_diagnostic_id = canteen_diagnostic.id if canteen_diagnostic else None
            # generated_from_groupe_diagnostic: the canteen's generated diagnostic (from its groupe) (if it exists)
            generated_from_groupe_diagnostic = next(
                (d for d in canteen_diagnostics if d.year == year and d.generated_from_groupe_diagnostic), None
            )
            generated_from_groupe_diagnostic_id = (
                generated_from_groupe_diagnostic.id if generated_from_groupe_diagnostic else None
            )
            generated_from_groupe_diagnostic_mode = (
                generated_from_groupe_diagnostic.central_kitchen_diagnostic_mode
                if generated_from_groupe_diagnostic
                else None
            )
            result.append(
                {
                    "year": year,
                    "is_teledeclared": is_teledeclared,
                    "declaration_donnees": declaration_donnees,
                    "canteen_diagnostic_id": canteen_diagnostic_id,
                    "generated_from_groupe_diagnostic_id": generated_from_groupe_diagnostic_id,
                    "generated_from_groupe_diagnostic_mode": generated_from_groupe_diagnostic_mode,
                }
            )
        return Response(DiagnosticRecapSerializer(result, many=True).data)


@extend_schema_view(
    get=extend_schema(
        summary="Vérifier les erreurs de validation pour un bilan.",
        description="Retourne toutes les erreurs de validation potentielles pour un bilan (champs manquants, valeurs invalides, etc.).",
        tags=["Bilans"],
        responses=DiagnosticCheckSerializer,
    )
)
class DiagnosticCheckView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get(self, request, canteen_pk, pk):
        canteen = self._get_canteen()
        diagnostic = get_object_or_404(Diagnostic, pk=self.kwargs["pk"], canteen=canteen)

        errors = {}
        try:
            diagnostic.full_clean()
        except ValidationError as e:
            errors = e.message_dict

        response = {"is_filled": diagnostic.is_filled, "errors": errors}
        return Response(DiagnosticCheckSerializer(response).data)


class EmailDiagnosticImportFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            self.file = request.data["file"]
            file_import.validate_file_size(self.file)
            file_import.validate_file_format(self.file)
            email = request.data.get("email", request.user.email).strip()
            context = {
                "from": email,
                "name": request.data.get("name", request.user.get_full_name()),
                "message": request.data.get("message", ""),
            }
            send_mail(
                subject="Fichier pour l'import de diagnostics massif",
                to=[settings.CONTACT_EMAIL],
                reply_to=[email],
                template="unusual_diagnostic_import_file",
                attachments=[(self.file.name, self.file.read(), self.file.content_type)],
                context=context,
            )
        except ValidationError as e:
            logger.warning(
                f"{request.user.id} tried to upload a file that is too large (over {settings.CSV_IMPORT_MAX_SIZE}):\n{e}"
            )
            return HttpResponseBadRequest()
        except Exception as e:
            logger.exception(
                f"User {request.user.id} encountered an error when trying to email a diagnostic import file:\n{e}"
            )
            return HttpResponseServerError()

        return HttpResponse()


class DiagnosticsToTeledeclareListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Diagnostic
    serializer_class = DiagnosticAndCanteenSerializer
    pagination_class = LongPagination
    ordering = "modification_date"

    def get_queryset(self):
        year = self.request.parser_context.get("kwargs").get("year")
        canteens = DiagnosticsToTeledeclareListView._get_canteens_filled(self.request.user.canteens.all())
        has_teledeclaration_submitted = (
            Teledeclaration.objects.filter(diagnostic=OuterRef("pk")).in_year(year).submitted()
        )
        has_teledeclaration_cancelled = (
            Teledeclaration.objects.filter(diagnostic=OuterRef("pk")).in_year(year).cancelled()
        )
        diagnostics_to_teledeclare = (
            Diagnostic.objects.filled()
            .filter(year=year, canteen__in=canteens, diagnostic_type__isnull=False)
            .annotate(has_teledeclaration_submitted=Exists(has_teledeclaration_submitted))
            .annotate(has_teledeclaration_cancelled=Exists(has_teledeclaration_cancelled))
        )

        diagnostics_to_teledeclare = diagnostics_to_teledeclare.exclude(has_teledeclaration_submitted=True)

        if is_in_correction():
            diagnostics_to_teledeclare = diagnostics_to_teledeclare.filter(has_teledeclaration_cancelled=True)

        return diagnostics_to_teledeclare

    @staticmethod
    def _get_canteens_filled(canteens):
        # We use this method instead of the SQL based one in the views/canteen.py file because we
        # don't need all the actions. By doing this on Python we can return early without running
        # all SQL requests when not needed. We are also not interested exactly in the kind of
        # completeness, just wether or not the canteen can teledeclare.
        # Possible to have this method in the model
        canteens_filled = [canteen for canteen in canteens if canteen.is_filled]
        return canteens_filled
