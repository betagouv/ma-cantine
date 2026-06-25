from django.conf import settings

from api.views.purchase_import_base import BasePurchasesImportView


PURCHASE_SIRET_SCHEMA_FILE_NAME = "achats_siret_old.json"
PURCHASE_SIRET_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_SIRET_SCHEMA_FILE_NAME}"
PURCHASE_SIRET_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_SIRET_SCHEMA_FILE_PATH}"
PURCHASE_ID_SCHEMA_FILE_NAME = "achats_id_old.json"
PURCHASE_ID_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_ID_SCHEMA_FILE_NAME}"
PURCHASE_ID_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_ID_SCHEMA_FILE_PATH}"


class PurchasesImportOldView(BasePurchasesImportView):
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
        return [c.strip() for c in row[6].split(",")] if row[6] else []

    def _get_definition_local(self, row):
        definition_local = row[7].strip() if row[7] else None
        if definition_local in ["AUTOUR_SERVICE", "AUTRE"]:
            return "KM"
        return definition_local

    def _get_definition_local_km(self, row):
        definition_local = row[7].strip() if row[7] else None
        if definition_local == "AUTOUR_SERVICE":
            return "200"
        return None
