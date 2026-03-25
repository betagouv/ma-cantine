from collections import Counter
from urllib.parse import urlencode

from django.contrib import admin
from django.http import Http404
from django.template.response import TemplateResponse
from django.urls import reverse

from data.models import Canteen
from data.models.creation_source import CreationSource

CANTEEN_TEXTCHOICES_PAGES = [
    {
        "key": "canteen-management-type",
        "title": "Cantines : modes de gestion (TextChoices)",
        "object_name": "CanteenManagementTypeTextChoices",
        "field_name": "management_type",
        "choices": Canteen.ManagementType.choices,
    },
    {
        "key": "canteen-production-type",
        "title": "Cantines : modes de production (TextChoices)",
        "object_name": "CanteenProductionTypeTextChoices",
        "field_name": "production_type",
        "choices": Canteen.ProductionType.choices,
    },
    {
        "key": "canteen-economic-model",
        "title": "Cantines : modèles économiques (TextChoices)",
        "object_name": "CanteenEconomicModelTextChoices",
        "field_name": "economic_model",
        "choices": Canteen.EconomicModel.choices,
    },
    {
        "key": "canteen-line-ministry",
        "title": "Cantines : administrations de tutelle (TextChoices)",
        "object_name": "CanteenLineMinistryTextChoices",
        "field_name": "line_ministry",
        "choices": Canteen.Ministries.choices,
    },
    {
        "key": "canteen-creation-source",
        "title": "Cantines : source de création (TextChoices)",
        "object_name": "CanteenCreationSourceTextChoices",
        "field_name": "creation_source",
        "choices": CreationSource.choices,
    },
]


def _build_canteen_textchoices_rows(field_name, choices):
    # Build counts once from all canteens to avoid one query per choice value.
    value_counts = Counter(value for value in Canteen.objects.values_list(field_name, flat=True) if value)
    rows = []
    for value, label in choices:
        canteen_changelist_url = f"{reverse('admin:data_canteen_changelist')}?{urlencode({field_name: value})}"
        rows.append(
            {
                "label": label,
                "value": value,
                "canteen_count": value_counts.get(value, 0),
                "canteen_changelist_url": canteen_changelist_url,
            }
        )
    return sorted(rows, key=lambda row: row["label"])


def canteen_textchoices_admin_view(request, page_key):
    page = next((page for page in CANTEEN_TEXTCHOICES_PAGES if page["key"] == page_key), None)
    if not page:
        raise Http404("Unknown canteen TextChoices page")

    rows = _build_canteen_textchoices_rows(page["field_name"], page["choices"])

    context = {
        **admin.site.each_context(request),
        "title": page["title"],
        "rows": rows,
        "field_name": page["field_name"],
    }
    return TemplateResponse(request, "admin/data/canteen_textchoices.html", context)
