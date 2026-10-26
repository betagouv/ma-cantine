from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (
    DiagnosticVoletApprovisionnementV2RetrieveUpdateView,
    DiagnosticVoletDiversificationV2RetrieveUpdateView,
    DiagnosticVoletGaspillageV2RetrieveUpdateView,
    DiagnosticVoletInformationV2RetrieveUpdateView,
    DiagnosticVoletPlastiqueV2RetrieveUpdateView,
    DiagnosticV2ListCreateView,
    DiagnosticV2RetrieveUpdateView,
)

urlpatterns = [
    path(
        "canteens/<int:canteen_pk>/diagnostics/",
        DiagnosticV2ListCreateView.as_view(),
        name="diagnostic_v2_list_create",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/<int:pk>",
        DiagnosticV2RetrieveUpdateView.as_view(),
        name="diagnostic_v2_retrieve_update",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/<int:pk>/approvisionnements",
        DiagnosticVoletApprovisionnementV2RetrieveUpdateView.as_view(),
        name="diagnostic_v2_approvisionnement_retrieve_update",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/<int:pk>/gaspillage-alimentaire",
        DiagnosticVoletGaspillageV2RetrieveUpdateView.as_view(),
        name="diagnostic_v2_gaspillage_retrieve_update",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/<int:pk>/menus-vegetariens",
        DiagnosticVoletDiversificationV2RetrieveUpdateView.as_view(),
        name="diagnostic_v2_diversification_retrieve_update",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/<int:pk>/substitution-plastique",
        DiagnosticVoletPlastiqueV2RetrieveUpdateView.as_view(),
        name="diagnostic_v2_plastique_retrieve_update",
    ),
    path(
        "canteens/<int:canteen_pk>/diagnostics/<int:pk>/information-convives",
        DiagnosticVoletInformationV2RetrieveUpdateView.as_view(),
        name="diagnostic_v2_information_retrieve_update",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
