from django.core.exceptions import ValidationError
from django.test import TestCase

from data.factories import (
    CanteenFactory,
    ResourceActionFactory,
    UserFactory,
    WasteActionFactory,
)


class ResourceActionModelSaveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.user = UserFactory()
        cls.canteen = CanteenFactory()
        cls.canteen.managers.add(cls.user)

    def test_resource_action_validation(self):
        # NOT OK: missing required field
        self.assertRaises(ValidationError, ResourceActionFactory)
        self.assertRaises(ValidationError, ResourceActionFactory, resource=self.waste_action)
        # OK: all required fields passed
        ResourceActionFactory(resource=self.waste_action, canteen=self.canteen)
        # resource & canteen unique together
        self.assertRaises(
            ValidationError, ResourceActionFactory, resource=self.waste_action, canteen=self.canteen, is_done=True
        )
