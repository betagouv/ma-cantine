from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import TabbedInterface, ObjectList, FieldPanel
from cms.models.wasteaction import WasteAction
from wagtail.images.api.v2.views import BaseAPIViewSet


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
                ],
                heading="Caractéristiques",
            ),
            ObjectList([FieldPanel("lead_image")], heading="Illustration"),
        ]
    )
    list_display = ["title", "modification_date"]


class WasteActionAPIViewSet(BaseAPIViewSet):
    """
    API endpoint that allows WasteActions to be viewed.
    """

    model = WasteAction
    api_fields = [
        "id",
        "creation_date",
        "modification_date",
        "title",
        "subtitle",
        "effort",
        "waste_origin",
        "description",
        "lead_image",
    ]
    body_fields = BaseAPIViewSet.body_fields + api_fields
    # If needed we can list all those fields by default. Otherwise we can see them by adding "?fields=*" to URL
    # listing_default_fields = BaseAPIViewSet.listing_default_fields + api_fields
