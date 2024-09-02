from wagtail.admin.filters import WagtailFilterSet
from cms.models import WasteAction


class WasteActionFilterSet(WagtailFilterSet):
    class Meta:
        model = WasteAction
        fields = ["effort"]
