from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.snippets.views.snippets import SnippetViewSet

from cms.filtersets.wasteaction import WasteActionFilterSet
from data.models import WasteAction


class WasteActionViewSet(SnippetViewSet):
    """
    This viewset allows using wasteactions on wagtail admin.
    """

    model = WasteAction
    icon = "doc-full"
    menu_label = "Actions anti-gaspi"
    menu_name = "wasteactions"
    menu_order = 90
    add_to_admin_menu = True
    filterset_class = WasteActionFilterSet
    list_display = [
        "title",
        "effort_display",
        "waste_origins_display",
        "has_lead_image",
        "creation_date",
        "modification_date",
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(
                [FieldPanel("title"), FieldPanel("subtitle"), FieldPanel("description")], heading="Description"
            ),
            ObjectList(
                [
                    FieldPanel("effort"),
                    FieldPanel("waste_origins"),
                ],
                heading="Caractéristiques",
            ),
            ObjectList([FieldPanel("lead_image")], heading="Illustration"),
        ]
    )
