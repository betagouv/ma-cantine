from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, ResourceActionFactory, UserFactory, WasteActionFactory
from data.models import WasteAction


class WasteActionsListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.url = reverse("waste_actions_list")

    def test_get_waste_actions_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class WasteActionsListFiltersApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("waste_actions_list")

    def test_effort_filter(self):
        WasteActionFactory(effort=WasteAction.Effort.LARGE)
        WasteActionFactory(effort=WasteAction.Effort.MEDIUM)
        WasteActionFactory(effort=WasteAction.Effort.SMALL)

        url = f"{self.url}?effort={WasteAction.Effort.SMALL}&effort={WasteAction.Effort.MEDIUM}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 2)

    def test_origin_filter(self):
        WasteActionFactory(waste_origins=[WasteAction.WasteOrigin.PLATE])
        WasteActionFactory(waste_origins=[WasteAction.WasteOrigin.PLATE, WasteAction.WasteOrigin.PREP])
        WasteActionFactory(waste_origins=[WasteAction.WasteOrigin.UNSERVED])

        url = (
            f"{self.url}?waste_origins={WasteAction.WasteOrigin.PREP}&waste_origins={WasteAction.WasteOrigin.UNSERVED}"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 2)

    def test_text_search(self):
        """
        A text search is carried out on title and subtitle, ignoring casing and accents
        """
        WasteActionFactory(title="Évaluation de travail", subtitle="Du texte")
        WasteActionFactory(title="Du texte", subtitle="Faire une évaluation")
        WasteActionFactory(title="Autre texte", subtitle="Ne m'évalue pas")

        url = f"{self.url}?search=évaluation"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 2)


class WasteActionsDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        CanteenFactory()
        cls.canteen = CanteenFactory(managers=[cls.user_with_canteen])
        cls.resource_action = ResourceActionFactory(resource=cls.waste_action, canteen=cls.canteen, is_done=True)
        cls.url = reverse("waste_action_detail", kwargs={"pk": cls.waste_action.id})

    def test_can_get_waste_action_detail_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.waste_action.id)
        self.assertTrue("canteenActions" not in body)

    @authenticate
    def test_get_waste_action_detail(self):
        # logged in user (without canteen)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.waste_action.id)
        self.assertTrue("canteenActions" in body)
        self.assertEqual(len(body["canteenActions"]), 0)

        # logged in user with canteen & resource action
        self.canteen.managers.add(authenticate.user)
        response = self.client.get(self.url)

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
