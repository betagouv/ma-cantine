from django_filters import rest_framework as django_filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination

from api.filters.utils import UnaccentSearchFilter
from api.serializers import WasteActionSerializer, WasteActionWithActionsSerializer
from data.models import WasteAction


class WasteActionPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 100


class WasteActionFilterSet(django_filters.FilterSet):
    effort = django_filters.MultipleChoiceFilter(choices=WasteAction.Effort)
    waste_origins = django_filters.MultipleChoiceFilter(choices=WasteAction.WasteOrigin, lookup_expr="icontains")

    class Meta:
        model = WasteAction
        fields = ["effort", "waste_origins"]


class WasteActionsView(ListAPIView):
    model = WasteAction
    queryset = WasteAction.objects.all()
    serializer_class = WasteActionSerializer
    pagination_class = WasteActionPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
    ]
    filterset_class = WasteActionFilterSet
    search_fields = ["title", "subtitle"]


class WasteActionView(RetrieveAPIView):
    model = WasteAction
    queryset = WasteAction.objects.all()
    serializer_class = WasteActionSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("context", self.get_serializer_context())
        if self.request.user.is_authenticated:
            return WasteActionWithActionsSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
