import logging
import re
import time
from abc import ABC, abstractmethod

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from api.permissions import IsAuthenticated
from common.api import validata
from common.utils import file_import
from data.models import EventLog, ImportFailure
from imports.schemas import detect_schema

logger = logging.getLogger(__name__)


class BaseImportView(ABC, APIView):
    """
    Abstract base class for CSV/TSV file imports.

    Handles common workflow:
    1. File validation (size, format)
    2. Schema validation via Validata
    3. Header validation: detects which of the accepted schemas the file uses (self.schema)
    4. Row-by-row processing with transactions
    5. Error handling and logging

    Subclasses must implement:
    - import_type: ImportType enum for logging failures
    - model_class: Main Django model being imported
    - _get_schemas(): Return the list of accepted schemas
    - _save_data_from_row(row): Process and save a single row
    - _get_response_data(): Return success response data
    """

    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")

    def __init__(self, **kwargs):
        self.errors = []
        self.start_time = time.time()
        self.file = None
        self.schema = None
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def import_type(self):
        """ImportType enum for logging failures"""
        pass

    @property
    @abstractmethod
    def model_class(self):
        """Main Django model being imported"""
        pass

    @abstractmethod
    def _get_schemas(self):
        """
        Return the list of accepted schemas (ImportSchema).

        The file is validated against the schema whose header matches the file header.
        If none matches, the header errors are computed against the first schema.
        """
        pass

    @abstractmethod
    def _save_data_from_row(self, row):
        """
        Process and save a single row.

        Args:
            row: List of values from CSV row

        Returns:
            Created or updated model instance
        """
        pass

    @abstractmethod
    def _get_response_data(self):
        """
        Return success response data specific to import type.

        Returns:
            dict: Response data to merge with base response
        """
        pass

    def is_true_value(self, value):
        """
        Check if a value is a true value.
        """
        return value.strip().lower() in ["oui", "x"]

    def post(self, request):
        self.start_time = time.time()
        self._log_import_start()

        try:
            # File validation
            self.file = request.data["file"]
            if not self._validate_file_size():
                return self._get_success_response()

            # Schema validation (Validata), first against the default schema
            schemas = self._get_schemas()
            default_schema = schemas[0]
            validata_response = self._validate_file_against_schema(default_schema)
            if validata_response is None:
                return self._get_success_response()

            # Header validation
            user_file_header = validata_response["resource_data"][0]
            # Custom header validation
            if not self._validate_file_header_custom(user_file_header):
                self._log_error(f"Echec lors de la validation du header (schema {default_schema.name} - Validata)")
                return self._get_success_response()
            # Generic header validation: detect the schema used by the file
            self.schema = detect_schema(user_file_header, schemas)
            if not self.schema:
                self.errors = validata.process_header_errors(user_file_header, default_schema.header)
                self._log_error(f"Echec lors de la validation du header (schema {default_schema.name} - Validata)")
                return self._get_success_response()
            if self.schema.import_type:
                self.import_type = self.schema.import_type
            # The file uses another accepted schema: validate it against this one
            if self.schema != default_schema:
                validata_response = self._validate_file_against_schema(self.schema)
                if validata_response is None:
                    return self._get_success_response()

            # Rows validation
            self.errors = validata.process_errors(validata_response["report"])
            if len(self.errors):
                self._log_error(f"Echec lors de la validation du fichier (schema {self.schema.name} - Validata)")
                return self._get_success_response()

            # ma-cantine validation (permissions, last checks...) + import
            with transaction.atomic():
                self._process_file(validata_response["resource_data"])

                if self.errors:
                    raise IntegrityError()

                # Allow subclasses to do post-processing
                self._post_process_file()

        except PermissionDenied as e:
            self._log_error(e.detail)
            self.errors = [{"row": 0, "status": status.HTTP_401_UNAUTHORIZED, "message": e.detail}]
        except IntegrityError as e:
            self._log_error(f"L'import du fichier CSV a échoué: {e}")
        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": status.HTTP_400_BAD_REQUEST, "message": e.message}]
        except Exception as e:
            message = f"Échec lors de la lecture du fichier: {e}"
            self._log_error(message, "exception")
            self.errors = [{"row": 0, "status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": message}]

        return self._get_success_response()

    @abstractmethod
    def _process_file(self, data):
        """
        Process all rows in the file.

        Args:
            data: List of rows from validated CSV file

        Implementation should:
        - Iterate through rows (skipping header)
        - Call _save_data_from_row() for each row
        - Handle exceptions and add to self.errors
        """
        pass

    def _post_process_file(self):
        """
        Hook for post-processing after all rows are processed.

        Override in subclasses if needed (e.g., geo-location updates).
        """
        pass

    def _get_row_identifier(self, row):
        """
        Get identifier from row for error messages.

        Override in subclasses to provide meaningful identifiers.
        Default: first column (often SIRET)
        """
        return row[0] if row else None

    def _validate_file_against_schema(self, schema):
        """
        Validate the file against the schema (Validata).

        Returns:
            dict: Validata response, or None if Validata could not generate the report
        """
        validata_response = validata.validate_file_against_schema(self.file, schema.url)
        if "error" in validata_response:
            error = validata_response["error"]["message"]
            self.errors = [
                {
                    "message": f"Une erreur inconnue s'est produite en lisant votre fichier : « {error} ». Renouveler votre essai, et si l'erreur persiste contactez le support.",
                    "status": 400,
                }
            ]
            self._log_error(f"Echec lors de la demande de validation du fichier (schema {schema.name} - Validata)")
            return None
        return validata_response

    def _validate_file_size(self):
        """
        Validate file size and handle ValidationError.

        Returns:
            bool: True if validation passed, False if file is too large
        """
        try:
            file_import.validate_file_size(self.file)
            return True
        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": status.HTTP_400_BAD_REQUEST, "message": e.message}]
            return False

    def _validate_file_header_custom(self, user_file_header):
        """
        Validate file header custom.

        Returns:
            bool: True if validation passed, False otherwise
        """
        return True

    def _has_canteen_permission(self, canteen):
        """
        Check if user has permission to access canteen or if is staff.
        """
        if self.request.user.is_staff:
            return True
        return self.request.user in canteen.managers.all()

    def _log_import_start(self):
        """Log the start of import process"""
        logger.info(f"{self.__class__.__name__} bulk import started")

    def _log_error(self, message, level="warning"):
        """Log error and create ImportFailure & EventLog records"""
        logger_function = getattr(logger, level)
        logger_function(message)
        ImportFailure.objects.create(
            user=self.request.user,
            file=self.file,
            details=message,
            import_type=self.import_type,
        )
        EventLog.log(
            EventLog.Category.IMPORT,
            self.import_type,
            EventLog.Status.FAILURE,
            user=self.request.user,
            data={"message": message, "count": None, "seconds": self._get_duration()},
        )

    def _log_success(self, response_data):
        """Create EventLog record (linked to the canteen if the import concerns a single canteen)"""
        canteen_ids = self._get_canteen_ids()
        EventLog.log(
            EventLog.Category.IMPORT,
            self.import_type,
            EventLog.Status.SUCCESS,
            user=self.request.user,
            canteen_id=next(iter(canteen_ids)) if len(canteen_ids) == 1 else None,
            data={"message": None, "count": response_data.get("count"), "seconds": self._get_duration()},
        )

    def _get_canteen_ids(self):
        """
        Ids of the canteens concerned by the import (only called on success: on failure, the objects are rolled back)
        Override in subclasses.
        """
        return set()

    def _get_duration(self):
        return round(time.time() - self.start_time, 2)

    def _get_success_response(self):
        """Build final response with errors and timing"""
        response_data = self._get_response_data()
        base_response = {
            "errors": self.errors,
            "seconds": time.time() - self.start_time,
        }
        if len(self.errors) > 0:
            response_data["count"] = 0
        else:
            self._log_success(response_data)
        return JsonResponse({**response_data, **base_response}, status=status.HTTP_200_OK)

    def _parse_errors(self, e, row, identifier=None):
        """
        Parse exceptions into error dictionaries.

        Can be extended by subclasses for custom error handling.
        """
        errors = []

        if isinstance(e, PermissionDenied):
            self._add_error(errors, e.detail, 401)
        elif isinstance(e, ObjectDoesNotExist):
            message = self._get_not_found_message(identifier)
            errors.append({"message": message, "code": 404})
        elif isinstance(e, ValidationError):
            self._parse_validation_error(e, errors)
        elif isinstance(e, ValueError):
            self._parse_value_error(e, errors)

        # Fallback for any error that didn't produce error messages
        if not errors:
            logger.exception(f"No errors added through parsing but exception raised: {e}")
            self._add_error(errors, self._get_generic_error_message())

        return errors

    def _parse_validation_error(self, e, errors):
        """Parse Django ValidationError"""
        if hasattr(e, "message_dict"):
            for field, messages in e.message_dict.items():
                verbose_field_name = self._get_verbose_field_name(field)
                for message in messages:
                    user_message = message
                    if field != "__all__":
                        user_message = f"Champ '{verbose_field_name}' : {user_message}"
                    self._add_error(errors, user_message)
        elif hasattr(e, "message"):
            self._add_error(errors, e.message)
        elif hasattr(e, "params"):
            self._add_error(errors, f"La valeur '{e.params['value']}' n'est pas valide.")
        else:
            self._add_error(errors, self._get_generic_error_message())

    def _parse_value_error(self, e, errors):
        """Parse ValueError with field information"""
        match = self.value_error_regex.search(str(e))
        field_name = match.group(1) if match else ""
        value_given = match.group(2) if match else ""
        if field_name:
            verbose_field_name = self._get_verbose_field_name(field_name)
            self._add_error(errors, f"Champ '{verbose_field_name}' : la valeur '{value_given}' n'est pas valide.")

    def _get_not_found_message(self, identifier):
        """Get error message for object not found"""
        return f"Une cantine avec le siret « {identifier} » n'existe pas sur la plateforme."

    def _get_generic_error_message(self):
        """Get generic error message for row processing failure"""
        return "Une erreur s'est produite en créant un objet pour cette ligne"

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        """Create error dictionary"""
        return {"row": row_number, "status": error_status, "message": message}

    @staticmethod
    def _add_error(errors, message, code=400):
        """Add error to errors list"""
        errors.append({"message": message, "code": code})

    def _get_verbose_field_name(self, field_name):
        """
        Get verbose name for field from model.

        Override in subclasses if multiple models need to be checked.
        """
        try:
            return self.model_class._meta.get_field(field_name).verbose_name
        except Exception:
            return field_name
