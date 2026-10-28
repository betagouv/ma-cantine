from imports.models import ImportSchema
from imports.views.purchase_base import BasePurchasesImportView


PURCHASE_SIRET_SCHEMA = ImportSchema("achats_siret_old.json")
PURCHASE_ID_SCHEMA = ImportSchema("achats_id_old.json")


class PurchasesImportOldView(BasePurchasesImportView):
    siret_schema = PURCHASE_SIRET_SCHEMA
    id_schema = PURCHASE_ID_SCHEMA

    def _get_caracteristiques(self, row_dict):
        return [c.strip() for c in row_dict["caracteristiques"].split(",")] if row_dict["caracteristiques"] else []

    def _get_definition_local(self, row_dict):
        definition_local = row_dict["definition_local"].strip() if row_dict["definition_local"] else None
        if definition_local in ["AUTOUR_SERVICE", "AUTRE"]:
            return "KM"
        return definition_local

    def _get_definition_local_km(self, row_dict):
        definition_local = row_dict["definition_local"].strip() if row_dict["definition_local"] else None
        if definition_local == "AUTOUR_SERVICE":
            return "200"
        return None
