from django import forms
from django_filters import CharFilter, MultipleChoiceFilter
from wagtail.admin.filters import WagtailFilterSet

from data.models import WasteAction


class WasteActionFilterSet(WagtailFilterSet):
    title = CharFilter(label="Titre contient", lookup_expr="unaccent__icontains")
    effort = MultipleChoiceFilter(choices=WasteAction.Effort.choices, widget=forms.CheckboxSelectMultiple)
    waste_origins = MultipleChoiceFilter(
        label=WasteAction._meta.get_field("waste_origins").verbose_name,
        choices=WasteAction.WasteOrigin.choices,
        widget=forms.CheckboxSelectMultiple,
        lookup_expr="icontains",
    )

    class Meta:
        model = WasteAction
        fields = ["title", "effort", "waste_origins"]
