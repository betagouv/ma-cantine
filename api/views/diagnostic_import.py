from abc import abstractmethod

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from simple_history.utils import update_change_reason

from api.views.base_import import BaseImportView
from data.models import Canteen, Diagnostic, ImportType
from data.models.creation_source import CreationSource


# simple
DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_FILE_NAME = "bilans_simple_siret.json"
DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_FILE_PATH = f"data/schemas/imports/{DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_FILE_NAME}"
DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_FILE_PATH}"
DIAGNOSTICS_SIMPLE_ID_SCHEMA_FILE_NAME = "bilans_simple_id.json"
DIAGNOSTICS_SIMPLE_ID_SCHEMA_FILE_PATH = f"data/schemas/imports/{DIAGNOSTICS_SIMPLE_ID_SCHEMA_FILE_NAME}"
DIAGNOSTICS_SIMPLE_ID_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{DIAGNOSTICS_SIMPLE_ID_SCHEMA_FILE_PATH}"
# complete
DIAGNOSTICS_COMPLETE_SCHEMA_FILE_NAME = "bilans_detaille.json"
DIAGNOSTICS_COMPLETE_SCHEMA_FILE_PATH = f"data/schemas/imports/{DIAGNOSTICS_COMPLETE_SCHEMA_FILE_NAME}"
DIAGNOSTICS_COMPLETE_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{DIAGNOSTICS_COMPLETE_SCHEMA_FILE_PATH}"


class DiagnosticsImportView(BaseImportView):
    model_class = Diagnostic

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diagnostics_created_count = 0
        self.is_id_import = False

    def _process_file(self, data):
        """Process all rows in the file."""
        for row_number, row in enumerate(data, start=1):
            if row_number == 1:  # skip header
                continue
            try:
                self._save_data_from_row(row)
            except Exception as e:
                identifier = self._get_row_identifier(row)
                for error in self._parse_errors(e, row, identifier):
                    self.errors.append(self._get_error(e, error["message"], error["code"], row_number))

    @transaction.atomic
    def _save_data_from_row(self, row):
        identifier = row[0]
        if self.is_id_import and not Canteen.objects.filter(id=identifier).exists():
            raise ObjectDoesNotExist()
        elif not self.is_id_import and not Canteen.objects.filter(siret=identifier).exists():
            raise ObjectDoesNotExist()
        canteen = Canteen.objects.get(id=identifier) if self.is_id_import else Canteen.objects.get(siret=identifier)
        # TODO : once it's merge re-use _has_canteen_manager_permission from base_import.py
        if self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")
        diagnostic_year, values_dict, diagnostic_type = self._validate_diagnostic(row)
        self._update_or_create_diagnostic(canteen, diagnostic_year, values_dict, diagnostic_type)

    @abstractmethod
    def _validate_diagnostic(self, row):
        """Parse row and return (year, values_dict, diagnostic_type)"""
        pass

    def _update_or_create_diagnostic(self, canteen, diagnostic_year, values_dict, diagnostic_type):
        diagnostic_exists = Diagnostic.objects.filter(canteen=canteen, year=diagnostic_year).exists()
        diagnostic = (
            Diagnostic.objects.get(canteen=canteen, year=diagnostic_year)
            if diagnostic_exists
            else Diagnostic(canteen_id=canteen.id, year=diagnostic_year, creation_source=CreationSource.IMPORT)
        )
        if diagnostic.is_teledeclared:
            raise ValidationError(
                "Ce n'est pas possible de modifier un bilan télédéclaré. Veuillez retirer cette ligne, ou annuler la télédéclaration."
            )
        diagnostic.diagnostic_type = diagnostic_type
        for key, value in values_dict.items():
            setattr(diagnostic, key, value)
        diagnostic.full_clean()
        diagnostic.save()
        update_change_reason(diagnostic, f"Mass CSV import. {self.__class__.__name__[:100]}")
        self.diagnostics_created_count += 1

    def _get_response_data(self):
        return {
            "count": self.diagnostics_created_count,
        }

    def _get_verbose_field_name(self, field_name):
        """Check both Canteen and Diagnostic models for field names"""
        try:
            return Canteen._meta.get_field(field_name).verbose_name
        except Exception:
            try:
                return Diagnostic._meta.get_field(field_name).verbose_name
            except Exception:
                pass
        return field_name

    def _get_generic_error_message(self):
        return "Une erreur s'est produite en créant un bilan pour cette ligne"

    def _parse_errors(self, e, row, identifier=None):
        """Extended error parsing to handle MultipleObjectsReturned"""
        errors = []

        # Handle specific case for multiple canteens with same SIRET
        if isinstance(e, Canteen.MultipleObjectsReturned):
            self._add_error(
                errors,
                f"Plusieurs cantines correspondent au SIRET {identifier}. Veuillez enlever les doublons pour pouvoir créer le bilan.",
            )
            return errors

        # Fall back to base class handling
        return super()._parse_errors(e, row, identifier)

    def _get_not_found_message(self, identifier):
        """Get error message for object not found"""
        identifier_name = "l'id" if self.is_id_import else "le siret"
        return f"Une cantine avec {identifier_name} « {identifier} » n'existe pas sur la plateforme."


class DiagnosticsSimpleImportView(DiagnosticsImportView):
    import_type = ImportType.DIAGNOSTIC_SIMPLE_SIRET

    def post(self, request):
        # Set import type based on request
        self.is_id_import = request.data.get("type") == "id"
        self.import_type = ImportType.DIAGNOSTIC_SIMPLE_ID if self.is_id_import else ImportType.DIAGNOSTIC_SIMPLE_SIRET
        return super().post(request)

    def _get_schema_config(self):
        return {
            "name": DIAGNOSTICS_SIMPLE_ID_SCHEMA_FILE_NAME
            if self.is_id_import
            else DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_FILE_NAME,
            "url": DIAGNOSTICS_SIMPLE_ID_SCHEMA_URL if self.is_id_import else DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_URL,
            "path": DIAGNOSTICS_SIMPLE_ID_SCHEMA_FILE_PATH
            if self.is_id_import
            else DIAGNOSTICS_SIMPLE_SIRET_SCHEMA_FILE_PATH,
        }

    def _validate_diagnostic(self, row):
        values_dict = {}
        diagnostic_year = row[1]
        offset_row = 2  # Two columns before value_fields in row
        for idx, value in enumerate(Diagnostic.SIMPLE_APPRO_FIELDS):
            value_idx = idx + offset_row
            values_dict[value] = None if not row[value_idx] else row[value_idx]
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.SIMPLE


class DiagnosticsCompleteImportView(DiagnosticsImportView):
    import_type = ImportType.DIAGNOSTIC_COMPLETE

    def _get_schema_config(self):
        return {
            "name": DIAGNOSTICS_COMPLETE_SCHEMA_FILE_NAME,
            "url": DIAGNOSTICS_COMPLETE_SCHEMA_URL,
            "path": DIAGNOSTICS_COMPLETE_SCHEMA_FILE_PATH,
        }

    def _validate_diagnostic(self, row):
        values_dict = {}
        diagnostic_year = row[1]
        offset_row = 2  # Two columns before value_fields in row
        for idx, value in enumerate(Diagnostic.COMPLETE_APPRO_FIELDS):
            value_idx = idx + offset_row
            values_dict[value] = None if not row[value_idx] else row[value_idx]
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.COMPLETE
