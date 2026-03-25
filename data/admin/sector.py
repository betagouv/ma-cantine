from collections import Counter
from urllib.parse import urlencode

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse

from data.models import Canteen
from data.models.sector import Sector, get_sector_category_from_sector, is_sector_with_line_ministry


def _build_sector_textchoices_rows():
    # Build counts once from all canteens to avoid one query per sector value.
    sector_counts = Counter()
    for sector_list in Canteen.objects.values_list("sector_list", flat=True):
        for sector_value in sector_list or []:
            sector_counts[sector_value] += 1

    rows = []
    for value, label in Sector.choices:
        category = get_sector_category_from_sector(value)
        canteen_changelist_url = f"{reverse('admin:data_canteen_changelist')}?{urlencode({'sector_list': value})}"
        rows.append(
            {
                "label": label,
                "value": value,
                "category": category,
                "category_label": category.label,
                "has_line_ministry": is_sector_with_line_ministry(value),
                "canteen_count": sector_counts.get(value, 0),
                "canteen_changelist_url": canteen_changelist_url,
            }
        )
    return rows


def sector_textchoices_admin_view(request):
    rows = _build_sector_textchoices_rows()

    rows = sorted(rows, key=lambda row: (row["category_label"], row["label"]))

    context = {
        **admin.site.each_context(request),
        "title": "Secteurs d'activité (TextChoices)",
        "rows": rows,
    }
    return TemplateResponse(request, "admin/data/sector_textchoices.html", context)
