from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from data.models import WasteAction
from api.serializers import WasteActionSerializer
from django_filters import rest_framework as django_filters


class WasteActionPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 100


class WasteActionsView(ListAPIView):
    model = WasteAction
    queryset = WasteAction.objects.all()
    serializer_class = WasteActionSerializer
    pagination_class = WasteActionPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
    ]
    filterset_fields = {"effort": ["in"]}


class WasteActionView(RetrieveAPIView):
    model = WasteAction
    queryset = WasteAction.objects.all()
    serializer_class = WasteActionSerializer
