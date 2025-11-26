from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CanteenFactory, ResourceActionFactory, UserFactory, WasteActionFactory
from data.models import WasteAction


class TestWasteActionsListApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()

    def test_get_waste_actions_list(self):
        response = self.client.get(reverse("waste_actions_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class TestWasteActionsListFiltersApi(APITestCase):
    def test_effort_filter(self):
        WasteActionFactory(effort=WasteAction.Effort.LARGE)
        WasteActionFactory(effort=WasteAction.Effort.MEDIUM)
        WasteActionFactory(effort=WasteAction.Effort.SMALL)

        response = self.client.get(
            f"{reverse('waste_actions_list')}?effort={WasteAction.Effort.SMALL}&effort={WasteAction.Effort.MEDIUM}"
        )
        results = response.data["results"]
        self.assertEqual(len(results), 2)

    def test_origin_filter(self):
        WasteActionFactory(waste_origins=[WasteAction.WasteOrigin.PLATE])
        WasteActionFactory(waste_origins=[WasteAction.WasteOrigin.PLATE, WasteAction.WasteOrigin.PREP])
        WasteActionFactory(waste_origins=[WasteAction.WasteOrigin.UNSERVED])

        response = self.client.get(
            f"{reverse('waste_actions_list')}?waste_origins={WasteAction.WasteOrigin.PREP}&waste_origins={WasteAction.WasteOrigin.UNSERVED}"
        )
        results = response.data["results"]
        self.assertEqual(len(results), 2)

    def test_text_search(self):
        """
        A text search is carried out on title and subtitle, ignoring casing and accents
        """
        WasteActionFactory(title="Évaluation de travail", subtitle="Du texte")
        WasteActionFactory(title="Du texte", subtitle="Faire une évaluation")
        WasteActionFactory(title="Autre texte", subtitle="Ne m'évalue pas")

        response = self.client.get(f"{reverse('waste_actions_list')}?search=evaluation")
        results = response.data["results"]
        self.assertEqual(len(results), 2)


class TestWasteActionsDetailApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        CanteenFactory()
        cls.canteen = CanteenFactory(managers=[cls.user_with_canteen])
        cls.resource_action = ResourceActionFactory(resource=cls.waste_action, canteen=cls.canteen, is_done=True)

    def test_get_waste_action_detail(self):
        # anonymous
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.waste_action.id)
        self.assertTrue("canteenActions" not in body)
        # logged in user (without canteen)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.waste_action.id)
        self.assertTrue("canteenActions" in body)
        self.assertEqual(len(body["canteenActions"]), 0)
        # logged in user with canteen & resource action
        self.client.force_login(user=self.user_with_canteen)
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.waste_action.id)
        self.assertTrue("canteenActions" in body)
        self.assertEqual(len(body["canteenActions"]), 1)
        self.assertTrue(body["canteenActions"][0]["isDone"])
        self.assertEqual(body["canteenActions"][0]["canteenId"], self.canteen.id)
        self.assertEqual(body["canteenActions"][0]["canteen"]["id"], self.canteen.id)
        self.assertEqual(body["canteenActions"][0]["canteen"]["name"], self.canteen.name)
        self.assertEqual(body["canteenActions"][0]["resourceId"], self.waste_action.id)
        self.assertEqual(body["canteenActions"][0]["resource"]["id"], self.waste_action.id)
