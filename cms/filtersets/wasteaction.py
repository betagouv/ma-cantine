from wagtail.admin.filters import WagtailFilterSet
from django_filters import CharFilter
from cms.models import WasteAction


class WasteActionFilterSet(WagtailFilterSet):
    title = CharFilter(lookup_expr="icontains")

    class Meta:
        model = WasteAction
        fields = ["effort"]
