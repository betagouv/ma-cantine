from django.urls import reverse
from rest_framework.test import APITestCase

from data.factories import WasteActionFactory
from data.models import WasteAction


class TestWasteActionsApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory.create()

    def test_get_waste_actions_list(self):
        response = self.client.get(reverse("waste_actions_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_waste_action_detail(self):
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.waste_action.id)


class TestWasteActionsFiltersApi(APITestCase):
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
