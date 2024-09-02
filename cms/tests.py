from django.test import TransactionTestCase
from django.core.exceptions import ValidationError
from .models import WasteAction
from .factories import WasteActionFactory


WASTE_ACTION = {
    "title": "Action 1",
    "description": "Description",
    "effort": WasteAction.Effort.SMALL,
    "waste_origins": [WasteAction.WasteOrigin.PREP],
}


class WasteActionModelSaveTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_waste_action_validation(self):
        # NOT OK: missing required field
        for REQUIRED_FIELD in ["title", "description", "effort", "waste_origins"]:
            WASTE_ACTION_WITHOUT_REQUIRED_FIELD = WASTE_ACTION | {REQUIRED_FIELD: None}
            self.assertRaises(ValidationError, WasteActionFactory, **WASTE_ACTION_WITHOUT_REQUIRED_FIELD)
        # OK: all required fields passed
        WasteActionFactory(**WASTE_ACTION)
        # OK: subtitle can be empty
        WASTE_ACTION_WITHOUT_SUBTITLE = WASTE_ACTION | {"subtitle": None}
        WasteActionFactory(**WASTE_ACTION_WITHOUT_SUBTITLE)
