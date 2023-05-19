from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from data.factories import UserFactory, PurchaseFactory, CanteenFactory, DiagnosticFactory
from data.models import Purchase, Diagnostic, Canteen
from .utils import authenticate


class TestPurchaseApi(APITestCase):
    def test_get_purchases_unauthenticated(self):
        """
        This endpoint is only available when authenticated
        """
        response = self.client.get(reverse("purchase_list_create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_someone_elses_purchases(self):
        """
        This endpoint can only return the purchases of canteens the logged user manages
        """
        other_user = UserFactory.create()
        other_user_canteen = CanteenFactory.create()
        other_user_canteen.managers.add(other_user)

        PurchaseFactory.create(canteen=other_user_canteen)

        response = self.client.get(reverse("purchase_list_create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results", [])
        self.assertEqual(len(body), 0)

    @authenticate
    def test_get_purchases(self):
        """
        The logged user should get the purchases that concern them
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        PurchaseFactory.create(canteen=canteen)
        PurchaseFactory.create(canteen=canteen)

        response = self.client.get(reverse("purchase_list_create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results", [])
        self.assertEqual(len(body), 2)

    def test_create_purchase_unauthenticated(self):
        """
        The purchase creation is only available when logged in
        """
        payload = {
            "date": "2022-01-13",
            "canteen_id": 1,
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_purchase_someone_elses_canteen(self):
        """
        A user can only create a purchase of a canteen they manage
        """
        other_user = UserFactory.create()
        other_user_canteen = CanteenFactory.create()
        other_user_canteen.managers.add(other_user)

        payload = {
            "date": "2022-01-13",
            "canteen": other_user_canteen.id,
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_purchase(self):
        """
        A user can create a purchase
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {
            "date": "2022-01-13",
            "canteen": canteen.id,
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO", "LOCAL"],
            "price_ht": 15.23,
            "local_definition": "AUTOUR_SERVICE",
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.local_definition, Purchase.Local.AUTOUR_SERVICE)
        self.assertEqual(len(purchase.characteristics), 2)

    @authenticate
    def test_create_purchase_nonexistent_canteen(self):
        """
        A user cannot create a purchase for an nonexistent canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {
            "date": "2022-01-13",
            "canteen": "999",
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_purchases_unauthenticated(self):
        """
        The purchase update is only available when logged in
        """
        purchase = PurchaseFactory.create()
        payload = {
            "id": purchase.id,
            "price_ht": 15.23,
        }
        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_update_purchase(self):
        """
        A user can update the data from a purchase object
        """
        purchase = PurchaseFactory.create()
        purchase.canteen.managers.add(authenticate.user)
        new_canteen = CanteenFactory.create()
        new_canteen.managers.add(authenticate.user)

        payload = {
            "id": purchase.id,
            "canteen": new_canteen.id,
            "description": "Saumon",
            "provider": "Test provider",
            "price_ht": 15.23,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        purchase.refresh_from_db()
        self.assertEqual(purchase.canteen, new_canteen)
        self.assertEqual(purchase.description, "Saumon")
        self.assertEqual(purchase.provider, "Test provider")
        self.assertEqual(float(purchase.price_ht), 15.23)

    @authenticate
    def test_update_someone_elses_purchase(self):
        """
        A user should not be able to update someone else's purchase object
        """
        purchase = PurchaseFactory.create()

        payload = {
            "id": purchase.id,
            "description": "Saumon",
            "provider": "Test provider",
            "price_ht": 15.23,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_update_someone_elses_canteen(self):
        """
        A user should not be able to set someone else's canteen in a purchase update
        """
        purchase = PurchaseFactory.create()
        purchase.canteen.managers.add(authenticate.user)
        new_canteen = CanteenFactory.create()

        payload = {
            "id": purchase.id,
            "canteen": new_canteen.id,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_purchase_total_summary(self):
        """
        Given a year, return spending by category
        Bio category is the sum of all products with either bio or bio en conversion labels
        Every category apart from bio should exlude bio (so bio + label rouge gets counted in bio but not label rouge)
        The categories with multiple labels on them should count items with two or more labels once
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        # For the year 2020
        # bio (+ rouge)
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.LABEL_ROUGE],
            price_ht=50,
        )
        # bio en conversion (+ igp)
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-08-01",
            characteristics=[Purchase.Characteristic.CONVERSION_BIO, Purchase.Characteristic.IGP],
            price_ht=150,
        )
        # hve x2 = 10
        PurchaseFactory.create(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.HVE], price_ht=2
        )
        PurchaseFactory.create(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.HVE], price_ht=8
        )
        # rouge x2 = 20
        PurchaseFactory.create(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.LABEL_ROUGE], price_ht=12
        )
        PurchaseFactory.create(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.LABEL_ROUGE], price_ht=8
        )
        # aoc, igp + igp = 30
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.AOCAOP, Purchase.Characteristic.IGP],
            price_ht=22,
        )
        PurchaseFactory.create(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.IGP], price_ht=4
        )
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.IGP, Purchase.Characteristic.HVE],
            price_ht=4,
        )
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.EXTERNALITES, Purchase.Characteristic.PERFORMANCE],
            price_ht=30,
        )
        PurchaseFactory.create(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.PERFORMANCE], price_ht=15
        )
        # some other durable label
        PurchaseFactory.create(
            canteen=canteen, date="2020-01-08", characteristics=[Purchase.Characteristic.PECHE_DURABLE], price_ht=240
        )
        # no labels
        PurchaseFactory.create(canteen=canteen, date="2020-01-01", characteristics=[], price_ht=500)

        # Not in the year 2020 - smoke test for year filtering
        PurchaseFactory.create(
            canteen=canteen, date="2019-01-01", characteristics=[Purchase.Characteristic.BIO], price_ht=666
        )

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["valueTotalHt"], 1045.0)
        self.assertEqual(body["valueBioHt"], 200.0)
        self.assertEqual(body["valueSustainableHt"], 50.0)
        self.assertEqual(body["valueEgalimOthersHt"], 250.0)
        self.assertEqual(body["valueExternalityPerformanceHt"], 45.0)

    @authenticate
    def test_complex_purchase_total_summary(self):
        """
        Given a year, return spending by category
        Bio category is the sum of all products with bio label
        Every category apart from bio should exclude bio (so bio + label rouge gets counted in bio but not label rouge)
        Categories should respect the heirarchy (if something is label rouge + AOC only count in rouge; if AOC and fermier count in AOC only)
        The three categories outside of EGAlim should get the totals regardless of what other labels they have
        The category of AOC/AOP/IGP/STG should count items with two or more labels once (applicable to extended declaration)
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        d = "2020-03-01"
        # some egalim characteristics
        bio = Purchase.Characteristic.BIO
        aoc = Purchase.Characteristic.AOCAOP
        stg = Purchase.Characteristic.STG
        fairtrade = Purchase.Characteristic.COMMERCE_EQUITABLE
        # some non-egalim characteristics
        short_dist = Purchase.Characteristic.SHORT_DISTRIBUTION
        local = Purchase.Characteristic.LOCAL
        # some families
        fruit = Purchase.Family.FRUITS_ET_LEGUMES
        meat = Purchase.Family.VIANDES_VOLAILLES
        other = Purchase.Family.AUTRES

        # test that bio trumps other labels, but doesn't stop non-EGAlim labels
        PurchaseFactory.create(canteen=canteen, date=d, family=fruit, characteristics=[bio, aoc], price_ht=120)
        PurchaseFactory.create(canteen=canteen, date=d, family=fruit, characteristics=[bio, fairtrade], price_ht=80)

        # check that sums are separate between families
        PurchaseFactory.create(
            canteen=canteen, date=d, family=meat, characteristics=[bio, short_dist, local], price_ht=10
        )

        # check that AOC and STG are regrouped and do not count bio totals and trump some other labels
        PurchaseFactory.create(canteen=canteen, date=d, family=fruit, characteristics=[aoc], price_ht=20)
        PurchaseFactory.create(canteen=canteen, date=d, family=fruit, characteristics=[stg, fairtrade], price_ht=60)

        # check that can have a family with only non-EGAlim labels
        PurchaseFactory.create(canteen=canteen, date=d, family=other, characteristics=[local], price_ht=50)
        PurchaseFactory.create(canteen=canteen, date=d, family=other, characteristics=[local], price_ht=50)

        # check that short distribution meat will include both this and the bio purchase which is also short dist.
        PurchaseFactory.create(canteen=canteen, date=d, family=meat, characteristics=[short_dist], price_ht=90)

        # check that items with no label are included in total
        PurchaseFactory.create(canteen=canteen, date=d, family=other, characteristics=[], price_ht=110)

        # Not in the year 2020 - smoke test for year filtering
        PurchaseFactory.create(canteen=canteen, date="2019-01-01", characteristics=[bio], price_ht=666)

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["valueTotalHt"], 590.0)
        self.assertEqual(body["valueFruitsEtLegumesBio"], 200.0)
        self.assertEqual(body["valueViandesVolaillesBio"], 10.0)
        self.assertEqual(body["valueFruitsEtLegumesAocaopIgpStg"], 80.0)
        self.assertEqual(body["valueFruitsEtLegumesCommerceEquitable"], None)
        self.assertEqual(body["valueAutresLocal"], 100.0)
        self.assertEqual(body["valueViandesVolaillesShortDistribution"], 100.0)
        self.assertEqual(body["valueViandesVolaillesLocal"], 10.0)
        self.assertEqual(body["valueAutresNonEgalim"], 210.0)
        self.assertEqual(body["valueViandesVolaillesNonEgalim"], 90.0)

    def test_purchase_summary_unauthenticated(self):
        canteen = CanteenFactory.create()
        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_purchase_meat_totals(self):
        """
        The totals for "viandes et volailles" must be included in the payload
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        # Should be counted both on EGALIM and "Provenance France"
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[
                Purchase.Characteristic.BIO,
                Purchase.Characteristic.LABEL_ROUGE,
                Purchase.Characteristic.FRANCE,
            ],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=50,
        )

        # Should be counted on EGALIM
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=40,
        )

        # Should be counted on EGALIM
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=30,
        )

        # Should not be counted as EGAlim, only included in the total
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=20,
        )

        # Should be counted on provenance france
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.FRANCE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=15,
        )

        # Not in the year 2020 - should not be included at all
        PurchaseFactory.create(
            canteen=canteen,
            date="2019-01-01",
            characteristics=[],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=10,
        )

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["valueMeatPoultryHt"], 155.0)
        self.assertEqual(body["valueMeatPoultryEgalimHt"], 120.0)
        self.assertEqual(body["valueMeatPoultryFranceHt"], 65.0)

    @authenticate
    def test_purchase_fish_totals(self):
        """
        The totals for "poissons, produits de la mer et de l'aquaculture" must be included in the payload
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        # Should be counted on EGALIM only once
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=55,
        )

        # Should be counted on EGALIM
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=40,
        )

        # Should be counted on EGALIM
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=30,
        )

        # Should not be counted as EGAlim, only included in the total
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=20,
        )

        # Should not be counted as EGAlim, only included in the total
        PurchaseFactory.create(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.FRANCE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=15,
        )

        # Not in the year 2020 - should not be included at all
        PurchaseFactory.create(
            canteen=canteen,
            date="2019-01-01",
            characteristics=[],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=10,
        )

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["valueFishHt"], 160.0)
        self.assertEqual(body["valueFishEgalimHt"], 125.0)

    @authenticate
    def test_purchase_not_authorized(self):
        canteen = CanteenFactory.create()
        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_purchase_nonexistent_canteen(self):
        response = self.client.get(reverse("canteen_purchases_summary", kwargs={"canteen_pk": 999999}), {"year": 2020})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_get_multi_year_purchase_statistics(self):
        """
        It is possible for a manager to retrieve year-on-year purchase totals for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        PurchaseFactory.create(canteen=canteen, price_ht=100, date="2020-01-01")
        PurchaseFactory.create(canteen=canteen, price_ht=50, date="2020-12-31")
        PurchaseFactory.create(canteen=canteen, price_ht=300, date="2021-01-01")
        PurchaseFactory.create(canteen=canteen, price_ht=150, date="2021-12-31")

        other_canteen = CanteenFactory.create()
        other_canteen.managers.add(authenticate.user)
        PurchaseFactory.create(canteen=other_canteen, price_ht=999, date="2021-01-01")

        response = self.client.get(reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("results", body)
        self.assertEquals(len(body["results"]), 2)
        self.assertEquals(body["results"][0]["year"], 2020)
        self.assertEquals(body["results"][0]["valueTotalHt"], 150)
        self.assertIn("valueBioHt", body["results"][0])
        self.assertEquals(body["results"][1]["year"], 2021)
        self.assertEquals(body["results"][1]["valueTotalHt"], 450)

    @authenticate
    def test_delete_purchase(self):
        """
        A user can delete a purchase object
        """
        purchase = PurchaseFactory.create()
        purchase.canteen.managers.add(authenticate.user)

        response = self.client.delete(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Purchase.objects.filter(pk=purchase.id).count(), 0)

    @authenticate
    def test_delete_unauthorized(self):
        """
        A user cannot delete a purchase object of a canteen they don't manage
        """
        purchase = PurchaseFactory.create()

        response = self.client.delete(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Purchase.objects.filter(pk=purchase.id).count(), 1)

    def test_delete_unauthenticated(self):
        """
        A user cannot delete a purchase object of a canteen if they're not authenticated
        """
        purchase = PurchaseFactory.create()

        response = self.client.delete(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Purchase.objects.filter(pk=purchase.id).count(), 1)  #

    @authenticate
    def test_delete_multiple_purchases(self):
        """
        Given a list of purchase ids, soft delete those purchases
        """
        purchase_1 = PurchaseFactory.create(deletion_date=None)
        purchase_1.canteen.managers.add(authenticate.user)
        purchase_2 = PurchaseFactory.create(deletion_date=None)
        purchase_2.canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse("delete_purchases"), {"ids": [purchase_1.id, purchase_2.id]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase_1.refresh_from_db()
        purchase_2.refresh_from_db()
        self.assertIsNotNone(purchase_1.deletion_date)
        self.assertIsNotNone(purchase_2.deletion_date)

    @authenticate
    def test_delete_invalid_purchases(self):
        """
        Ignore ids that are: non-existant; already deleted; not managed by the user
        And delete what can be deleted
        """
        should_delete = PurchaseFactory.create(deletion_date=None)
        date = timezone.now()
        already_deleted = PurchaseFactory.create(deletion_date=date)
        should_delete.canteen.managers.add(authenticate.user)
        already_deleted.canteen.managers.add(authenticate.user)
        invalid_id = "999"
        not_mine = PurchaseFactory.create(deletion_date=None)
        ids = [should_delete.id, already_deleted.id, invalid_id, not_mine.id]

        response = self.client.post(reverse("delete_purchases"), {"ids": ids}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        should_delete.refresh_from_db()
        self.assertIsNotNone(should_delete.deletion_date)
        already_deleted.refresh_from_db()
        self.assertEqual(already_deleted.deletion_date, date)
        not_mine.refresh_from_db()
        self.assertIsNone(not_mine.deletion_date)

    @authenticate
    def test_restore_purchases(self):
        """
        This endpoint restores the given IDs of deleted purchases
        """
        date = timezone.now()
        purchase_1 = PurchaseFactory.create(deletion_date=date)
        purchase_2 = PurchaseFactory.create(deletion_date=date)
        not_me = PurchaseFactory.create(deletion_date=date)
        for p in [purchase_1, purchase_2, not_me]:
            p.canteen.managers.add(authenticate.user)
        not_my_purchase = PurchaseFactory.create(deletion_date=date)

        response = self.client.post(
            reverse("restore_purchases"), {"ids": [purchase_1.id, purchase_2.id, not_my_purchase.id]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)
        purchase_1.refresh_from_db()
        purchase_2.refresh_from_db()
        not_me.refresh_from_db()
        not_my_purchase.refresh_from_db()
        self.assertIsNone(purchase_1.deletion_date)
        self.assertIsNone(purchase_2.deletion_date)
        self.assertEqual(not_me.deletion_date, date)
        self.assertEqual(not_my_purchase.deletion_date, date)

    @authenticate
    def test_search_purchases(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen)
        PurchaseFactory.create(description="tomates", canteen=canteen)
        PurchaseFactory.create(description="pommes", canteen=canteen)

        search_term = "avoine"
        response = self.client.get(f"{reverse('purchase_list_create')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("description"), "avoine")

    @authenticate
    def test_search_only_user_purchases(self):
        PurchaseFactory.create(description="avoine")
        PurchaseFactory.create(description="tomates")
        PurchaseFactory.create(description="pommes")

        search_term = "avoine"
        response = self.client.get(f"{reverse('purchase_list_create')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 0)

    @authenticate
    def test_filter_by_canteen(self):
        canteen = CanteenFactory.create()
        other_canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        other_canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen)
        PurchaseFactory.create(description="tomates", canteen=other_canteen)
        PurchaseFactory.create(description="pommes", canteen=canteen)

        canteen_id = canteen.id
        response = self.client.get(f"{reverse('purchase_list_create')}?canteen__id={canteen_id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 2)

    @authenticate
    def test_filter_by_characteristic(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen, characteristics=[Purchase.Characteristic.BIO])
        PurchaseFactory.create(
            description="tomates",
            canteen=canteen,
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.PECHE_DURABLE],
        )
        PurchaseFactory.create(
            description="pommes", canteen=canteen, characteristics=[Purchase.Characteristic.PECHE_DURABLE]
        )

        response = self.client.get(f"{reverse('purchase_list_create')}?characteristics={Purchase.Characteristic.BIO}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

        response = self.client.get(
            f"{reverse('purchase_list_create')}?characteristics={Purchase.Characteristic.BIO}&characteristics={Purchase.Characteristic.PECHE_DURABLE}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)

    @authenticate
    def test_filter_by_family(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen, family=Purchase.Family.PRODUITS_DE_LA_MER)
        PurchaseFactory.create(description="tomates", canteen=canteen, family=Purchase.Family.PRODUITS_DE_LA_MER)
        PurchaseFactory.create(description="pommes", canteen=canteen, family=Purchase.Family.AUTRES)

        response = self.client.get(f"{reverse('purchase_list_create')}?family={Purchase.Family.PRODUITS_DE_LA_MER}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

    @authenticate
    def test_filter_by_date(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen, date="2020-01-01")
        PurchaseFactory.create(description="tomates", canteen=canteen, date="2020-01-02")
        PurchaseFactory.create(description="pommes", canteen=canteen, date="2020-02-01")

        response = self.client.get(f"{reverse('purchase_list_create')}?date_after=2020-01-02")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

        response = self.client.get(f"{reverse('purchase_list_create')}?date_before=2020-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)

        response = self.client.get(f"{reverse('purchase_list_create')}?date_after=2020-01-02&date_before=2020-02-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

    @authenticate
    def test_available_filter_options(self):
        """
        Test that filter options with data are included in purchases list response
        """
        first_canteen = CanteenFactory.create()
        first_canteen.managers.add(authenticate.user)
        second_canteen = CanteenFactory.create()
        second_canteen.managers.add(authenticate.user)
        PurchaseFactory.create(
            description="avoine",
            canteen=first_canteen,
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            characteristics=[Purchase.Characteristic.BIO],
        )
        PurchaseFactory.create(
            description="tomates",
            canteen=first_canteen,
            family=Purchase.Family.VIANDES_VOLAILLES,
            characteristics=[],
        )
        PurchaseFactory.create(
            description="pommes",
            canteen=second_canteen,
            family=Purchase.Family.PRODUITS_LAITIERS,
            characteristics=[Purchase.Characteristic.LABEL_ROUGE],
        )

        not_my_canteen = CanteenFactory.create()
        PurchaseFactory.create(
            description="secret",
            canteen=not_my_canteen,
            family=Purchase.Family.AUTRES,
            characteristics=[Purchase.Characteristic.COMMERCE_EQUITABLE],
        )

        response = self.client.get(f"{reverse('purchase_list_create')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        families = body.get("families", [])
        self.assertEqual(len(families), 3)
        self.assertIn(Purchase.Family.PRODUITS_DE_LA_MER, families)
        self.assertNotIn(Purchase.Family.AUTRES, families)
        self.assertEqual(len(body.get("characteristics", [])), 2)
        canteens = body.get("canteens", [])
        self.assertEqual(len(canteens), 2)
        self.assertNotIn(not_my_canteen.id, canteens)

        response = self.client.get(f"{reverse('purchase_list_create')}?characteristics={Purchase.Characteristic.BIO}")
        body = response.json()
        self.assertEqual(len(body["families"]), 1)

        response = self.client.get(f"{reverse('purchase_list_create')}?family={Purchase.Family.PRODUITS_LAITIERS}")
        body = response.json()
        self.assertEqual(len(body["characteristics"]), 1)

    def test_excel_export_unauthenticated(self):
        response = self.client.get(reverse("purchase_list_export"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_excel_export(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen)
        PurchaseFactory.create(description="tomates", canteen=canteen)
        PurchaseFactory.create(description="pommes", canteen=canteen)

        response = self.client.get(reverse("purchase_list_export"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    @authenticate
    def test_excel_export_search(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen)
        PurchaseFactory.create(description="tomates", canteen=canteen)
        PurchaseFactory.create(description="pommes", canteen=canteen)

        search_term = "avoine"
        response = self.client.get(f"{reverse('purchase_list_export')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @authenticate
    def test_excel_export_filter(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(family=Purchase.Family.PRODUITS_DE_LA_MER, description="avoine", canteen=canteen)
        PurchaseFactory.create(family=Purchase.Family.PRODUITS_DE_LA_MER, description="tomates", canteen=canteen)
        PurchaseFactory.create(family=Purchase.Family.AUTRES, description="pommes", canteen=canteen)

        response = self.client.get(f"{reverse('purchase_list_export')}?family=PRODUITS_DE_LA_MER")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @authenticate
    def test_get_purchase_options(self):
        """
        A manager should be able to retrieve a list of products and providers that
        they've already entered on their own purchases
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        PurchaseFactory.create(description="avoine", canteen=canteen, provider="provider1")
        PurchaseFactory.create(description="pommes", canteen=canteen, provider="provider2")
        PurchaseFactory.create(description="pommes", canteen=canteen, provider="provider1")
        PurchaseFactory.create(description=None, canteen=canteen, provider=None)

        PurchaseFactory.create(description="secret product", provider="secret provider")

        response = self.client.get(f"{reverse('purchase_options')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["products"]), 2)
        self.assertEqual(len(body["providers"]), 2)
        self.assertIn("avoine", body["products"])
        self.assertIn("provider2", body["providers"])
        self.assertNotIn("secret product", body["products"])
        self.assertNotIn("secret provider", body["providers"])

    def test_get_purchase_options_unauthenticated(self):
        response = self.client.get(reverse("purchase_options"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_diagnostics_from_purchases(self):
        """
        Given a list of canteen ids and a year, create diagnostics
        pre-filled with purchase totals for that year
        """
        # TODO: refactor canteen creation and manager adding into setup and takedown?
        canteen_site = CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE)
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL)
        canteens = [canteen_site, central_kitchen]
        for canteen in canteens:
            canteen.managers.add(authenticate.user)
        # purchases to be included in totals
        PurchaseFactory.create(canteen=canteen_site, date="2021-01-01", price_ht=50)
        PurchaseFactory.create(canteen=canteen_site, date="2021-12-31", price_ht=150)

        PurchaseFactory.create(canteen=central_kitchen, date="2021-01-01", price_ht=5)
        PurchaseFactory.create(canteen=central_kitchen, date="2021-12-31", price_ht=15)

        # purchases to be filtered out from totals
        PurchaseFactory.create(canteen=canteen_site, date="2022-01-01", price_ht=666)
        PurchaseFactory.create(canteen=central_kitchen, date="2020-12-31", price_ht=666)

        year = 2021
        self.assertEqual(Diagnostic.objects.filter(year=year, canteen__in=canteens).count(), 0)

        response = self.client.post(
            reverse("diagnostics_from_purchases"),
            {"year": year, "canteenIds": [canteen_site.id, central_kitchen.id]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 2)
        diag_site = Diagnostic.objects.get(year=year, canteen=canteen_site)
        self.assertIn(diag_site.id, results)
        self.assertEqual(diag_site.value_total_ht, 200)
        self.assertEqual(diag_site.central_kitchen_diagnostic_mode, None)
        diag_cc = Diagnostic.objects.get(year=year, canteen=central_kitchen)
        self.assertIn(diag_cc.id, results)
        self.assertEqual(diag_cc.value_total_ht, 20)
        self.assertEqual(diag_cc.central_kitchen_diagnostic_mode, "APPRO")

    def test_unauthorised_create_diagnostics_from_purchases(self):
        """
        If not logged in, throw a 403
        """
        response = self.client.post(reverse("diagnostics_from_purchases"), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_missing_year_create_diagnostics_from_purchases(self):
        """
        If year is missing, throw a 400
        """
        response = self.client.post(reverse("diagnostics_from_purchases"), {"canteenIds": []}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_missing_canteens_create_diagnostics_from_purchases(self):
        """
        If canteen ids are missing, throw a 400
        """
        response = self.client.post(reverse("diagnostics_from_purchases"), {"year": 2021}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_errors_for_create_diagnostics_from_purchases(self):
        """
        Handle errors in diagnostic creation gracefully, creating what can be created
        """
        canteen_with_diag = CanteenFactory.create()
        canteen_without_purchases = CanteenFactory.create()
        good_canteen = CanteenFactory.create()
        canteens = [canteen_with_diag, canteen_without_purchases, good_canteen]
        for canteen in canteens:
            canteen.managers.add(authenticate.user)
        not_my_canteen = CanteenFactory.create()

        year = 2023
        DiagnosticFactory.create(canteen=canteen_with_diag, year=year)
        PurchaseFactory.create(canteen=good_canteen, date=f"{year}-01-01", price_ht=100)
        PurchaseFactory.create(canteen=canteen_with_diag, date=f"{year}-01-01", price_ht=666)
        PurchaseFactory.create(canteen=not_my_canteen, date=f"{year}-01-01", price_ht=666)

        response = self.client.post(
            reverse("diagnostics_from_purchases"),
            {"year": year, "canteenIds": ["666", not_my_canteen.id] + [canteen.id for canteen in canteens]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 1)
        errors = body["errors"]
        self.assertEqual(errors[0], "Inconnue cantine : 666")
        self.assertEqual(errors[1], f"Vous ne gerez pas la cantine : {not_my_canteen.id}")
        self.assertEqual(
            errors[2], f"Il existe déjà un diagnostic pour l'année 2023 pour la cantine : {canteen_with_diag.id}"
        )
        self.assertEqual(errors[3], f"Aucun achat trouvé pour la cantine : {canteen_without_purchases.id}")
        self.assertEqual(len(errors), 4)

    # test another endpoint: fetching canteens that can have diags created + provisional totals (preview before creation?)
