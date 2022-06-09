from django import forms
from django.contrib import admin
from django.utils import timezone
from data.models import CommunityEvent


class CommunityEventForm(forms.ModelForm):
    class Meta:
        widgets = {
            "title": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "tagline": forms.Textarea(attrs={"cols": 65, "rows": 3}),
            "link": forms.Textarea(attrs={"cols": 70, "rows": 1}),
        }


class UpcomingEventsFilter(admin.SimpleListFilter):
    title = "date"

    parameter_name = "upcoming_status"

    def lookups(self, request, model_admin):
        return (
            (None, "À venir"),
            ("past", "Passé"),
            ("all", "Tout"),
        )

    # need to override choices otherwise django adds 'all' as the
    # None value choice, whereas in this case None is 'À venir'
    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": cl.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.filter(end_date__gt=timezone.now())
        elif self.value() in ("all"):
            return queryset
        elif self.value() in ("past"):
            return queryset.filter(end_date__lte=timezone.now())


@admin.register(CommunityEvent)
class CommunityEventAdmin(admin.ModelAdmin):

    form = CommunityEventForm
    fields = (
        "title",
        "tagline",
        "start_date",
        "end_date",
        "link",
    )
    list_display = (
        "title",
        "start_date",
    )
    list_filter = (UpcomingEventsFilter,)
