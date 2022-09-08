from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PartnerFactory, PartnerTypeFactory


class TestPartnersApi(APITestCase):
    def test_get_partners(self):
        partners = [
            PartnerFactory.create(),
            PartnerFactory.create(),
        ]
        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body.get("count"), 2)

        results = body.get("results", [])

        for partner in partners:
            self.assertTrue(any(x["id"] == partner.id for x in results))

    def test_get_single_partner(self):
        type = PartnerTypeFactory.create(name="Test type")
        partner = PartnerFactory.create()
        partner.types.add(type)

        response = self.client.get(reverse("single_partner", kwargs={"pk": partner.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test type", response.json()["types"])
