from django import forms
from django.contrib import admin
from data.models import VideoTutorial


class VideoTutorialForm(forms.ModelForm):
    class Meta:
        widgets = {
            "title": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "description": forms.Textarea(attrs={"cols": 55, "rows": 4}),
        }


@admin.register(VideoTutorial)
class VideoTutorial(admin.ModelAdmin):
    form = VideoTutorialForm

    list_display = (
        "title",
        "description",
        "published",
        "creation_date",
        "modification_date",
    )
