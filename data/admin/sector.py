from django.contrib import admin
from django.template.response import TemplateResponse

from data.models.sector import Sector, SectorCategory, get_sector_category_from_sector, is_sector_with_line_ministry


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
    category = request.GET.get("category", "")
    has_line_ministry = request.GET.get("has_line_ministry", "")

    rows = _build_sector_textchoices_rows()

    if category:
        rows = [row for row in rows if row["category"] == category]

    if has_line_ministry in {"true", "false"}:
        expected_value = has_line_ministry == "true"
        rows = [row for row in rows if row["has_line_ministry"] == expected_value]

    rows = sorted(rows, key=lambda row: (row["category_label"], row["label"]))

    context = {
        **admin.site.each_context(request),
        "title": "Secteurs d'activité",
        "rows": rows,
        "category_choices": SectorCategory.choices,
        "selected_has_line_ministry": has_line_ministry,
        "total_count": len(rows),
    }
    return TemplateResponse(request, "admin/data/sector_textchoices.html", context)
