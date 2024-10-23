from django.core.exceptions import ValidationError
from django.test import TestCase

from data.factories import (
    CanteenFactory,
    ResourceActionFactory,
    UserFactory,
    WasteActionFactory,
)
from data.models import ResourceAction


class ResourceActionQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        cls.canteen = CanteenFactory()
        cls.canteen_with_manager = CanteenFactory(managers=[cls.user_with_canteen])
        cls.waste_action = WasteActionFactory()
        ResourceActionFactory(resource=cls.waste_action, canteen=cls.canteen, is_done=True)
        ResourceActionFactory(resource=cls.waste_action, canteen=cls.canteen_with_manager, is_done=True)

    def test_for_user_canteens(self):
        self.assertEqual(ResourceAction.objects.count(), 2)
        self.assertEqual(ResourceAction.objects.for_user_canteens(self.user).count(), 0)
        self.assertEqual(ResourceAction.objects.for_user_canteens(self.user_with_canteen).count(), 1)


class ResourceActionModelSaveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user])
        cls.waste_action = WasteActionFactory()

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
