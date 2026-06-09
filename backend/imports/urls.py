from django.urls import path

from backend.imports.canteen_create import CanteensCreateImportView
from backend.imports.canteen_managers import CanteensManagersImportView
from backend.imports.canteen_update import CanteensUpdateImportView
from backend.imports.diagnostic import DiagnosticsCompleteImportView, DiagnosticsSimpleImportView
from backend.imports.purchase import PurchasesImportView

urlpatterns = [
    path("importPurchases/", PurchasesImportView.as_view(), name="purchases_import"),
    path("importCanteens/create/", CanteensCreateImportView.as_view(), name="canteens_create_import"),
    path("importCanteens/update/", CanteensUpdateImportView.as_view(), name="canteens_update_import"),
    path("importCanteensManagers/", CanteensManagersImportView.as_view(), name="canteens_managers_import"),
    path("importDiagnostics/simple/", DiagnosticsSimpleImportView.as_view(), name="diagnostics_simple_import"),
    path("importDiagnostics/complete/", DiagnosticsCompleteImportView.as_view(), name="diagnostics_complete_import"),
]
