from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import PartnerFactory, PartnerTypeFactory, SectorFactory, UserFactory
from data.models import Partner


class TestPartnersApi(APITestCase):
    def test_get_partners(self):
        """
        Returns partners and the types that are in use therefore available for filtering
        """
        sector_1 = SectorFactory.create()
        sector_2 = SectorFactory.create()
        sector_3 = SectorFactory.create()
        type = PartnerTypeFactory.create(name="Test type")
        type_2 = PartnerTypeFactory.create(name="Test type 2")
        PartnerTypeFactory.create(name="Unused type")
        partners = [
            PartnerFactory.create(departments=["01", "02"], published=True),
            PartnerFactory.create(departments=["01", "11"], published=True),
            PartnerFactory.create(departments=None, published=True),
        ]
        partners[0].types.add(type)
        partners[0].sectors.add(sector_1)
        partners[1].types.add(type)  # add same type to two different partners to check deduplication
        partners[1].types.add(type_2)
        partners[1].sectors.add(sector_2)
        # don't add type to third partner to check null value filtering
        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body.get("count"), 3)

        results = body.get("results", [])
        for partner in partners:
            self.assertTrue(any(x["id"] == partner.id for x in results))

        types = body.get("types", [])
        self.assertIn("Test type", types)
        self.assertIn("Test type 2", types)
        self.assertEqual(len(types), 2)

        departments = body.get("departments", [])
        self.assertIn("01", departments)
        self.assertIn("02", departments)
        self.assertIn("11", departments)
        self.assertEqual(len(departments), 3)

        sectors = body.get("sectors", [])
        self.assertIn(sector_1.id, sectors)
        self.assertIn(sector_2.id, sectors)
        self.assertNotIn(sector_3.id, sectors)

    def test_type_filter(self):
        """
        Return the union of all partners based on the types requested
        """
        good = PartnerTypeFactory.create(name="Good")
        also = PartnerTypeFactory.create(name="Also good")
        ignored = PartnerTypeFactory.create(name="Ignored")

        find_me_1 = PartnerFactory.create(name="Find me", published=True)
        find_me_1.types.add(good)
        find_me_2 = PartnerFactory.create(name="Find me too", published=True)
        find_me_2.types.add(ignored)
        find_me_2.types.add(good)
        find_me_3 = PartnerFactory.create(name="Me three", published=True)
        find_me_3.types.add(also)
        ignore_me = PartnerFactory.create(name="Ignore me", published=True)
        ignore_me.types.add(ignored)
        PartnerFactory.create(name="Typeless", published=True)

        url = f"{reverse('partners_list')}?type=Good&type=Also good"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        results = list(map(lambda r: r.get("name"), results))
        self.assertIn("Find me", results)
        self.assertIn("Find me too", results)
        self.assertIn("Me three", results)

    def test_department_filter(self):
        """
        Return the union of all partners based on departments requested
        """
        PartnerFactory.create(name="Find me", departments=["09"], published=True)
        PartnerFactory.create(name="Find me too", departments=["10"], published=True)
        PartnerFactory.create(name="Me three", departments=["10", "11"], published=True)
        PartnerFactory.create(name="But not me", departments=["11"], published=True)

        url = f"{reverse('partners_list')}?department=09&department=10"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        results = list(map(lambda r: r.get("name"), results))
        self.assertIn("Find me", results)
        self.assertIn("Find me too", results)
        self.assertIn("Me three", results)

    def test_cost_filter(self):
        """
        Return all the free partners
        """
        PartnerFactory.create(name="Find me", gratuity_option=Partner.GratuityOption.FREE, published=True)
        PartnerFactory.create(name="But not me", gratuity_option=Partner.GratuityOption.PAID, published=True)

        url = f"{reverse('partners_list')}?gratuityOption=free"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Find me")

    def test_categories_filter(self):
        """
        Returns the union of all partners based on categories (aka needs) requested
        """
        PartnerFactory.create(name="Find me", categories=["appro"], published=True)
        PartnerFactory.create(name="Find me too", categories=["plastic"], published=True)
        PartnerFactory.create(name="Me three", categories=["plastic", "asso"], published=True)
        PartnerFactory.create(name="But not me", categories=["asso"], published=True)

        url = f"{reverse('partners_list')}?category=appro&category=plastic"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        results = list(map(lambda r: r.get("name"), results))
        self.assertIn("Find me", results)
        self.assertIn("Find me too", results)
        self.assertIn("Me three", results)

    def test_get_single_partner(self):
        type = PartnerTypeFactory.create(name="Test type")
        partner = PartnerFactory.create(published=True)
        partner.types.add(type)

        response = self.client.get(reverse("single_partner", kwargs={"pk": partner.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test type", response.json()["types"])

    def test_get_published_partners_only(self):
        PartnerFactory.create(name="I am published", published=True)
        PartnerFactory.create(name="I am secret", published=False)

        response = self.client.get(reverse("partners_list"))
        partners = response.json().get("results")
        self.assertEqual(len(partners), 1)
        self.assertEqual(partners[0]["name"], "I am published")

    def test_get_published_partner_only(self):
        partner = PartnerFactory.create(name="I am secret", published=False)

        response = self.client.get(reverse("single_partner", kwargs={"pk": partner.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_partner(self):
        """
        Test that unauthenticated users can create draft partners
        """
        sector = SectorFactory.create()
        partner_type = PartnerTypeFactory.create()
        self.assertEqual(Partner.objects.count(), 0)
        payload = {
            "name": "New partner please",
            "shortDescription": "This is a required field",
            "published": True,
            "contactEmail": "test@example.com",
            "sectors": [sector.id],
            "types": [partner_type.id],
        }
        response = self.client.post(reverse("partners_list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Partner.objects.count(), 1, "Exactly one partner added to DB")
        partner = Partner.objects.first()
        self.assertEqual(partner.name, "New partner please")
        self.assertEqual(partner.short_description, "This is a required field")
        self.assertEqual(partner.contact_email, "test@example.com")
        self.assertEqual(partner.sectors.count(), 1)
        self.assertEqual(partner.sectors.first().id, sector.id)
        self.assertEqual(partner.types.count(), 1)
        self.assertEqual(partner.types.first().id, partner_type.id)
        self.assertFalse(partner.published, "A user can't create a published partner")

    def test_cannot_fetch_contact_info(self):
        partner = PartnerFactory.create(published=True, contact_email="secret@mi5.com")

        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        partner = body["results"][0]
        self.assertNotIn("contactEmail", partner)

    def test_randomized_results(self):
        """
        Results should be randomized yet consistent with the user
        """
        for i in range(50):
            PartnerFactory.create(published=True)
        user_1 = UserFactory.create()
        user_2 = UserFactory.create()

        self.client.force_login(user=user_1)

        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        user_1_results_1 = [x["id"] for x in body.get("results")]
        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        user_1_results_2 = [x["id"] for x in body.get("results")]
        self.client.force_login(user=user_2)

        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        user_2_results_1 = [x["id"] for x in body.get("results")]
        response = self.client.get(reverse("partners_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        user_2_results_2 = [x["id"] for x in body.get("results")]
        self.assertEqual(user_1_results_1, user_1_results_2)
        self.assertEqual(user_2_results_1, user_2_results_2)
        self.assertNotEqual(user_1_results_1, user_2_results_1)
