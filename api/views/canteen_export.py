from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListAPIView

from api.permissions import IsAuthenticated
from api.serializers import CanteenExportSerializer


class UserCanteenListExportView(ListAPIView, XLSXFileMixin):
    permission_classes = [IsAuthenticated]
    renderer_classes = (XLSXRenderer,)
    pagination_class = None
    serializer_class = CanteenExportSerializer

    def get_queryset(self):
        # similar to UserCanteenActions
        return self.request.user.canteens.has_siret().order_by("name")

    # same as data/schemas/imports/cantines.json
    column_header = {
        "titles": [
            "siret",
            "nom",
            "siret_cuisine_centrale",
            "nombre_repas_jour",
            "nombre_repas_an",
            "secteurs",
            "type_production",
            "type_gestion",
            "modèle_économique",
            "groupe_id",
            "administration_tutelle",
            "gestionnaires_additionnels",
        ],
        # "column_width": [],
        "style": {
            "font": {
                "bold": True,
            },
        },
    }
    body = {
        "style": {
            "alignment": {
                "horizontal": "left",
                "vertical": "center",
            },
        },
        "height": 20,
    }

    def post(self, request, *args, **kwargs):
        raise MethodNotAllowed()
