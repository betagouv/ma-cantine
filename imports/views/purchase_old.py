from imports.schemas import ImportSchema
from imports.views.purchase_base import BasePurchasesImportView


PURCHASE_SIRET_SCHEMA = ImportSchema("achats_siret_old.json")
PURCHASE_ID_SCHEMA = ImportSchema("achats_id_old.json")


class PurchasesImportOldView(BasePurchasesImportView):
    siret_schema = PURCHASE_SIRET_SCHEMA
    id_schema = PURCHASE_ID_SCHEMA

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
