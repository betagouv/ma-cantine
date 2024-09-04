from django import forms
from wagtail.admin.filters import WagtailFilterSet
from django_filters import CharFilter, MultipleChoiceFilter
from cms.models import WasteAction


class WasteActionFilterSet(WagtailFilterSet):
    title = CharFilter(lookup_expr="icontains")
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
