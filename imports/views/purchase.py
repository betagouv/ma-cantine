from data.models import Purchase

from imports.models import ImportSchema
from imports.views.purchase_base import BasePurchasesImportView

PURCHASE_SIRET_SCHEMA = ImportSchema("achats_siret.json")
PURCHASE_ID_SCHEMA = ImportSchema("achats_id.json")


class PurchasesImportView(BasePurchasesImportView):
    siret_schema = PURCHASE_SIRET_SCHEMA
    id_schema = PURCHASE_ID_SCHEMA

    def _get_caracteristiques(self, row_dict):
        categories_egalim = row_dict["categories_egalim"].strip() if row_dict["categories_egalim"] else ""
        origine = row_dict["origine"].strip() if row_dict["origine"] else ""
        est_circuit_court = row_dict["est_circuit_court"].strip().lower() if row_dict["est_circuit_court"] else ""
        est_local = row_dict["est_local"].strip().lower() if row_dict["est_local"] else ""

        egalim_caracteristics = categories_egalim.split(",") if categories_egalim else []
        origine_caracteristics = origine.split(",") if origine else []
        circuit_court_caracteristics = (
            [Purchase.Characteristic.CIRCUIT_COURT] if self.is_true_value(est_circuit_court) else []
        )
        local_caracteristics = [Purchase.Characteristic.LOCAL] if self.is_true_value(est_local) else []
        return egalim_caracteristics + origine_caracteristics + circuit_court_caracteristics + local_caracteristics

    def _get_definition_local(self, row_dict):
        return row_dict["definition_local"].strip() if row_dict["definition_local"] else ""

    def _get_definition_local_km(self, row_dict):
        return row_dict["definition_local_km"] or None
