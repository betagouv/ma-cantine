import logging
import re
import time
from abc import ABC, abstractmethod
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from simple_history.utils import update_change_reason

from api.permissions import IsAuthenticated
from common.utils import file_import
from data.models import Canteen, Diagnostic, ImportFailure, ImportType
from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)


DIAGNOSTICS_SCHEMA_FILE_PATH = "data/schemas/imports/bilans_simple.json"


class ImportDiagnosticsView(ABC, APIView):
    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")
    manager_column_idx = 11
    year_idx = 12

    def __init__(self, **kwargs):
        self.diagnostics_created = 0
        self.errors = []
        self.start_time = None
        self.file = None
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def import_type(): ...

    def post(self, request):
        self.start_time = time.time()
        logger.info("Diagnostic bulk import started")
        try:
            with transaction.atomic():
                self.file = request.data["file"]
                file_import.validate_file_size(self.file)
                self._process_file(self.file)
                if self.errors:
                    raise IntegrityError()
        except PermissionDenied as e:
            self._log_error(e.detail)
            self.errors = [{"row": 0, "status": 401, "message": e.detail}]
        except IntegrityError as e:
            self._log_error(f"L'import du fichier CSV a échoué: {e}")
        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": 400, "message": e.message}]
        except Exception as e:
            message = f"Échec lors de la lecture du fichier: {e}"
            self._log_error(message, "exception")
            self.errors = [{"row": 0, "status": 400, "message": message}]

        return self._get_success_response()

    def _log_error(self, message, level="warning"):
        logger_function = getattr(logger, level)
        logger_function(message)
        ImportFailure.objects.create(
            user=self.request.user,
            file=self.file,
            details=message,
            import_type=self.import_type,
        )

    def _process_file(self, file):
        print("file")
        print(file)
        # TODO : add Validata checks
        # TODO : add a loop with Validata returned rows
        rows = []
        for row_number, row in rows:
            try:
                self._save_data_from_row(row)
            except Exception as e:
                for error in self._parse_errors(e, row):
                    self.errors.append(
                        ImportDiagnosticsView._get_error(e, error["message"], error["code"], row_number + 1)
                    )

    @transaction.atomic
    def _save_data_from_row(self, row):
        diagnostic_year, values_dict, diagnostic_type = self._validate_diagnostic(row)
        print("diagnostic_year")
        print(diagnostic_year)
        print("values_dict")
        print(values_dict)
        print("diagnostic_type")
        print(diagnostic_type)
        canteen = ""  # TODO : find canteen from SIRET and link diagnostic to canteen
        self._has_canteen_permission(
            canteen
        )  # TODO : check if user has permission to create diagnostic for this canteen
        self._update_or_create_diagnostic(canteen, diagnostic_year, values_dict, diagnostic_type)

    @abstractmethod
    def _validate_diagnostic(self, row): ...

    def _update_or_create_diagnostic(self, canteen, diagnostic_year, values_dict, diagnostic_type):
        diagnostic_exists = Diagnostic.objects.filter(canteen=canteen, year=diagnostic_year).exists()
        diagnostic = (
            Diagnostic.objects.get(canteen=canteen, year=diagnostic_year)
            if diagnostic_exists
            else Diagnostic(canteen_id=canteen.id, year=diagnostic_year, creation_source=CreationSource.IMPORT)
        )
        if diagnostic.is_teledeclared:
            raise ValidationError(
                "Ce n'est pas possible de modifier un diagnostic télédéclaré. Veuillez retirer cette ligne, ou annuler la télédéclaration."
            )
        diagnostic.diagnostic_type = diagnostic_type
        for key, value in values_dict.items():
            setattr(diagnostic, key, value)
        diagnostic.full_clean()
        diagnostic.save()
        update_change_reason(diagnostic, f"Mass CSV import. {self.__class__.__name__[:100]}")
        self.diagnostics_created += 1

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        return {"row": row_number, "status": error_status, "message": message}

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            return Canteen._meta.get_field(field_name).verbose_name
        except Exception:
            try:
                return Diagnostic._meta.get_field(field_name).verbose_name
            except Exception:
                pass
        return field_name

    def _get_success_response(self):
        body = {
            "count": 0 if len(self.errors) else self.diagnostics_created,
            "errors": self.errors,
            "errorCount": len(self.errors),
            "seconds": time.time() - self.start_time,
        }
        return JsonResponse(body, status=status.HTTP_200_OK)

    @staticmethod
    def _add_error(errors, message, code=400):
        errors.append({"message": message, "code": code})

    def _has_canteen_permission(self, canteen):
        return self.request.user in canteen.managers.all()

    def _parse_errors(self, e, row):  # noqa: C901
        errors = []
        if isinstance(e, PermissionDenied):
            ImportDiagnosticsView._add_error(errors, e.detail, 401)
        elif isinstance(e, ValidationError):
            if hasattr(e, "message_dict"):
                for field, messages in e.message_dict.items():
                    verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if field != "__all__":
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        ImportDiagnosticsView._add_error(errors, user_message)
            elif hasattr(e, "message"):
                ImportDiagnosticsView._add_error(errors, e.message)
            elif hasattr(e, "params"):
                ImportDiagnosticsView._add_error(errors, f"La valeur '{e.params['value']}' n'est pas valide.")
            else:
                ImportDiagnosticsView._add_error(
                    errors, "Une erreur s'est produite en créant un diagnostic pour cette ligne"
                )
        elif isinstance(e, ValueError):
            match = self.value_error_regex.search(str(e))
            field_name = match.group(1) if match else ""
            value_given = match.group(2) if match else ""
            if field_name:
                verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field_name)
                ImportDiagnosticsView._add_error(
                    errors, f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
                )
        if not errors:
            ImportDiagnosticsView._add_error(
                errors, "Une erreur s'est produite en créant un diagnostic pour cette ligne"
            )
        return errors


class DiagnosticsSimpleImportView(ImportDiagnosticsView):
    total_value_idx = 13
    import_type = ImportType.DIAGNOSTIC_SIMPLE

    def _validate_diagnostic(self, row):
        values_dict = None
        diagnostic_year = row[self.year_idx]
        appro_fields_length = len(row) - self.total_value_idx
        value_fields = Diagnostic.SIMPLE_APPRO_FIELDS_FOR_IMPORT[:appro_fields_length]
        values_dict = {}
        value_offset = 0
        for value in value_fields:
            value_offset = value_offset + 1
            value_idx = self.year_idx + value_offset
            values_dict[value] = None if not row[value_idx] else Decimal(row[value_idx].strip().replace(",", "."))
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.SIMPLE
