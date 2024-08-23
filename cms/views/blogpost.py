from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import TabbedInterface, ObjectList, FieldPanel
from data.models import BlogPost


class BlogPostViewSet(SnippetViewSet):
    """
    This viewset allows using blog posts on wagtail admin.
    """

    model = BlogPost
    icon = "doc-full"
    menu_label = "Articles de blog"
    menu_name = "blogposts"
    menu_order = 90
    add_to_admin_menu = True
    edit_handler = TabbedInterface(
        [
            ObjectList([FieldPanel("title"), FieldPanel("tagline"), FieldPanel("body")], heading="Description"),
            ObjectList(
                [
                    FieldPanel("published"),
                    FieldPanel("author"),
                    FieldPanel("tags"),
                    FieldPanel("display_date"),
                ],
                heading="Méta données",
            ),
        ]
    )
    list_display = ["title", "modification_date", "published"]
