from .diagnostic import FullDiagnosticSerializer
from .canteen import FullCanteenSerializer
from data.models import Diagnostic


class DiagnosticAndCanteenSerializer(FullDiagnosticSerializer):
    canteen = FullCanteenSerializer(read_only=True)

    class Meta:
        model = Diagnostic
        fields = tuple(FullDiagnosticSerializer().fields) + ("canteen",)
