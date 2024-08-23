from wagtail.snippets.models import register_snippet
from .views import WasteActionViewSet, BlogPostViewSet

register_snippet(WasteActionViewSet)
register_snippet(BlogPostViewSet)
