from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from data.models import WasteAction
from api.serializers import WasteActionSerializer


class WasteActionPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 100


class WasteActionsView(ListAPIView):
    model = WasteAction
    serializer_class = WasteActionSerializer
    pagination_class = WasteActionPagination
    queryset = WasteAction.objects.all()
