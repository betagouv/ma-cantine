import logging
from common.utils import send_mail
from data.models.diagnostic import Diagnostic
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from api.serializers import PublicDiagnosticSerializer
from data.models import Canteen
from api.permissions import (
    IsCanteenManager,
    CanEditDiagnostic,
    IsAuthenticated,
    IsAuthenticatedOrTokenHasResourceScope,
)
from api.exceptions import DuplicateException

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        summary="Création d'un nouveau diagnostic.",
        description="Un diagnostic doit être rattaché a une cantine. Certains vérifications sur les données peuvent être effectués.",
    )
)
class DiagnosticCreateView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]
    model = Diagnostic
    serializer_class = PublicDiagnosticSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs.setdefault("action", "create")
        return PublicDiagnosticSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        try:
            canteen_id = self.request.parser_context.get("kwargs").get("canteen_pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(self.request, self, canteen):
                raise PermissionDenied()
            serializer.is_valid(raise_exception=True)
            serializer.save(canteen=canteen)
        except ObjectDoesNotExist as e:
            logger.warning(f"Attempt to create a diagnostic from an unexistent canteen ID : {canteen_id}: \n{e}")
            raise NotFound()
        except IntegrityError as e:
            logger.warning(f"Attempt to create an existing diagnostic for canteen ID {canteen_id}:\n{e}")
            raise DuplicateException()


@extend_schema_view(
    patch=extend_schema(
        summary="Modification d'un diagnostic existant.",
        description="À noter qu'un diagnostic ne peut pas être modifié une fois qu'il a été télédéclaré. Pour ce faire, il faut d'abord annuler la télédéclaration.",
    ),
    put=extend_schema(
        exclude=True,
    ),
)
class DiagnosticUpdateView(UpdateAPIView):
    permission_classes = [
        IsAuthenticatedOrTokenHasResourceScope,
        CanEditDiagnostic,
    ]
    required_scopes = ["canteen"]
    model = Diagnostic
    serializer_class = PublicDiagnosticSerializer
    queryset = Diagnostic.objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse({"error": "Only PATCH request supported in this resource"}, status=405)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


class EmailDiagnosticImportFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            file = request.data["file"]
            self._verify_file_size(file)
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
                attachments=[(file.name, file.read(), file.content_type)],
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

    @staticmethod
    def _verify_file_size(file):
        if file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")
