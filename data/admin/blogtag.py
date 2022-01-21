from django import forms
from django.contrib import admin
from data.models import BlogTag


class BlogTagForm(forms.ModelForm):
    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"cols": 35, "rows": 1}),
        }


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):

    form = BlogTagForm
    fields = ("name",)
    list_display = (
        "name",
        "creation_date",
    )
    list_filter = ("name",)
