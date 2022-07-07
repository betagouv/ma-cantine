import csv
import time
import re
import logging
from common.utils import send_mail
from decimal import Decimal
from data.models.diagnostic import Diagnostic
from django.db import IntegrityError, transaction
from django.db.models.functions import Lower
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist, BadRequest, ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from api.serializers import PublicDiagnosticSerializer, FullCanteenSerializer
from data.models import Canteen, Sector
from api.permissions import IsCanteenManager, CanEditDiagnostic, IsAuthenticated
from api.exceptions import DuplicateException
from .utils import camelize, normalise_siret
from .canteen import AddManagerView
import requests

logger = logging.getLogger(__name__)


class DiagnosticCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
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
        except ObjectDoesNotExist:
            logger.error(f"Attempt to create a diagnostic from an unexistent canteen ID : {canteen_id}")
            raise NotFound()
        except IntegrityError:
            logger.error(f"Attempt to create an existing diagnostic for canteen ID {canteen_id}")
            raise DuplicateException()


class DiagnosticUpdateView(UpdateAPIView):
    permission_classes = [
        IsAuthenticated,
        CanEditDiagnostic,
    ]
    model = Diagnostic
    serializer_class = PublicDiagnosticSerializer
    queryset = Diagnostic.objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse({"error": "Only PATCH request supported in this resource"}, status=405)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


# flake8: noqa: C901
class ImportDiagnosticsView(APIView):
    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")
    annotated_sectors = Sector.objects.annotate(name_lower=Lower("name"))

    def __init__(self, **kwargs):
        self.diagnostics_created = 0
        super().__init__(**kwargs)

    def post(self, request):
        start = time.time()
        logger.info("Diagnostic bulk import started")
        try:
            with transaction.atomic():
                file = request.data["file"]
                ImportDiagnosticsView._verify_file_size(file)
                (canteens, errors) = self._treat_csv_file(file)

                if errors:
                    raise IntegrityError()

            serialized_canteens = [camelize(FullCanteenSerializer(canteen).data) for canteen in canteens.values()]
            return ImportDiagnosticsView._get_success_response(
                serialized_canteens, self.diagnostics_created, errors, start
            )

        except IntegrityError as e:
            logger.exception(e)
            logger.error("L'import du fichier CSV a échoué")
            return ImportDiagnosticsView._get_success_response([], 0, errors, start)

        except ValidationError as e:
            message = e.message
            logger.error(message)
            message = message
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportDiagnosticsView._get_success_response([], 0, errors, start)

        except Exception as e:
            logger.exception(e)
            message = "Échec lors de la lecture du fichier"
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportDiagnosticsView._get_success_response([], 0, errors, start)

    @staticmethod
    def _verify_file_size(file):
        if file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _treat_csv_file(self, file):
        canteens = {}
        errors = []
        locations_csv_str = "siret,citycode,postcode\n"
        has_locations_to_find = False

        filestring = file.read().decode("utf-8-sig")
        filelines = filestring.splitlines()
        dialect = csv.Sniffer().sniff(filelines[0])

        csvreader = csv.reader(filelines, dialect=dialect)
        for row_number, row in enumerate(csvreader, start=1):
            if row_number == 1 and row[0].lower() == "siret":
                continue
            try:
                if row[0] == "":
                    raise ValidationError({"siret": "Le siret de la cantine ne peut pas être vide"})
                siret = normalise_siret(row[0])
                canteen, should_update_geolocation = self._update_or_create_canteen_with_diagnostic(row, siret)
                canteens[canteen.siret] = canteen
                if should_update_geolocation:
                    has_locations_to_find = True
                    if canteen.city_insee_code:
                        locations_csv_str += f"{canteen.siret},{canteen.city_insee_code},\n"
                    else:
                        locations_csv_str += f"{canteen.siret},,{canteen.postal_code}\n"

            except Exception as e:
                for error in self._parse_errors(e, row):
                    errors.append(ImportDiagnosticsView._get_error(e, error["message"], error["code"], row_number))
        if has_locations_to_find:
            self._update_location_data(canteens, locations_csv_str)
        return (canteens, errors)

    @transaction.atomic
    def _update_or_create_canteen_with_diagnostic(self, row, siret):
        # first check that the number of columns is good
        #   to throw error if badly formatted early on.
        # NB: if year is given, appro data is required, else only canteen data required
        if len(row) > 18 and not self.request.user.is_staff:
            raise PermissionDenied(detail=f"Format fichier : 15-18 ou 11 colonnes attendues, {len(row)} trouvés.")
        diagnostic_year = None
        try:
            diagnostic_year = row[11]
            if not diagnostic_year and any(row[12:18]):
                raise ValidationError({"year": "L'année est obligatoire pour créer un diagnostic."})
        except IndexError:
            pass
        manager_column_idx = 10
        if diagnostic_year:
            row[14]  # check all required diagnostic fields are given
        else:
            row[manager_column_idx - 1]  # managers are optional, so could be missing too

        if not row[5]:
            raise ValidationError({"daily_meal_count": "Ce champ ne peut pas être vide."})
        elif not row[2] and not row[3]:
            raise ValidationError(
                {"postal_code": "Ce champ ne peut pas être vide si le code INSEE de la ville est vide."}
            )

        # TODO: This should take into account more number formats and be factored out to utils
        number_error_message = "Ce champ doit être un nombre décimal."

        try:
            manager_emails = []
            if len(row) > manager_column_idx + 1 and row[manager_column_idx]:
                manager_emails = ImportDiagnosticsView._get_manager_emails(row[manager_column_idx])
        except Exception as e:
            raise ValidationError({"email": "Un adresse email des gestionnaires n'est pas valide."})

        if diagnostic_year:
            try:
                if not row[12]:
                    raise Exception
                value_total_ht = Decimal(row[12].strip().replace(",", "."))
            except Exception as e:
                raise ValidationError({"value_total_ht": number_error_message})

            try:
                if not row[13]:
                    raise Exception
                value_bio_ht = Decimal(row[13].strip().replace(",", "."))
            except Exception as e:
                raise ValidationError({"value_bio_ht": number_error_message})

            try:
                if not row[14]:
                    raise Exception
                value_sustainable_ht = Decimal(row[14].strip().replace(",", "."))
            except Exception as e:
                raise ValidationError({"value_sustainable_ht": number_error_message})

            value_label_rouge = None
            try:
                if len(row) >= 16 and row[15]:
                    value_label_rouge = Decimal(row[15].strip().replace(",", "."))
            except Exception as e:
                raise ValidationError({"value_label_rouge": number_error_message})

            value_label_aoc_igp = None
            try:
                if len(row) >= 17 and row[16]:
                    value_label_aoc_igp = Decimal(row[16].strip().replace(",", "."))
            except Exception as e:
                raise ValidationError({"value_label_aoc_igp": number_error_message})

            value_label_hve = None
            try:
                if len(row) >= 18 and row[17]:
                    value_label_hve = Decimal(row[17].strip().replace(",", "."))
            except Exception as e:
                raise ValidationError({"value_label_hve": number_error_message})

        silently_added_manager_emails = []
        import_source = "Import massif"
        publication_status = Canteen.PublicationStatus.DRAFT
        if len(row) > 18:  # already checked earlier that it's a staff user
            try:
                if row[18]:
                    silently_added_manager_emails = ImportDiagnosticsView._get_manager_emails(row[18])
            except Exception as e:
                raise ValidationError({"email": "Un adresse email des gestionnaires (pas notifiés) n'est pas valide."})

            try:
                import_source = row[19].strip()
            except Exception as e:
                raise ValidationError({"import_source": "Ce champ ne peut pas être vide."})

            if len(row) > 20 and row[20]:
                publication_status = row[20].strip()

        canteen_exists = Canteen.objects.filter(siret=siret).exists()
        canteen = Canteen.objects.get(siret=siret) if canteen_exists else Canteen.objects.create(siret=siret)

        if canteen_exists and self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        should_update_geolocation = (
            ImportDiagnosticsView._should_update_geolocation(canteen, row) if canteen_exists else True
        )

        canteen.name = row[1].strip()
        canteen.city_insee_code = row[2].strip()
        canteen.postal_code = row[3].strip()
        canteen.central_producer_siret = normalise_siret(row[4])
        canteen.daily_meal_count = row[5].strip()
        canteen.production_type = row[7].strip().lower()
        canteen.management_type = row[8].strip().lower()
        canteen.economic_model = row[9].strip().lower()
        canteen.import_source = import_source
        canteen.publication_status = publication_status

        # full_clean must be before the relation-model updates bc they don't require a save().
        # If an exception is launched by full_clean, it must be here.
        canteen.full_clean()
        if row[6]:
            canteen.sectors.set(
                [
                    self.annotated_sectors.get(name_lower__unaccent=sector.strip().lower())
                    for sector in row[6].split("+")
                ]
            )

        canteen.save()

        if not self.request.user.is_staff:
            canteen.managers.add(self.request.user)
        if manager_emails:
            ImportDiagnosticsView._add_managers_to_canteen(manager_emails, canteen)
        if silently_added_manager_emails:
            ImportDiagnosticsView._add_managers_to_canteen(
                silently_added_manager_emails, canteen, send_invitation_mail=False
            )

        if diagnostic_year:
            diagnostic = Diagnostic(
                canteen_id=canteen.id,
                year=diagnostic_year,
                value_total_ht=value_total_ht,
                value_bio_ht=value_bio_ht,
                value_sustainable_ht=value_sustainable_ht,
                value_label_rouge=value_label_rouge,
                value_label_aoc_igp=value_label_aoc_igp,
                value_label_hve=value_label_hve,
            )
            diagnostic.full_clean()
            diagnostic.save()
            self.diagnostics_created += 1
        return (canteen, should_update_geolocation)

    @staticmethod
    def _should_update_geolocation(canteen, row):
        if canteen.city:
            city_code_changed = row[2] and canteen.city_insee_code != row[2].strip()
            postal_code_changed = row[3] and canteen.postal_code != row[3].strip()
            return city_code_changed or postal_code_changed
        else:
            has_geo_data = canteen.city_insee_code or canteen.postal_code
            return has_geo_data

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

    def _parse_errors(self, e, row):
        errors = []
        if isinstance(e, PermissionDenied):
            errors.append(
                {
                    "message": e.detail,
                    "code": 401,
                }
            )
        elif isinstance(e, Sector.DoesNotExist):
            errors.append(
                {
                    "message": "Le secteur spécifié ne fait pas partie des options acceptées",
                    "code": 400,
                }
            )
        elif isinstance(e, ValidationError):
            if e.message_dict:
                for field, messages in e.message_dict.items():
                    verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if user_message == "Un objet Diagnostic avec ces champs Canteen et Année existe déjà.":
                            user_message = "Un diagnostic pour cette année et cette cantine existe déjà."
                        if field != "__all__":
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        errors.append(
                            {
                                "message": user_message,
                                "code": 400,
                            }
                        )

            elif hasattr(e, "params"):
                errors.append(
                    {
                        "message": f"La valeur '{e.params['value']}' n'est pas valide.",
                        "code": 400,
                    }
                )
            else:
                errors.append(
                    {
                        "message": "Une erreur s'est produite en créant un diagnostic pour cette ligne",
                        "code": 400,
                    }
                )
        elif isinstance(e, ValueError):
            match = self.value_error_regex.search(str(e))
            field_name = match.group(1) if match else ""
            value_given = match.group(2) if match else ""
            if field_name:
                verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field_name)
                errors.append(
                    {
                        "message": f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'.",
                        "code": 400,
                    }
                )
        elif isinstance(e, IndexError):
            errors.append(
                {
                    "message": f"Données manquantes : 15 colonnes attendus, {len(row)} trouvés.",
                    "code": 400,
                }
            )
        if not errors:
            errors.append(
                {
                    "message": "Une erreur s'est produite en créant un diagnostic pour cette ligne",
                    "code": 400,
                }
            )
        return errors

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            return Canteen._meta.get_field(field_name).verbose_name
        except:
            try:
                return Diagnostic._meta.get_field(field_name).verbose_name
            except:
                pass
        return field_name

    @staticmethod
    def _update_location_data(canteens, locations_csv_str):
        try:
            # NB: max size of a csv file is 50 MB
            response = requests.post(
                "https://api-adresse.data.gouv.fr/search/csv/",
                files={
                    "data": ("locations.csv", locations_csv_str),
                },
                data={
                    "postcode": "postcode",
                    "citycode": "citycode",
                    "result_columns": ["result_citycode", "result_postcode", "result_city", "result_context"],
                },
                timeout=3,
            )
            response.raise_for_status()  # Raise an exception if the request failed
            for row in csv.reader(response.text.splitlines()):
                if row[0] == "siret":
                    continue  # skip header
                if row[5] != "":  # city found, so rest of data is found
                    canteen = canteens[row[0]]
                    canteen.city_insee_code = row[3]
                    canteen.postal_code = row[4]
                    canteen.city = row[5]
                    canteen.department = row[6].split(",")[0]
                    canteen.save()
        except Exception as e:
            logger.error(f"Error while updating location data : {repr(e)} - {e}")

    @staticmethod
    def _get_manager_emails(row):
        manager_emails = row.split(",")
        normalized_emails = list(map(lambda x: get_user_model().objects.normalize_email(x.strip()), manager_emails))
        for email in normalized_emails:
            validate_email(email)
        return normalized_emails

    @staticmethod
    def _add_managers_to_canteen(emails, canteen, send_invitation_mail=True):
        for email in emails:
            try:
                AddManagerView.add_manager_to_canteen(email, canteen, send_invitation_mail=send_invitation_mail)
            except IntegrityError as e:
                logger.error(
                    f"Attempt to add existing manager with email {email} to canteen {canteen.id} from a CSV import"
                )
                logger.exception(e)


class EmailDiagnosticImportFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            file = request.data["file"]
            self._verify_file_size(file)
            email = request.data.get("email", request.user.email)
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
        except ValidationError:
            logger.error(
                f"{request.user.id} tried to upload a file that is too large (over {settings.CSV_IMPORT_MAX_SIZE})"
            )
            return HttpResponseBadRequest()
        except Exception as e:
            logger.error(f"User {request.user.id} encountered an error when trying to email a diagnostic import file")
            logger.exception(e)
            return HttpResponseServerError()

        return HttpResponse()

    @staticmethod
    def _verify_file_size(file):
        if file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")
