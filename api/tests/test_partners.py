from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PartnerFactory, PartnerTypeFactory


class TestPartnersApi(APITestCase):
    def test_get_partners(self):
        """
        Returns partners and the types that are in use therefore available for filtering
        """
        type = PartnerTypeFactory.create(name="Test type")
        PartnerTypeFactory.create(name="Unused type")
        partners = [
            PartnerFactory.create(),
            PartnerFactory.create(),
            PartnerFactory.create(),
        ]
        partners[0].types.add(type)
        partners[1].types.add(type)  # add same type to two different partners to check deduplication
        # don't add type to third partner to check null value filtering
        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body.get("count"), 3)

        results = body.get("results", [])
        for partner in partners:
            self.assertTrue(any(x["id"] == partner.id for x in results))

        types = body.get("types", [])
        self.assertEqual(len(types), 1)
        self.assertIn("Test type", types)

    def test_type_filter(self):
        """
        Return the union of all partners based on the types requested
        """
        good = PartnerTypeFactory.create(name="Good")
        also = PartnerTypeFactory.create(name="Also good")
        ignored = PartnerTypeFactory.create(name="Ignored")

        find_me_1 = PartnerFactory.create(name="Find me")
        find_me_1.types.add(good)
        find_me_2 = PartnerFactory.create(name="Find me too")
        find_me_2.types.add(ignored)
        find_me_2.types.add(good)
        find_me_3 = PartnerFactory.create(name="Me three")
        find_me_3.types.add(also)
        ignore_me = PartnerFactory.create(name="Ignore me")
        ignore_me.types.add(ignored)
        PartnerFactory.create(name="Typeless")

        url = f"{reverse('partners_list')}?type=Good&type=Also good"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        results = map(lambda r: r.get("name"), results)
        self.assertIn("Find me", results)
        self.assertIn("Find me too", results)
        self.assertIn("Me three", results)

    def test_department_filter(self):
        """
        Return the union of all partners based on departments requested
        """
        PartnerFactory.create(name="Find me", departments=["09"])
        PartnerFactory.create(name="Find me too", departments=["10"])
        PartnerFactory.create(name="Me three", departments=["10", "11"])
        PartnerFactory.create(name="But not me", departments=["11"])

        url = f"{reverse('partners_list')}?department=09&department=10"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        results = map(lambda r: r.get("name"), results)
        self.assertIn("Find me", results)
        self.assertIn("Find me too", results)
        self.assertIn("Me three", results)

    def test_cost_filter(self):
        """
        Return all the free partners
        """
        PartnerFactory.create(name="Find me", free=True)
        PartnerFactory.create(name="But not me", free=False)

        url = f"{reverse('partners_list')}?free=True"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Find me")

    def test_categories_filter(self):
        """
        Returns the union of all partners based on categories (aka needs) requested
        """
        PartnerFactory.create(name="Find me", categories=["appro"])
        PartnerFactory.create(name="Find me too", categories=["plastic"])
        PartnerFactory.create(name="Me three", categories=["plastic", "asso"])
        PartnerFactory.create(name="But not me", categories=["asso"])

        url = f"{reverse('partners_list')}?category=appro&category=plastic"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        results = map(lambda r: r.get("name"), results)
        self.assertIn("Find me", results)
        self.assertIn("Find me too", results)
        self.assertIn("Me three", results)

    def test_get_single_partner(self):
        type = PartnerTypeFactory.create(name="Test type")
        partner = PartnerFactory.create()
        partner.types.add(type)

        response = self.client.get(reverse("single_partner", kwargs={"pk": partner.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test type", response.json()["types"])
