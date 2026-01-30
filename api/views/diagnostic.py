import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.db.models import Exists, OuterRef
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from api.exceptions import DuplicateException
from api.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManager,
    IsLinkedCanteenManager,
)
from api.serializers import (
    DiagnosticAndCanteenSerializer,
    ManagerDiagnosticSerializer,
)
from api.views.utils import update_change_reason_with_auth
from common.utils import file_import, send_mail
from data.models import Canteen, Teledeclaration
from data.models.creation_source import CreationSource
from data.models.diagnostic import Diagnostic
from macantine.utils import is_in_correction

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        summary="Créer un nouveau diagnostic.",
        description="Un diagnostic doit être rattaché a une cantine.",
    )
)
class DiagnosticCreateView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]
    model = Diagnostic
    serializer_class = ManagerDiagnosticSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs.setdefault("action", "create")
        return ManagerDiagnosticSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        try:
            canteen_id = self.request.parser_context.get("kwargs").get("canteen_pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(self.request, self, canteen):
                raise PermissionDenied()
            serializer.is_valid(raise_exception=True)
            creation_source = serializer.validated_data.get("creation_source") or CreationSource.API
            diagnostic = serializer.save(canteen=canteen, creation_source=creation_source)
            update_change_reason_with_auth(self, diagnostic)
        except ObjectDoesNotExist as e:
            logger.warning(f"Attempt to create a diagnostic from an unexistent canteen ID : {canteen_id}: \n{e}")
            raise NotFound()
        except IntegrityError as e:
            logger.warning(f"Attempt to create an existing diagnostic for canteen ID {canteen_id}:\n{e}")
            raise DuplicateException()


@extend_schema_view(
    patch=extend_schema(
        summary="Modifier un diagnostic existant.",
        description="À noter qu'un diagnostic ne peut pas être modifié une fois qu'il a été télédéclaré. Pour ce faire, il faut d'abord annuler la télédéclaration.",
    ),
    put=extend_schema(
        exclude=True,
    ),
)
class DiagnosticUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsLinkedCanteenManager]
    required_scopes = ["canteen"]
    http_method_names = ["patch"]  # disable "put"
    queryset = Diagnostic.objects.all()
    serializer_class = ManagerDiagnosticSerializer

    def perform_update(self, serializer):
        if self.get_object().is_teledeclared:
            raise PermissionDenied("Ce n'est pas possible de modifier un diagnostic télédéclaré.")
        serializer.is_valid(raise_exception=True)
        diagnostic = serializer.save()
        update_change_reason_with_auth(self, diagnostic)


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


class DiagnosticsToTeledeclarePagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class DiagnosticsToTeledeclareListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Diagnostic
    serializer_class = DiagnosticAndCanteenSerializer
    pagination_class = DiagnosticsToTeledeclarePagination
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
