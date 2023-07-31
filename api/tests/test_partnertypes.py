from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PartnerTypeFactory


class TestPartnerTypeApi(APITestCase):
    def test_get_partner_types(self):
        """
        The API should return all partner types
        """
        PartnerTypeFactory.create()
        PartnerTypeFactory.create()
        PartnerTypeFactory.create()

        response = self.client.get(reverse("partner_types_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
