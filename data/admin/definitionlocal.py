from collections import Counter
from urllib.parse import urlencode

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse

from data.models import Purchase
from data.models.definitionlocal import DefinitionLocal


def _build_definitionlocal_textchoices_rows():
    # Build counts once from all purchases to avoid one query per choice value.
    value_counts = Counter(value for value in Purchase.objects.values_list("definition_local", flat=True) if value)
    rows = []
    for value, label in DefinitionLocal.choices:
        purchase_changelist_url = (
            f"{reverse('admin:data_purchase_changelist')}?{urlencode({'definition_local': value})}"
        )
        rows.append(
            {
                "label": label,
                "value": value,
                "purchase_count": value_counts.get(value, 0),
                "purchase_changelist_url": purchase_changelist_url,
            }
        )
    return rows


def definitionlocal_textchoices_admin_view(request):
    rows = _build_definitionlocal_textchoices_rows()

    context = {
        **admin.site.each_context(request),
        "title": "Définition du local (TextChoices)",
        "rows": rows,
    }
    return TemplateResponse(request, "admin/data/definitionlocal_textchoices.html", context)
