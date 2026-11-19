from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.models import PartnerType


class TestPartnerTypeApi(APITestCase):
    def test_get_partner_types(self):
        """
        The API should return all partner types (from the enum)
        """
        response = self.client.get(reverse("partner_types_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), len(PartnerType))
        self.assertEqual(body[0], {"id": "logiciel", "name": "Logiciels / outils numériques"})
