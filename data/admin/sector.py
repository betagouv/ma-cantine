from django.contrib import admin
from django.template.response import TemplateResponse

from data.models.sector import Sector, get_sector_category_from_sector, is_sector_with_line_ministry


def _build_sector_textchoices_rows():
    rows = []
    for value, label in Sector.choices:
        category = get_sector_category_from_sector(value)
        rows.append(
            {
                "label": label,
                "value": value,
                "category": category,
                "category_label": category.label,
                "has_line_ministry": is_sector_with_line_ministry(value),
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
