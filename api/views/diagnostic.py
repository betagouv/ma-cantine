import csv
import time
import re
import logging
from data.models.diagnostic import Diagnostic
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, BadRequest, ValidationError
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from api.serializers import DiagnosticSerializer, FullCanteenSerializer
from data.models import Canteen, Sector
from api.permissions import IsCanteenManager, CanEditDiagnostic
from .utils import camelize

logger = logging.getLogger(__name__)


class DiagnosticCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Diagnostic
    serializer_class = DiagnosticSerializer

    def perform_create(self, serializer):
        try:
            canteen_id = self.request.parser_context.get("kwargs").get("canteen_pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(
                self.request, self, canteen
            ):
                raise PermissionDenied()
            serializer.save(canteen=canteen)
        except ObjectDoesNotExist:
            logger.error(
                f"Attempt to create a diagnostic from an unexistent canteen ID : {canteen_id}"
            )
            raise NotFound()
        except IntegrityError:
            logger.error(
                f"Attempt to create an existing diagnostic for canteen ID {canteen_id}"
            )
            raise BadRequest()


class DiagnosticUpdateView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, CanEditDiagnostic]
    model = Diagnostic
    serializer_class = DiagnosticSerializer
    queryset = Diagnostic.objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Only PATCH request supported in this resource"}, status=405
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# flake8: noqa: C901
class ImportDiagnosticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")
    validation_error_regex = re.compile(r"La valeur «\xa0(.+)\xa0»")
    # TODO? Django adds quotes for choice validation errors so the regex would be:
    # choice_error_regex = re.compile(
    #     r"La valeur «\xa0'(.+)'\xa0» n’est pas un choix valide."
    # )

    def post(self, request):
        start = time.time()
        logger.info("Diagnostic bulk import started")
        diagnostics_created = 0
        canteens = {}
        errors = []
        try:
            filestring = request.data["file"].read().decode("utf-8")
            csvreader = csv.reader(filestring.splitlines())
            with transaction.atomic():
                for row_number, row in enumerate(csvreader, start=1):
                    try:
                        siret = ImportDiagnosticsView._normalise_siret(row[0])
                        canteen = self._create_canteen_with_diagnostic(row, siret)
                        diagnostics_created += 1
                        canteens[canteen.siret] = canteen
                    except Exception as e:
                        (message, code) = self._parse_error(e)
                        errors.append(
                            ImportDiagnosticsView._get_error(
                                e, message, code, row_number
                            )
                        )

                if errors:
                    raise IntegrityError()

            serialized_canteens = [
                camelize(FullCanteenSerializer(canteen).data)
                for canteen in canteens.values()
            ]
            return ImportDiagnosticsView._get_success_response(
                serialized_canteens, diagnostics_created, errors, start
            )

        except IntegrityError:
            logger.error("L'import du fichier CSV a échoué")
            return ImportDiagnosticsView._get_success_response([], 0, errors, start)

        except Exception as e:
            logger.exception(e)
            message = "Échec lors de la lecture du fichier"
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportDiagnosticsView._get_success_response([], 0, errors, start)

    @transaction.atomic
    def _create_canteen_with_diagnostic(self, row, siret):
        (canteen, created) = Canteen.objects.get_or_create(
            siret=siret,
            defaults={
                "siret": siret,
                "name": row[1],  # TODO: should this be optional or not?
                "city_insee_code": row[2],
                "postal_code": row[3],
                "central_producer_siret": row[4],
                "daily_meal_count": row[5],
                "production_type": row[7],
                "management_type": row[8],
            },
        )

        if not created and self.request.user not in canteen.managers.all():
            raise PermissionDenied()

        if created:
            canteen.managers.add(self.request.user)
            if row[6]:
                canteen.sectors.add(
                    *[Sector.objects.get(name=sector) for sector in row[6].split("+")]
                )
            canteen.full_clean()  # validate choice fields
            canteen.save()

        diagnostic = Diagnostic(
            canteen_id=canteen.id,
            year=row[9],
            value_total_ht=row[10],
            value_bio_ht=row[11],
            value_sustainable_ht=row[12],
            value_fair_trade_ht=row[13],
        )
        diagnostic.full_clean()  # trigger field validators like year min/max
        diagnostic.save()
        return canteen

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        logger.error(f"Error on row {row_number}")
        logger.exception(e)
        return {"row": row_number, "status": error_status, "message": message}

    @staticmethod
    def _get_success_response(canteens, count, errors, start_time):
        return JsonResponse(
            {
                "canteens": canteens,
                "count": count,
                "errors": errors,
                "seconds": time.time() - start_time,
            },
            status=status.HTTP_200_OK,
        )

    def _parse_error(self, e):
        message = "Une erreur s'est produite en créant un diagnostic pour cette ligne"
        code = 400
        if isinstance(e, PermissionDenied):
            message = f"Vous n'êtes pas un gestionnaire de cette cantine."
            code = 401
        elif isinstance(e, Sector.DoesNotExist):
            message = "Le secteur spécifié ne fait pas partie des options acceptées"
        elif isinstance(e, ValidationError):
            try:
                field_name = list(e.message_dict.keys())[0]
                if (
                    hasattr(e, "messages")
                    and e.messages[0]
                    == "Un objet Diagnostic avec ces champs Canteen et An existe déjà."
                ):
                    message = (
                        "Un diagnostic pour cette année et cette cantine existe déjà"
                    )
                elif field_name:
                    verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(
                        field_name
                    )
                    match = self.validation_error_regex.search(e.messages[0])
                    if match:
                        value_given = match.group(1) if match else ""
                        message = f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
                    elif field_name == "year":
                        message = (
                            f"Pour le champ '{verbose_field_name}', {e.messages[0]}"
                        )
            except:
                if hasattr(e, "params"):
                    message = f"La valeur '{e.params['value']}' n'est pas valide."
        elif isinstance(e, ValueError):
            match = self.value_error_regex.search(str(e))
            field_name = match.group(1) if match else ""
            value_given = match.group(2) if match else ""
            if field_name:
                verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(
                    field_name
                )
                message = f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
        return (message, code)

    @staticmethod
    def _normalise_siret(siret):
        # TODO: find official siret format
        return siret.replace(" ", "")

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            verbose_field_name = Canteen._meta.get_field(field_name).verbose_name
        except:
            try:
                verbose_field_name = Diagnostic._meta.get_field(field_name).verbose_name
            except:
                pass
        return verbose_field_name
