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
from data.models import ImportFailure

logger = logging.getLogger(__name__)


class BaseImportView(ABC, APIView):
    """
    Abstract base class for CSV/TSV file imports.

    Handles common workflow:
    1. File validation (size, format)
    2. Schema validation via Validata
    3. Header validation
    4. Row-by-row processing with transactions
    5. Error handling and logging

    Subclasses must implement:
    - import_type: ImportType enum for logging failures
    - model_class: Main Django model being imported
    - _get_schema_config(): Return schema configuration dict
    - _save_data_from_row(row): Process and save a single row
    - _get_response_data(): Return success response data
    """

    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")

    def __init__(self, **kwargs):
        self.errors = []
        self.start_time = None
        self.file = None
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
    def _get_schema_config(self):
        """
        Return schema configuration dictionary.

        Returns:
            dict: Must contain 'name' and 'url' keys
                {
                    'name': 'schema_file.json',
                    'url': 'https://...'
                }
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

    def post(self, request):
        self.start_time = time.time()
        self._log_import_start()

        try:
            # File validation
            self.file = request.data["file"]
            file_import.validate_file_size(self.file)

            # Schema validation (Validata)
            schema_config = self._get_schema_config()
            validata_response = validata.validate_file_against_schema(self.file, schema_config["url"])

            # Error generating the report
            if "error" in validata_response:
                error = validata_response["error"]["message"]
                self.errors = [
                    {
                        "message": f"Une erreur inconnue s'est produite en lisant votre fichier : « {error} ». Renouveler votre essai, et si l'erreur persiste contactez le support.",
                        "status": 400,
                    }
                ]
                self._log_error(
                    f"Echec lors de la demande de validation du fichier (schema {schema_config['name']} - Validata)"
                )
                return self._get_success_response()

            # Header validation
            if not self._validate_header(validata_response, schema_config["name"]):
                return self._get_success_response()

            # Rows validation
            self.errors = validata.process_errors(validata_response["report"])
            if len(self.errors):
                self._log_error(f"Echec lors de la validation du fichier (schema {schema_config['name']} - Validata)")
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

    def _validate_header(self, validata_response, schema_name):
        """
        Validate file header.

        Can be overridden by subclasses for custom header validation.
        """
        header_has_errors = validata.check_if_has_errors_header(validata_response["report"])
        if header_has_errors:
            self.errors = [
                {
                    "message": "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
                    "status": 400,
                }
            ]
            self._log_error(f"Echec lors de la validation du header (schema {schema_name} - Validata)")
            return False
        return True

    def _process_file(self, data):
        """
        Process all rows in the file.

        Can be overridden by subclasses for custom processing (e.g., chunking).
        """
        for row_number, row in enumerate(data, start=1):
            if row_number == 1:  # skip header
                continue
            try:
                self._save_data_from_row(row)
            except Exception as e:
                identifier = self._get_row_identifier(row)
                for error in self._parse_errors(e, row, identifier):
                    self.errors.append(self._get_error(e, error["message"], error["code"], row_number))

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

    def _log_import_start(self):
        """Log the start of import process"""
        logger.info(f"{self.__class__.__name__} bulk import started")

    def _log_error(self, message, level="warning"):
        """Log error and create ImportFailure record"""
        logger_function = getattr(logger, level)
        logger_function(message)
        ImportFailure.objects.create(
            user=self.request.user,
            file=self.file,
            details=message,
            import_type=self.import_type,
        )

    def _get_success_response(self):
        """Build final response with errors and timing"""
        response_data = self._get_response_data() if not self.errors else {}
        base_response = {
            "errors": self.errors,
            "seconds": time.time() - self.start_time,
        }
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
            self._add_error(
                errors, f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
            )

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
