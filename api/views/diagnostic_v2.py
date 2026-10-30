from api.permissions import IsAuthenticated, IsCanteenManagerUrlParam
from api.serializers import (
    DiagnosticVoletApprovisionnementV2Serializer,
    DiagnosticVoletDiversificationV2Serializer,
    DiagnosticVoletGaspillageV2Serializer,
    DiagnosticVoletInformationV2Serializer,
    DiagnosticVoletPlastiqueV2Serializer,
    DiagnosticV2Serializer,
)
from api.views.diagnostic import DiagnosticListCreateView, DiagnosticRetrieveUpdateView

# internal only for now (no OAuth2, so hidden from the API docs, see api.hooks)
# until the field names are stable
PERMISSION_CLASSES = [IsAuthenticated, IsCanteenManagerUrlParam]


class DiagnosticV2ListCreateView(DiagnosticListCreateView):
    permission_classes = PERMISSION_CLASSES
    serializer_class = DiagnosticV2Serializer


class DiagnosticV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    permission_classes = PERMISSION_CLASSES
    serializer_class = DiagnosticV2Serializer


class DiagnosticVoletApprovisionnementV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    permission_classes = PERMISSION_CLASSES
    serializer_class = DiagnosticVoletApprovisionnementV2Serializer


class DiagnosticVoletGaspillageV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    permission_classes = PERMISSION_CLASSES
    serializer_class = DiagnosticVoletGaspillageV2Serializer


class DiagnosticVoletDiversificationV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    permission_classes = PERMISSION_CLASSES
    serializer_class = DiagnosticVoletDiversificationV2Serializer


class DiagnosticVoletPlastiqueV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    permission_classes = PERMISSION_CLASSES
    serializer_class = DiagnosticVoletPlastiqueV2Serializer


class DiagnosticVoletInformationV2RetrieveUpdateView(DiagnosticRetrieveUpdateView):
    permission_classes = PERMISSION_CLASSES
    serializer_class = DiagnosticVoletInformationV2Serializer
