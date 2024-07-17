from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import TabbedInterface, ObjectList, FieldPanel, MultipleChooserPanel
from cms.models.actionsheet import ActionSheet
from django import forms


class ActionSheetViewSet(SnippetViewSet):
    """
    This viewset allows using actionsheets on wagtail admin.
    """
    model = ActionSheet
    icon = "doc-full"
    menu_label = "Fiches action"
    menu_name = "actionsheets"
    menu_order = 000
    add_to_admin_menu = True
    edit_handler = TabbedInterface([
        ObjectList([FieldPanel("title"), FieldPanel("subtitle"), FieldPanel("description")], heading="Description"),
        ObjectList([FieldPanel("effort"), FieldPanel("waste_origin"), FieldPanel("savings_estimation"), FieldPanel("coefficient")], heading="Caractéristiques"),
        ObjectList([FieldPanel("image")], heading="Illustration"),
    ])
    list_display = ["title", "modification_date"]