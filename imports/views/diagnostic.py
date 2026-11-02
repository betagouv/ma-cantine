from data.models import Diagnostic

from imports.models import ImportSchema, ImportType
from imports.views.diagnostic_base import BaseDiagnosticsImportView

# Columns: identifier (siret or cantine_id), année_bilan, values
# simple
DIAGNOSTICS_SIMPLE_SIRET_SCHEMA = ImportSchema("bilans_simple_siret.json")
DIAGNOSTICS_SIMPLE_ID_SCHEMA = ImportSchema("bilans_simple_id.json")
DIAGNOSTICS_SIMPLE_SIRET_2026_SCHEMA = ImportSchema("bilans_simple_siret_2026.json")
DIAGNOSTICS_SIMPLE_ID_2026_SCHEMA = ImportSchema("bilans_simple_id_2026.json")
# complete
DIAGNOSTICS_COMPLETE_SCHEMA = ImportSchema("bilans_detaille.json")
DIAGNOSTICS_COMPLETE_2026_SCHEMA = ImportSchema("bilans_detaille_2026.json")


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

    def _get_schemas(self):
        if self.is_siret_import:
            return {"2025": DIAGNOSTICS_SIMPLE_SIRET_SCHEMA, "2026": DIAGNOSTICS_SIMPLE_SIRET_2026_SCHEMA}
        return {"2025": DIAGNOSTICS_SIMPLE_ID_SCHEMA, "2026": DIAGNOSTICS_SIMPLE_ID_2026_SCHEMA}


class DiagnosticsCompleteImportView(BaseDiagnosticsImportView):
    import_type = ImportType.DIAGNOSTIC_COMPLETE
    diagnostic_type = Diagnostic.DiagnosticType.COMPLETE

    def _get_schemas(self):
        return {"2025": DIAGNOSTICS_COMPLETE_SCHEMA, "2026": DIAGNOSTICS_COMPLETE_2026_SCHEMA}
