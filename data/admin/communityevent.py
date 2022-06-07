from django import forms
from django.contrib import admin
from data.models import CommunityEvent


class CommunityEventForm(forms.ModelForm):
    class Meta:
        widgets = {
            "title": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "tagline": forms.Textarea(attrs={"cols": 65, "rows": 3}),
            "link": forms.Textarea(attrs={"cols": 70, "rows": 1}),
        }


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
