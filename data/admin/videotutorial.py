from django import forms
from django.contrib import admin
from data.models import VideoTutorial


class VideoTutorialForm(forms.ModelForm):
    class Meta:
        widgets = {
            "title": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "description": forms.Textarea(attrs={"cols": 55, "rows": 4}),
        }


class AccessibilityStatusFilter(admin.SimpleListFilter):
    title = "statut d'accessibilité"
    parameter_name = "a11y"

    def lookups(self, request, model_admin):
        return (
            ("ACCESSIBLE", "✅ Accessible"),
            ("MISSING_SUBTITLES", "🛑 Sous-titres manquants"),
        )

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
            return queryset
        elif self.value() in ("ACCESSIBLE"):
            return queryset.filter(subtitles__isnull=False)
        elif self.value() in ("MISSING_SUBTITLES"):
            return queryset.filter(subtitles__isnull=True)


@admin.register(VideoTutorial)
class VideoTutorial(admin.ModelAdmin):
    form = VideoTutorialForm

    list_display = (
        "title",
        "description",
        "published",
        "sous_titré",
        "creation_date",
        "modification_date",
    )

    list_filter = (AccessibilityStatusFilter,)
