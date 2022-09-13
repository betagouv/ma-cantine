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

    def test_type_filter(self):
        good = PartnerTypeFactory.create(name="Good")
        ignored = PartnerTypeFactory.create(name="Ignored")

        find_me_1 = PartnerFactory.create(name="Find me")
        find_me_1.types.add(good)
        find_me_2 = PartnerFactory.create(name="Find me too")
        find_me_2.types.add(ignored)
        find_me_2.types.add(good)
        ignore_me = PartnerFactory.create(name="Ignore me")
        ignore_me.types.add(ignored)
        PartnerFactory.create(name="Typeless")

        url = f"{reverse('partners_list')}?type=Good"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)
        results = map(lambda r: r.get("name"), results)
        self.assertTrue("Find me" in results)
        self.assertTrue("Find me too" in results)

    def test_get_single_partner(self):
        type = PartnerTypeFactory.create(name="Test type")
        partner = PartnerFactory.create()
        partner.types.add(type)

        response = self.client.get(reverse("single_partner", kwargs={"pk": partner.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test type", response.json()["types"])
