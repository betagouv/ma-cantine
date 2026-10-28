from data.models import Purchase

from imports.schemas import ImportSchema
from imports.views.purchase_base import BasePurchasesImportView

PURCHASE_SIRET_SCHEMA = ImportSchema("achats_siret.json")
PURCHASE_ID_SCHEMA = ImportSchema("achats_id.json")


class PurchasesImportView(BasePurchasesImportView):
    siret_schema = PURCHASE_SIRET_SCHEMA
    id_schema = PURCHASE_ID_SCHEMA

    def _get_caracteristiques(self, row):
        categories_egalim = row[6].strip() if row[6] else ""
        origine = row[7].strip() if row[7] else ""
        est_circuit_court = row[8].strip().lower() if row[8] else ""
        est_local = row[9].strip().lower() if row[9] else ""

        egalim_caracteristics = categories_egalim.split(",") if categories_egalim else []
        origine_caracteristics = origine.split(",") if origine else []
        circuit_court_caracteristics = (
            [Purchase.Characteristic.CIRCUIT_COURT] if self.is_true_value(est_circuit_court) else []
        )
        local_caracteristics = [Purchase.Characteristic.LOCAL] if self.is_true_value(est_local) else []
        return egalim_caracteristics + origine_caracteristics + circuit_court_caracteristics + local_caracteristics

    def _get_definition_local(self, row):
        return row[10].strip() if row[10] else ""

    def _get_definition_local_km(self, row):
        return row[11] or None
