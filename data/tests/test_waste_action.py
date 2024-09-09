from django.test import TransactionTestCase
from django.core.exceptions import ValidationError
from data.models.wasteaction import WasteAction
from data.factories.wasteaction import WasteActionFactory


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
