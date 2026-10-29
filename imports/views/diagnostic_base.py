from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from simple_history.utils import update_change_reason

from imports.views.base import BaseImportView
from data.models import Canteen, Diagnostic
from data.models.creation_source import CreationSource


class BaseDiagnosticsImportView(BaseImportView):
    """
    Shared logic for diagnostic CSV imports.

    Subclasses provide:
    - `diagnostic_type`: the type of the diagnostics created or updated (simple or complete)
    - `_get_schema()`: which JSON Table Schema to validate against
      (columns: identifier (siret or cantine_id), année_bilan, values)
    """

    model_class = Diagnostic
    diagnostic_type = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diagnostics_created_count = 0
        self.canteen_ids = set()
        self.is_siret_import = True

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
        if self.is_siret_import and not Canteen.objects.filter(siret=identifier).exists():
            raise ObjectDoesNotExist()
        elif not self.is_siret_import and not Canteen.objects.filter(id=identifier).exists():
            raise ObjectDoesNotExist()
        canteen = Canteen.objects.get(siret=identifier) if self.is_siret_import else Canteen.objects.get(id=identifier)
        if self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")
        diagnostic_year, values_dict, diagnostic_type = self._validate_diagnostic(row)
        self._update_or_create_diagnostic(canteen, diagnostic_year, values_dict, diagnostic_type)

    def _validate_diagnostic(self, row):
        """Parse row (values read by column name) and return (year, values_dict, diagnostic_type)"""
        _, year_column, *value_columns = self.schema.header
        row_dict = self._get_row_dict(row)
        values_dict = {column: row_dict[column] or None for column in value_columns}
        return row_dict[year_column], values_dict, self.diagnostic_type

    def _update_or_create_diagnostic(self, canteen, diagnostic_year, values_dict, diagnostic_type):
        diagnostic_exists = Diagnostic.objects.filter(canteen=canteen, year=diagnostic_year).exists()
        diagnostic = (
            Diagnostic.objects.get(canteen=canteen, year=diagnostic_year)
            if diagnostic_exists
            else Diagnostic(
                canteen_id=canteen.id,
                year=diagnostic_year,
                creation_user=self.request.user,
                creation_source=CreationSource.IMPORT,
            )
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
        self.canteen_ids.add(diagnostic.canteen_id)

    def _get_canteen_ids(self):
        return self.canteen_ids

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
        identifier_name = "le siret" if self.is_siret_import else "l'id"
        return f"Une cantine avec {identifier_name} « {identifier} » n'existe pas sur la plateforme."
