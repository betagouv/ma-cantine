from django import forms
from django.contrib import admin

from data.models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        widgets = {
            "title": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "tagline": forms.Textarea(attrs={"cols": 65, "rows": 3}),
        }


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "display_date",
        "author",
        "published_state",
    )
    list_filter = ("published",)

    form = BlogPostForm
    filter_vertical = ("tags",)
    fields = (
        "title",
        "tagline",
        "display_date",
        "published",
        "author",
        "body",
        "tags",
    )

    def published_state(self, obj):
        return "✅ Publié" if obj.published else "🔒 Non publié"
