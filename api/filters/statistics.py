import django_filters

from data.models import Canteen


class StatisticsFilterSet(django_filters.FilterSet):
    year = django_filters.NumberFilter(
        field_name="year", lookup_expr="exact", required=True, help_text="Filter by year of declared data"
    )
    region = django_filters.MultipleChoiceFilter(
        field_name="region", lookup_expr="in", help_text="Filter by region(s), using their Insee code"
    )
    department = django_filters.MultipleChoiceFilter(
        field_name="department", lookup_expr="in", help_text="Filter by department(s), using their Insee code"
    )
    epci = django_filters.MultipleChoiceFilter(
        field_name="epci", lookup_expr="in", help_text="Filter by EPCI(s), using their Insee code"
    )
    pat = django_filters.MultipleChoiceFilter(
        field_name="pat_list", lookup_expr="overlap", help_text="Filter by PAT(s), using their id"
    )
    sectors = django_filters.MultipleChoiceFilter(
        field_name="sectors", lookup_expr="in", help_text="Filter by sector(s), using their internal id"
    )

    class Meta:
        model = Canteen
        fields = []
