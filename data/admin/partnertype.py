from collections import Counter
from urllib.parse import urlencode

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import reverse

from data.models import Partner, PartnerType


def _build_partnertype_textchoices_rows():
    # Build counts once from all partners to avoid one query per type value.
    partner_type_counts = Counter()
    for type_list in Partner.objects.values_list("type_list", flat=True):
        for partner_type_value in type_list or []:
            partner_type_counts[partner_type_value] += 1

    rows = []
    for value, label in PartnerType.choices:
        partner_changelist_url = f"{reverse('admin:data_partner_changelist')}?{urlencode({'type_list': value})}"
        rows.append(
            {
                "label": label,
                "value": value,
                "partner_count": partner_type_counts.get(value, 0),
                "partner_changelist_url": partner_changelist_url,
            }
        )
    return rows


def partnertype_textchoices_admin_view(request):
    rows = _build_partnertype_textchoices_rows()

    context = {
        **admin.site.each_context(request),
        "title": "Partenaires : types d'acteur (TextChoices)",
        "rows": rows,
    }
    return TemplateResponse(request, "admin/data/partnertype_textchoices.html", context)
