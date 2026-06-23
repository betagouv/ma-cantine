from django.conf import settings

from data.models import Purchase

from api.views.purchase_import_base import BasePurchasesImportView


PURCHASE_SIRET_SCHEMA_FILE_NAME = "achats_siret.json"
PURCHASE_SIRET_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_SIRET_SCHEMA_FILE_NAME}"
PURCHASE_SIRET_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_SIRET_SCHEMA_FILE_PATH}"
PURCHASE_ID_SCHEMA_FILE_NAME = "achats_id.json"
PURCHASE_ID_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_ID_SCHEMA_FILE_NAME}"
PURCHASE_ID_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_ID_SCHEMA_FILE_PATH}"


class PurchasesImportView(BasePurchasesImportView):
    """Purchases import using the 2026 schema (categories EGalim, origine, local, circuit court)."""

    def _get_schema_config(self):
        if self.is_siret_import:
            return {
                "name": PURCHASE_SIRET_SCHEMA_FILE_NAME,
                "url": PURCHASE_SIRET_SCHEMA_URL,
                "path": PURCHASE_SIRET_SCHEMA_FILE_PATH,
            }
        return {
            "name": PURCHASE_ID_SCHEMA_FILE_NAME,
            "url": PURCHASE_ID_SCHEMA_URL,
            "path": PURCHASE_ID_SCHEMA_FILE_PATH,
        }

    def _get_caracteristiques(self, row):
        boolean_true_values = ["oui", "x"]
        categories_egalim = row[6].strip() if row[6] else ""
        origine = row[7].strip() if row[7] else ""
        est_circuit_court = row[8].strip().lower() if row[8] else ""
        est_local = row[9].strip().lower() if row[9] else ""

        egalim_caracteristics = categories_egalim.split(",") if categories_egalim else []
        origine_caracteristics = origine.split(",") if origine else []
        local_caracteristics = [Purchase.Characteristic.LOCAL] if est_local in boolean_true_values else []
        circuit_court_caracteristics = (
            [Purchase.Characteristic.CIRCUIT_COURT] if est_circuit_court in boolean_true_values else []
        )
        return egalim_caracteristics + origine_caracteristics + local_caracteristics + circuit_court_caracteristics

    def _get_definition_local(self, row):
        est_local = row[9].strip() if row[9] else ""
        definition_local = row[10].strip() if row[10] else ""
        return definition_local if est_local == "x" else ""
