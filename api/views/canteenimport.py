import csv
import logging
import re
import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models.functions import Lower
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from simple_history.utils import update_change_reason

from api.permissions import IsAuthenticated
from api.serializers import FullCanteenSerializer
from common.api import validata
from common.api.adresse import fetch_geo_data_from_code_csv
from common.utils import file_import
from common.utils import utils as utils_utils
from data.models import Canteen, ImportFailure, ImportType, Sector
from data.utils import CreationSource

from .canteen import AddManagerView
from .utils import camelize

logger = logging.getLogger(__name__)

CANTEEN_SCHEMA_FILE_NAME = "cantines.json"
CANTEEN_ADMIN_SCHEMA_FILE_NAME = "cantines_admin.json"
CANTEEN_SCHEMA_FILE_PATH = f"data/schemas/imports/{CANTEEN_SCHEMA_FILE_NAME}"
CANTEEN_ADMIN_SCHEMA_FILE_PATH = f"data/schemas/imports/{CANTEEN_ADMIN_SCHEMA_FILE_NAME}"
CANTEEN_SCHEMA_URL = (
    f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/staging/{CANTEEN_SCHEMA_FILE_PATH}"
)
CANTEEN_ADMIN_SCHEMA_URL = (
    f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/staging/{CANTEEN_ADMIN_SCHEMA_FILE_PATH}"
)


class ImportCanteensView(APIView):
    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")
    manager_column_idx = 11  # gestionnaires_additionnels
    silent_manager_idx = 11 + 3  # admin_gestionnaires_additionnels
    annotated_sectors = Sector.objects.annotate(name_lower=Lower("name"))

    def __init__(self, **kwargs):
        self.canteens = {}
        self.errors = []
        self.start_time = None
        self.encoding_detected = None
        self.file = None
        self.is_admin_import = False
        super().__init__(**kwargs)

    def post(self, request):  # noqa: C901
        self.start_time = time.time()
        logger.info("Canteen bulk import started")
        try:
            self.file = request.data["file"]
            self.is_admin_import = self.request.user.is_staff
            schema_name = CANTEEN_ADMIN_SCHEMA_FILE_NAME if self.is_admin_import else CANTEEN_SCHEMA_FILE_NAME
            schema_url = CANTEEN_ADMIN_SCHEMA_URL if self.is_admin_import else CANTEEN_SCHEMA_URL

            # Schema validation (Validata)
            validata_response = validata.validate_file_against_schema(self.file, schema_url)

            # Error generating the report
            if "error" in validata_response:
                error = validata_response["error"]["message"]
                self.errors = [
                    {
                        "message": f"Une erreur inconnue s'est produite en lisant votre fichier : « {error} ». Renouveler votre essai, et si l'erreur persiste contactez le support.",
                        "status": 400,
                    }
                ]
                self._log_error(f"Echec lors de la demande de validation du fichier (schema {schema_name} - Validata)")
                return self._get_success_response()

            # Header validation
            header_has_errors = validata.check_if_has_errors_header(validata_response["report"])
            if header_has_errors:
                self.errors = [
                    {
                        "message": "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
                        "status": 400,
                    }
                ]
                self._log_error(f"Echec lors de la validation du header (schema {schema_name} - Validata)")
                return self._get_success_response()

            # Rows validation
            self.errors = validata.process_errors(validata_response["report"])
            if len(self.errors):
                self._log_error(f"Echec lors de la validation du fichier (schema {schema_name} - Validata)")
                return self._get_success_response()

            # ma-cantine validation (permissions, last checks...) + import
            with transaction.atomic():
                self._process_file(validata_response["resource_data"])

                if self.errors:
                    raise IntegrityError()

        except PermissionDenied as e:
            self._log_error(e.detail)
            self.errors = [{"row": 0, "status": 401, "message": e.detail}]
        except IntegrityError as e:
            self._log_error(f"L'import du fichier CSV a échoué:\n{e}")
        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": 400, "message": e.message}]
        except UnicodeDecodeError as e:
            self._log_error(e.reason)
            self.errors = [{"row": 0, "status": 400, "message": "Le fichier doit être sauvegardé en Unicode (utf-8)"}]
        except Exception as e:
            self._log_error(f"Échec lors de la lecture du fichier:\n{e}", "exception")
            self.errors = [{"row": 0, "status": 400, "message": "Échec lors de la lecture du fichier"}]

        return self._get_success_response()

    def _log_error(self, message, level="warning"):
        logger_function = getattr(logger, level)
        logger_function(message)
        ImportFailure.objects.create(
            user=self.request.user,
            file=self.file,
            details=message,
            import_type=ImportType.CANTEEN_ONLY,
        )

    def _process_file(self, data):
        locations_csv_str = "siret,citycode,postcode\n"
        has_locations_to_find = False
        for row_number, row in enumerate(data, start=1):
            try:
                if row_number == 1:  # skip header
                    continue
                canteen, should_update_geolocation = self._save_data_from_row(row)
                self.canteens[canteen.siret] = canteen
                if should_update_geolocation and not self.errors:
                    has_locations_to_find = True
                    if canteen.city_insee_code:
                        locations_csv_str += f"{canteen.siret},{canteen.city_insee_code},\n"
                    else:
                        locations_csv_str += f"{canteen.siret},,{canteen.postal_code}\n"

            except Exception as e:
                for error in self._parse_errors(e, row):
                    self.errors.append(ImportCanteensView._get_error(e, error["message"], error["code"], row_number))
        if has_locations_to_find:
            self._update_location_data(locations_csv_str)

    def _decode_file(self, file):
        # TODO: refactor
        file.seek(0)
        (result, encoding) = file_import.decode_bytes(file.read())
        self.encoding_detected = encoding
        return result

    @transaction.atomic
    def _save_data_from_row(self, row):
        if row[0] == "":
            raise ValidationError({"siret": "Le siret de la cantine ne peut pas être vide"})
        # validate data for format etc, starting with basic non-data-specific row checks
        ImportCanteensView._validate_canteen(row)
        manager_emails = self._get_manager_emails_to_notify(row)
        # return staff-customisable fields
        (
            import_source,
            silently_added_manager_emails,
        ) = self._generate_canteen_meta_fields(row)
        # create the canteen
        canteen, should_update_geolocation = self._update_or_create_canteen(
            row, import_source, manager_emails, silently_added_manager_emails
        )

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
        logger.exception(f"Error on row {row_number}:\n{e}")
        return {"row": row_number, "status": error_status, "message": message}

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            return Canteen._meta.get_field(field_name).verbose_name
        except Exception:
            pass
        return field_name

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
                logger.warning(
                    f"Attempt to add existing manager with email {email} to canteen {canteen.id} from a CSV import:\n{e}"
                )

    def _get_success_response(self):
        serialized_canteens = (
            []
            if len(self.errors)
            else [camelize(FullCanteenSerializer(canteen).data) for canteen in self.canteens.values()]
        )
        body = {
            "canteens": serialized_canteens,
            "count": 0 if len(self.errors) else len(serialized_canteens),
            "errors": self.errors,
            "seconds": time.time() - self.start_time,
            "encoding": self.encoding_detected,
        }
        return JsonResponse(body, status=status.HTTP_200_OK)

    def _update_location_data(self, locations_csv_str):
        try:
            response = fetch_geo_data_from_code_csv(locations_csv_str)
            for row in csv.reader(response.splitlines()):
                if row[0] == "siret":
                    continue  # skip header
                if row[5] != "":  # city found, so rest of data is found
                    canteen = self.canteens[row[0]]
                    canteen.city_insee_code = row[3]
                    canteen.postal_code = row[4]
                    canteen.city = row[5]
                    canteen.department = row[6].split(",")[0]
                    canteen.save()
                    update_change_reason(canteen, f"Mass CSV import - Geo data. {self.__class__.__name__[:100]}")
        except Exception as e:
            logger.exception(f"Error while updating location data : {repr(e)} - {e}")

    @staticmethod
    def _add_error(errors, message, code=400):
        errors.append({"message": message, "code": code})

    @staticmethod
    def _validate_canteen(row):
        if not row[2] and not row[3]:
            raise ValidationError(
                {"postal_code": "Ce champ ne peut pas être vide si le code INSEE de la ville est vide."}
            )
        if row[8] != Canteen.ProductionType.CENTRAL:
            if not row[7]:
                raise ValidationError(
                    {
                        "sectors": f"Ce champ ne peut pas être vide sauf pour les cantines avec le type de production {Canteen.ProductionType.CENTRAL}."
                    }
                )
            if row[7].count("+") > 2:
                raise ValidationError({"sectors": "Ce champ ne peut avoir plus de 3 valeurs."})

    def _get_manager_emails_to_notify(self, row):
        try:
            manager_emails = []
            if len(row) > self.manager_column_idx and row[self.manager_column_idx]:
                manager_emails = ImportCanteensView._get_manager_emails(row[self.manager_column_idx])
        except Exception:
            raise ValidationError(
                {"email": f"Un adresse email des gestionnaires ({row[self.manager_column_idx]}) n'est pas valide."}
            )
        return manager_emails

    def _has_canteen_permission(self, canteen):
        # admin bypass the is_canteen_manager check
        if self.is_admin_import:
            return True
        return self.request.user in canteen.managers.all()

    def _update_or_create_canteen(
        self,
        row,
        import_source,
        manager_emails,
        silently_added_manager_emails,
    ):
        siret = utils_utils.normalize_string(row[0])
        name = row[1].strip()
        daily_meal_count = row[5].strip()
        yearly_meal_count = row[6].strip()
        management_type = row[9].strip().lower()
        production_type = row[8].strip().lower()
        economic_model = row[10].strip().lower()
        central_producer_siret = utils_utils.normalize_string(row[4]) if row[4] else None
        satellite_canteens_count = row[12].strip() if row[12] else None
        canteen_exists = Canteen.objects.filter(siret=siret).exists()
        canteen = (
            Canteen.objects.get(siret=siret)
            if canteen_exists
            else Canteen.objects.create(
                name=name,
                siret=siret,
                daily_meal_count=daily_meal_count,
                yearly_meal_count=yearly_meal_count,
                management_type=management_type,
                production_type=production_type,
                economic_model=economic_model,
                central_producer_siret=central_producer_siret,
                satellite_canteens_count=satellite_canteens_count,
                creation_source=CreationSource.IMPORT,
            )
        )

        if not canteen_exists:
            update_change_reason(canteen, f"Mass CSV import - canteen creation. {self.__class__.__name__[:100]}")

        if canteen_exists and not self._has_canteen_permission(canteen):
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        should_update_geolocation = (
            ImportCanteensView._should_update_geolocation(canteen, row) if canteen_exists else True
        )

        # TODO: remove hardcoded indexes
        canteen.name = row[1].strip()
        canteen.city_insee_code = row[2].strip() if row[2] else None
        canteen.postal_code = row[3].strip() if row[3] else None
        canteen.daily_meal_count = row[5].strip()
        canteen.yearly_meal_count = row[6].strip()
        # sectors: see below
        canteen.production_type = row[8].strip().lower()
        canteen.management_type = row[9].strip().lower()
        canteen.economic_model = row[10].strip().lower()
        canteen.central_producer_siret = utils_utils.normalize_string(row[4]) if row[4] else None
        canteen.satellite_canteens_count = satellite_canteens_count
        if self.is_admin_import:
            canteen.line_ministry = (
                next((key for key, value in Canteen.Ministries.choices if value == row[13].strip()), None)
                if row[13]
                else None
            )
            canteen.import_source = import_source
        if row[7]:
            canteen.sectors.set(
                [
                    self.annotated_sectors.get(name_lower__unaccent=sector.strip().lower())
                    for sector in row[7].split("+")
                ]
            )

        canteen.save()
        update_change_reason(canteen, f"Mass CSV import. {self.__class__.__name__[:100]}")

        if not self.request.user.is_staff:
            canteen.managers.add(self.request.user)
        if manager_emails:
            ImportCanteensView._add_managers_to_canteen(manager_emails, canteen)
        if silently_added_manager_emails:
            ImportCanteensView._add_managers_to_canteen(
                silently_added_manager_emails, canteen, send_invitation_mail=False
            )
        return (canteen, should_update_geolocation)

    def _generate_canteen_meta_fields(self, row):
        silently_added_manager_emails = []
        import_source = "Import massif"
        if len(row) > self.silent_manager_idx:  # already checked earlier that it's a staff user
            try:
                if row[self.silent_manager_idx]:
                    silently_added_manager_emails = ImportCanteensView._get_manager_emails(
                        row[self.silent_manager_idx]
                    )
            except Exception:
                raise ValidationError(
                    {
                        "email": f"Un adresse email des gestionnaires (pas notifiés) ({row[self.silent_manager_idx]}) n'est pas valide."
                    }
                )
            import_source = row[self.silent_manager_idx + 1].strip()

        return (import_source, silently_added_manager_emails)

    def _parse_errors(self, e, row):  # noqa: C901
        errors = []
        if isinstance(e, PermissionDenied):
            ImportCanteensView._add_error(errors, e.detail, 401)
        elif isinstance(e, Sector.DoesNotExist):
            ImportCanteensView._add_error(errors, "Le secteur spécifié ne fait pas partie des options acceptées")
        elif isinstance(e, ValidationError):
            if hasattr(e, "message_dict"):
                for field, messages in e.message_dict.items():
                    verbose_field_name = ImportCanteensView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if field != "__all__":
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        ImportCanteensView._add_error(errors, user_message)
            elif hasattr(e, "message"):
                ImportCanteensView._add_error(errors, e.message)
            elif hasattr(e, "params"):
                ImportCanteensView._add_error(errors, f"La valeur '{e.params['value']}' n'est pas valide.")
            else:
                logger.exception(f"Unknown validation error: {e}")
                ImportCanteensView._add_error(
                    errors, "Une erreur s'est produite en créant une cantine pour cette ligne"
                )
        elif isinstance(e, ValueError):
            match = self.value_error_regex.search(str(e))
            field_name = match.group(1) if match else ""
            value_given = match.group(2) if match else ""
            if field_name:
                verbose_field_name = ImportCanteensView._get_verbose_field_name(field_name)
                ImportCanteensView._add_error(
                    errors, f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
                )
        elif isinstance(e, Canteen.MultipleObjectsReturned):
            ImportCanteensView._add_error(
                errors,
                f"Plusieurs cantines correspondent au SIRET {row[0]}. Veuillez enlever les doublons.",
            )
        elif isinstance(e, FileFormatError):
            ImportCanteensView._add_error(errors, e.detail)
        if not errors:
            logger.exception(f"No errors added through parsing but exception raised: {e}")
            ImportCanteensView._add_error(errors, "Une erreur s'est produite en créant une cantine pour cette ligne")
        return errors


class FileFormatError(Exception):
    def __init__(self, detail, **kwargs):
        self.detail = detail
        super().__init__(detail)
