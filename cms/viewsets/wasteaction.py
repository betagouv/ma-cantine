from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import TabbedInterface, ObjectList, FieldPanel
from wagtail.images.api.v2.views import BaseAPIViewSet
from djangorestframework_camel_case.render import CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer
from data.models.wasteaction import WasteAction
from cms.filtersets.wasteaction import WasteActionFilterSet


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
    list_display = ["title", "modification_date"]
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


class WasteActionAPIViewSet(BaseAPIViewSet):
    """
    API endpoint that allows WasteActions to be viewed.
    """

    renderer_classes = [CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer]
    model = WasteAction
    body_fields = [
        "id",
        "creation_date",
        "modification_date",
        "title",
        "subtitle",
        "effort",
        "waste_origins",
        "description",
        "lead_image",
    ]
    meta_fields = []
