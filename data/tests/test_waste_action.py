from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase

from data.factories import WasteActionFactory
from data.models import WasteAction

WASTE_ACTION = {
    "title": "Action 1",
    "description": "Description",
    "effort": WasteAction.Effort.SMALL,
    "waste_origins": [WasteAction.WasteOrigin.PREP],
}

WASTE_ACTION_REQUIRED_FIELDS = ["title", "description", "effort", "waste_origins"]


class WasteActionModelSaveTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_waste_action_validation(self):
        # NOT OK: missing required field
        for required_field in WASTE_ACTION_REQUIRED_FIELDS:
            WASTE_ACTION_WITHOUT_REQUIRED_FIELD = WASTE_ACTION | {required_field: None}
            self.assertRaises(ValidationError, WasteActionFactory, **WASTE_ACTION_WITHOUT_REQUIRED_FIELD)
        # OK: all required fields passed (subtitle can be empty)
        WasteActionFactory(**WASTE_ACTION)


class WasteActionModelPropertiesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_effort_display(self):
        waste_action = WasteActionFactory(effort=WasteAction.Effort.SMALL)
        self.assertEqual(waste_action.effort_display(), "Petit pas")

    def test_waste_origins_display(self):
        waste_action = WasteActionFactory(
            waste_origins=[WasteAction.WasteOrigin.PREP, WasteAction.WasteOrigin.UNSERVED]
        )
        self.assertEqual(waste_action.waste_origins_display(), "Préparation, Non servi")

    def test_has_lead_image(self):
        waste_action = WasteActionFactory(lead_image=None)
        self.assertEqual(waste_action.has_lead_image(), "Non")
