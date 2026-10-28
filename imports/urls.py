from django.urls import path

from imports.views.canteen_create import CanteensCreateImportView
from imports.views.canteen_managers import CanteensManagersImportView
from imports.views.canteen_update import CanteensUpdateImportView
from imports.views.diagnostic import DiagnosticsCompleteImportView, DiagnosticsSimpleImportView
from imports.views.purchase import PurchasesImportView
from imports.views.purchase_old import PurchasesImportOldView

urlpatterns = [
    path("importPurchases/", PurchasesImportView.as_view(), name="purchases_import"),
    path("importPurchasesOld/", PurchasesImportOldView.as_view(), name="purchases_import_old"),
    path("importCanteens/create/", CanteensCreateImportView.as_view(), name="canteens_create_import"),
    path("importCanteens/update/", CanteensUpdateImportView.as_view(), name="canteens_update_import"),
    path("importCanteensManagers/", CanteensManagersImportView.as_view(), name="canteens_managers_import"),
    path("importDiagnostics/simple/", DiagnosticsSimpleImportView.as_view(), name="diagnostics_simple_import"),
    path("importDiagnostics/complete/", DiagnosticsCompleteImportView.as_view(), name="diagnostics_complete_import"),
]
