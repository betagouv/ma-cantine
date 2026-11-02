from data.models import Diagnostic

from imports.models import ImportSchema, ImportType
from imports.views.diagnostic_base import BaseDiagnosticsImportView

# Columns: identifier (siret or cantine_id), année_bilan, values
# simple
DIAGNOSTICS_SIMPLE_SIRET_SCHEMA = ImportSchema("bilans_simple_siret.json")
DIAGNOSTICS_SIMPLE_ID_SCHEMA = ImportSchema("bilans_simple_id.json")
DIAGNOSTICS_SIMPLE_SIRET_2026_SCHEMA = ImportSchema("bilans_simple_siret_2026.json")  # not used yet
DIAGNOSTICS_SIMPLE_ID_2026_SCHEMA = ImportSchema("bilans_simple_id_2026.json")  # not used yet
# complete
DIAGNOSTICS_COMPLETE_SCHEMA = ImportSchema("bilans_detaille.json")


class DiagnosticsSimpleImportView(BaseDiagnosticsImportView):
    import_type = ImportType.DIAGNOSTIC_SIMPLE_SIRET
    diagnostic_type = Diagnostic.DiagnosticType.SIMPLE

    def post(self, request):
        # Set import type based on request
        self.is_siret_import = request.data.get("type") == "siret"
        self.import_type = (
            ImportType.DIAGNOSTIC_SIMPLE_SIRET if self.is_siret_import else ImportType.DIAGNOSTIC_SIMPLE_ID
        )
        return super().post(request)

    def _get_schema(self):
        return DIAGNOSTICS_SIMPLE_SIRET_SCHEMA if self.is_siret_import else DIAGNOSTICS_SIMPLE_ID_SCHEMA


class DiagnosticsCompleteImportView(BaseDiagnosticsImportView):
    import_type = ImportType.DIAGNOSTIC_COMPLETE
    diagnostic_type = Diagnostic.DiagnosticType.COMPLETE

    def _get_schema(self):
        return DIAGNOSTICS_COMPLETE_SCHEMA
