from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import TabbedInterface, ObjectList, FieldPanel
from cms.models.wasteaction import WasteAction


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
    edit_handler = TabbedInterface(
        [
            ObjectList(
                [FieldPanel("title"), FieldPanel("subtitle"), FieldPanel("description")], heading="Description"
            ),
            ObjectList(
                [
                    FieldPanel("effort"),
                    FieldPanel("waste_origin"),
                    # FieldPanel("savings_estimation"),
                    # FieldPanel("coefficient"),
                ],
                heading="Caractéristiques",
            ),
            ObjectList([FieldPanel("lead_image")], heading="Illustration"),
        ]
    )
    list_display = ["title", "modification_date"]
