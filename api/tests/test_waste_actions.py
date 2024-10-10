from django.urls import reverse
from rest_framework.test import APITestCase

from data.factories import (
    CanteenFactory,
    ResourceActionFactory,
    UserFactory,
    WasteActionFactory,
)
from data.models import WasteAction


class TestWasteActionsListApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory.create()

    def test_get_waste_actions_list(self):
        response = self.client.get(reverse("waste_actions_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)


class TestWasteActionsListFiltersApi(APITestCase):
    def test_effort_filter(self):
        WasteActionFactory.create(effort=WasteAction.Effort.LARGE)
        WasteActionFactory.create(effort=WasteAction.Effort.MEDIUM)
        WasteActionFactory.create(effort=WasteAction.Effort.SMALL)

        response = self.client.get(
            f"{reverse('waste_actions_list')}?effort={WasteAction.Effort.SMALL}&effort={WasteAction.Effort.MEDIUM}"
        )
        results = response.data["results"]
        self.assertEqual(len(results), 2)

    def test_origin_filter(self):
        WasteActionFactory.create(waste_origins=[WasteAction.WasteOrigin.PLATE])
        WasteActionFactory.create(waste_origins=[WasteAction.WasteOrigin.PLATE, WasteAction.WasteOrigin.PREP])
        WasteActionFactory.create(waste_origins=[WasteAction.WasteOrigin.UNSERVED])

        response = self.client.get(
            f"{reverse('waste_actions_list')}?waste_origins={WasteAction.WasteOrigin.PREP}&waste_origins={WasteAction.WasteOrigin.UNSERVED}"
        )
        results = response.data["results"]
        self.assertEqual(len(results), 2)

    def test_text_search(self):
        """
        A text search is carried out on title and subtitle, ignoring casing and accents
        """
        WasteActionFactory.create(title="Évaluation de travail", subtitle="Du texte")
        WasteActionFactory.create(title="Du texte", subtitle="Faire une évaluation")
        WasteActionFactory.create(title="Autre texte", subtitle="Ne m'évalue pas")

        response = self.client.get(f"{reverse('waste_actions_list')}?search=evaluation")
        results = response.data["results"]
        self.assertEqual(len(results), 2)


class TestWasteActionsDetailApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory.create()
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        CanteenFactory()
        cls.canteen = CanteenFactory()
        cls.canteen.managers.add(cls.user_with_canteen)
        cls.resource_action = ResourceActionFactory.create(
            resource=cls.waste_action, canteen=cls.canteen, is_done=True
        )

    def test_get_waste_action_detail(self):
        # anonymous
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.waste_action.id)
        self.assertTrue("actions" not in response.data)
        # logged in user (without canteen)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.waste_action.id)
        self.assertTrue("actions" in response.data)
        self.assertEqual(len(response.data["actions"]), 0)
        # logged in user with canteen & resource action
        self.client.force_login(user=self.user_with_canteen)
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.waste_action.id)
        self.assertTrue("actions" in response.data)
        self.assertEqual(len(response.data["actions"]), 1)
        self.assertEqual(response.data["actions"][0]["canteen_id"], self.canteen.id)
        self.assertEqual(response.data["actions"][0]["canteen"]["id"], self.canteen.id)
        self.assertEqual(response.data["actions"][0]["canteen"]["name"], self.canteen.name)
        self.assertTrue(response.data["actions"][0]["is_done"])
