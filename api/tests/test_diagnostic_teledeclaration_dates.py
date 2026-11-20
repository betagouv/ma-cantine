from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from common.tests.utils import date_before_campaign, date_in_campaign, date_in_campaign_correction


class TeledeclarationCampaignDatesListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("list_teledeclaration_campaign_dates")

    def test_campaign_dates_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 6)
        self.assertEqual(body[-1]["year"], 2026)


class TeledeclarationCampaignDatesRetrieveApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("retrieve_teledeclaration_campaign_dates", kwargs={"year": 2024})

    def test_campaign_dates_retrieve(self):
        for date_freeze in [
            {"date": date_before_campaign(2024), "in_teledeclaration": False, "in_correction": False},
            {"date": date_in_campaign(2024), "in_teledeclaration": True, "in_correction": False},
            {"date": date_in_campaign_correction(2024), "in_teledeclaration": False, "in_correction": True},
        ]:
            with self.subTest(DATE=date_freeze["date"]):
                with freeze_time(date_freeze["date"]):
                    response = self.client.get(self.url)

                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    body = response.json()
                    self.assertEqual(body["year"], 2024)
                    self.assertEqual(body["inTeledeclaration"], date_freeze["in_teledeclaration"])
                    self.assertEqual(body["inCorrection"], date_freeze["in_correction"])
