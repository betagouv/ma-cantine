from django.test import TransactionTestCase
from django.db.utils import IntegrityError
from .models import WasteAction


class WasteActionModelSaveTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_waste_action_validation(self):
        # NOT OK : waste_origins is required
        self.assertRaises(IntegrityError, WasteAction.objects.create, title="Action 1")
        # OK
        WasteAction.objects.create(title="Action 1", subtitle=None, waste_origins=[WasteAction.WasteOrigin.PREP])
