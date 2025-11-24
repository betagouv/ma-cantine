from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, PurchaseFactory
from data.models import Canteen, Diagnostic, Teledeclaration, Sector


class CanteenActionApiTest(APITestCase):
    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_canteen_actions(self):
        """
        Check that this endpoint returns the user's canteens and the next action required
        """
        # these canteens aren't in a very logical order, because want to test sorting by action
        # create diag (has one for 2020)
        needs_last_year_diag = CanteenFactory.create(
            siret="21590350100017",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        # nothing to do
        complete = CanteenFactory.create(
            siret="21340172201787",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        complete_central_no_sectors = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            siret="21380185500015",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
            satellite_canteens_count=1,
            sector_list=[],
        )
        complete_central_with_diff_sat_count = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            siret="21670482500019",
            managers=[authenticate.user],
            satellite_canteens_count=10,
            sector_list=[],
        )
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=complete_central_with_diff_sat_count.siret,
        )
        complete_site_one_sector = CanteenFactory.create(
            siret="21640122400011",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
            sector_list=[Sector.EDUCATION_PRIMAIRE],
        )
        # complete diag
        needs_to_fill_diag = CanteenFactory.create(
            siret="21010034300016",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        central_siret = "92341284500011"
        needs_diagnostic_mode = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL, siret=central_siret, managers=[authenticate.user]
        )
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_siret
        )
        # complete establishement
        needs_sectors = CanteenFactory.create(
            siret="37856520465586",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            managers=[authenticate.user],
        )
        Canteen.objects.filter(id=needs_sectors.id).update(sector_list=[])
        needs_sectors.refresh_from_db()
        needs_daily_meal_count = CanteenFactory.create(
            siret="40419443300078",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            # daily_meal_count=12,
            managers=[authenticate.user],
        )
        Canteen.objects.filter(id=needs_daily_meal_count.id).update(daily_meal_count=None)
        needs_daily_meal_count.refresh_from_db()
        too_many_sectors = CanteenFactory.create(
            siret="83014132100034",
            managers=[authenticate.user],
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PRIVATE,
            city_insee_code="69123",
            sector_list=[
                Sector.ADMINISTRATION_PRISON,
                Sector.EDUCATION_PRIMAIRE,
                Sector.SANTE_HOPITAL,
                Sector.SOCIAL_EHPAD,
            ],
        )
        # TD
        needs_td = CanteenFactory.create(
            siret="21630113500010",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        # create satellites
        needs_additional_satellites = CanteenFactory.create(
            siret="78146469373706",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=3,
            managers=[authenticate.user],
        )
        CanteenFactory.create(name="Not my canteen")

        last_year = 2021
        DiagnosticFactory.create(year=last_year - 1, canteen=needs_last_year_diag)

        td_diag = DiagnosticFactory.create(year=last_year, canteen=complete, value_total_ht=1000)
        Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)
        td_diag_central_no_sectors = DiagnosticFactory.create(
            year=last_year,
            canteen=complete_central_no_sectors,
            value_total_ht=1000,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        Teledeclaration.create_from_diagnostic(td_diag_central_no_sectors, authenticate.user)
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=complete_central_no_sectors.siret,
        )

        td_diag_central_with_one_sat = DiagnosticFactory.create(
            year=last_year,
            canteen=complete_central_with_diff_sat_count,
            value_total_ht=1000,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        Teledeclaration.create_from_diagnostic(td_diag_central_with_one_sat, authenticate.user)

        td_diag_one_sector = DiagnosticFactory.create(
            year=last_year,
            canteen=complete_site_one_sector,
            value_total_ht=1000,
        )
        Teledeclaration.create_from_diagnostic(td_diag_one_sector, authenticate.user)

        DiagnosticFactory.create(year=last_year, canteen=needs_to_fill_diag, value_total_ht=None)
        # make sure the endpoint only looks at diagnostics of the year requested
        DiagnosticFactory.create(year=last_year - 1, canteen=needs_to_fill_diag, value_total_ht=1000)

        DiagnosticFactory.create(
            year=last_year, canteen=needs_diagnostic_mode, central_kitchen_diagnostic_mode=None, value_total_ht=100
        )

        DiagnosticFactory.create(year=last_year, canteen=needs_td, value_total_ht=100)

        DiagnosticFactory.create(year=last_year, canteen=needs_sectors, value_total_ht=100)

        DiagnosticFactory.create(year=last_year, canteen=needs_daily_meal_count, value_total_ht=100)

        DiagnosticFactory.create(year=last_year, canteen=too_many_sectors, value_total_ht=100)

        # has a diagnostic but this canteen did not register any satellites
        DiagnosticFactory.create(year=last_year, canteen=needs_additional_satellites, value_total_ht=100)

        response = self.client.get(
            reverse("list_actionable_canteens", kwargs={"year": last_year}) + "?ordering=action,modification_date"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        returned_canteens = body["results"]
        self.assertEqual(len(returned_canteens), 12)

        expected_actions = [
            (needs_additional_satellites, Canteen.Actions.ADD_SATELLITES),
            (needs_last_year_diag, Canteen.Actions.CREATE_DIAGNOSTIC),
            (needs_to_fill_diag, Canteen.Actions.FILL_DIAGNOSTIC),
            (needs_diagnostic_mode, Canteen.Actions.FILL_DIAGNOSTIC),
            (needs_sectors, Canteen.Actions.FILL_CANTEEN_DATA),
            (needs_daily_meal_count, Canteen.Actions.FILL_CANTEEN_DATA),
            (too_many_sectors, Canteen.Actions.FILL_CANTEEN_DATA),
            (needs_td, Canteen.Actions.TELEDECLARE),
            (complete, Canteen.Actions.NOTHING),
            (complete_central_no_sectors, Canteen.Actions.NOTHING),
            (complete_central_with_diff_sat_count, Canteen.Actions.NOTHING),
            (complete_site_one_sector, Canteen.Actions.NOTHING),
        ]
        for index, (canteen, action) in zip(range(len(expected_actions)), expected_actions):
            with self.subTest(canteen=canteen, action=action):
                self.assertEqual(returned_canteens[index]["id"], canteen.id)
                self.assertEqual(returned_canteens[index]["action"], action)
                self.assertIn("sectors", returned_canteens[index])
        self.assertTrue(body["hasPendingActions"])

    @authenticate
    def test_central_without_satellites_has_complete_satellites_action(self):
        """
        Test for a bug fix. A central that doesn't have any satellites at all should get the complete satellite action.
        """
        CanteenFactory.create(
            siret="45467900121441",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=3,
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}) + "?ordering=action")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["results"][0]["action"], Canteen.Actions.ADD_SATELLITES)

    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_actions_missing_data(self):
        """
        Even if the diagnostic is complete, the mandatory information on the canteen level should
        return a Canteen.Actions.FILL_CANTEEN_DATA
        """
        canteen_central = CanteenFactory.create(
            siret="21590350100017",
            production_type=Canteen.ProductionType.CENTRAL,
        )
        # First a case in which the canteen is complete
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            siret="96766910375238",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        last_year = 2021
        diagnostic = DiagnosticFactory.create(year=last_year, canteen=canteen, value_total_ht=1000)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)

        # If mandatory data on the canteen is missing, we need a 35_fill_canteen_data
        Canteen.objects.filter(id=canteen.id).update(yearly_meal_count=None)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

        # Central cuisines should have the number of satellites filled in
        Canteen.objects.filter(id=canteen.id).update(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=1000, satellite_canteens_count=None
        )
        canteen_sat = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            central_producer_siret=canteen.siret,
            managers=[authenticate.user],
        )
        diagnostic.central_kitchen_diagnostic_mode = "APPRO"
        diagnostic.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

        # reset diag from above change.
        diagnostic.central_kitchen_diagnostic_mode = None
        diagnostic.save()

        # Central kitchens with missing satellites should return the add satellite action
        canteen_sat.delete()
        Canteen.objects.filter(id=canteen.id).update(satellite_canteens_count=123)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.ADD_SATELLITES)

        # Satellites should have the SIRET of the central cuisine (1/2)
        canteen.production_type = Canteen.ProductionType.ON_SITE_CENTRAL
        canteen.central_producer_siret = canteen_central.siret
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)

        # Satellites should have the SIRET of the central cuisine (2/2)
        Canteen.objects.filter(id=canteen.id).update(central_producer_siret=None)
        canteen.refresh_from_db()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_actions_satellite(self):
        """
        If a satellite's CC has teledeclared there is no pending action for the satellite
        """
        central_kitchen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            siret="96766910375238",
            city_insee_code="69123",
            satellite_canteens_count=1,
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            siret="99569440745111",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            central_producer_siret="96766910375238",
            managers=[authenticate.user],
        )
        diagnostic = DiagnosticFactory.create(
            year=2021,
            canteen=central_kitchen,
            value_total_ht=1000,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
        )

        last_year = 2021
        DiagnosticFactory.create(
            year=last_year,
            canteen=satellite,
            value_total_ht=1200,
        )

        # cc diagnostic not teledeclared
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        satellite_action = next(x for x in returned_canteens if x["id"] == satellite.id)["action"]
        self.assertEqual(satellite_action, Canteen.Actions.NOTHING_SATELLITE)

        # cc diagnostic teledeclared
        Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        satellite_action = next(x for x in returned_canteens if x["id"] == satellite.id)["action"]
        self.assertEqual(satellite_action, Canteen.Actions.NOTHING_SATELLITE_TELEDECLARED)

    @authenticate
    def test_get_canteens_with_purchases_no_diagnostics_for_year(self):
        """
        Return a list of canteens I manage who do have purchases for the given year,
        but have not yet created a diagnostic
        """
        year = 2023
        canteen_without_diag = CanteenFactory.create(managers=[authenticate.user])
        canteen_with_diag = CanteenFactory.create(managers=[authenticate.user])
        CanteenFactory.create(managers=[authenticate.user])  # canteen_without_purchases
        not_my_canteen = CanteenFactory.create()
        DiagnosticFactory.create(canteen=canteen_with_diag, year=year)
        PurchaseFactory.create(canteen=canteen_without_diag, date=f"{year}-01-01")
        # add second purchase to check canteen id deduplication
        PurchaseFactory.create(canteen=canteen_without_diag, date=f"{year}-12-01")
        PurchaseFactory.create(canteen=canteen_with_diag, date=f"{year}-01-01")
        PurchaseFactory.create(canteen=not_my_canteen, date=f"{year}-01-01")

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["undiagnosedCanteensWithPurchases"], [canteen_without_diag.id])

    @authenticate
    def test_filter_td_bad_sirets(self):
        """
        Check that canteens with SIRET issues (no SIRET, SIRET = central_producer_siret) have complete canteen actions and not TD actions
        """
        last_year = 2021
        canteen_central = CanteenFactory.create(
            siret="75665621899905",
            production_type=Canteen.ProductionType.CENTRAL,
        )
        # canteen not ok with diag
        canteen_with_no_siret = CanteenFactory.create(
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            city_insee_code="69123",
            managers=[authenticate.user],
        )
        Canteen.objects.filter(id=canteen_with_no_siret.id).update(siret=None)
        canteen_with_no_siret.refresh_from_db()
        DiagnosticFactory.create(canteen=canteen_with_no_siret, year=last_year, value_total_ht=10000)
        # canteen not ok with diag
        canteen_with_bad_central_siret = CanteenFactory.create(
            siret="59282615314394",
            central_producer_siret=canteen_central.siret,  # changed to 59282615314394 below
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
            city_insee_code="69123",
            managers=[authenticate.user],
        )
        Canteen.objects.filter(id=canteen_with_bad_central_siret.id).update(
            central_producer_siret=canteen_with_bad_central_siret.siret
        )
        canteen_with_bad_central_siret.refresh_from_db()
        DiagnosticFactory.create(canteen=canteen_with_bad_central_siret, year=last_year, value_total_ht=10000)
        # canteen ok without diag
        CanteenFactory.create(
            siret="55314169703815",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            city_insee_code="69123",
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        body = response.json()

        returned_canteens = body["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)
        self.assertEqual(returned_canteens[1]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

    def test_list_canteen_actions_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the canteens actions view
        """
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_single_canteen_actions(self):
        """
        Check that this endpoint can return the summary for a specified canteen
        """
        CanteenFactory.create(
            id=3,
            production_type=Canteen.ProductionType.ON_SITE,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], Canteen.Actions.CREATE_DIAGNOSTIC)

    @authenticate
    @freeze_time("2025-01-01")  # before the 2024 campaign
    def test_before_campaign_dates(self):
        complete = CanteenFactory.create(
            id=2,
            siret="21590350100017",
            city_insee_code="69123",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            managers=[authenticate.user],
        )
        last_year = 2024
        DiagnosticFactory.create(canteen=complete, year=last_year, value_total_ht=10000)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

        # last_year -1
        DiagnosticFactory.create(canteen=complete, year=last_year - 1, value_total_ht=10000)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year - 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

    @authenticate
    @freeze_time("2025-04-20")  # during the 2024 correction campaign
    def test_during_the_correction_campaign(self):
        complete = CanteenFactory.create(
            id=2,
            siret="21590350100017",
            city_insee_code="69123",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            managers=[authenticate.user],
        )
        last_year = 2024
        diagnostic = DiagnosticFactory.create(canteen=complete, year=last_year, value_total_ht=10000)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)  # not allowed to teledeclare

        # submit a teledeclaration during the campaign
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.NOTHING)

        # cancel the teledeclaration
        teledeclaration.cancel()

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.TELEDECLARE)  # allowed to teledeclare

    @authenticate
    @freeze_time("2025-12-30")  # after the 2024 campaign
    def test_after_campaign_dates(self):
        """
        Check that when we are after the campaign we don't return the teledeclaration action
        """
        canteen_td = CanteenFactory.create(
            id=2,
            siret="21590350100017",
            city_insee_code="69123",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            managers=[authenticate.user],
        )
        canteen_did_not_td = CanteenFactory.create(
            id=3,
            siret="21010034300016",
            city_insee_code="69123",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            managers=[authenticate.user],
        )
        last_year = 2024
        for canteen in [canteen_td, canteen_did_not_td]:
            DiagnosticFactory.create(canteen=canteen, year=last_year, value_total_ht=10000)
        Teledeclaration.create_from_diagnostic(
            Diagnostic.objects.get(canteen=canteen_td, year=last_year), authenticate.user
        )

        # canteen_td
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.NOTHING)

        # canteen_did_not_td (last_year)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

        # canteen_did_not_td (last_year + 1)
        DiagnosticFactory.create(canteen=canteen, year=last_year + 1, value_total_ht=10000)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": last_year + 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

    def test_get_retrieve_actionable_canteen_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the canteen actions view
        """
        CanteenFactory.create(id=3, production_type=Canteen.ProductionType.ON_SITE)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_retrieve_actionable_canteen_unauthorized(self):
        """
        If the user is not the manager, they will not be able to
        access the canteen actions view
        """
        CanteenFactory.create(id=3, production_type=Canteen.ProductionType.ON_SITE)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_actions_missing_line_ministry(self):
        """
        Even if the diagnostic is complete, the mandatory information on the canteen level should
        return a Canteen.Actions.FILL_CANTEEN_DATA if line ministry is not there
        """
        canteen = CanteenFactory.create(
            siret="96766910375238",
            city_insee_code="69123",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.ADMINISTRATION_PRISON, Sector.EDUCATION_PRIMAIRE],
            line_ministry=None,
            managers=[authenticate.user],
        )
        last_year = 2021
        DiagnosticFactory.create(year=last_year, canteen=canteen, value_total_ht=1000)
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

        # a canteen that has a line ministry should be complete
        canteen.line_ministry = Canteen.Ministries.AFFAIRES_ETRANGERES
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)

        # a canteen without a line ministry and without a sector that demands one is also complete
        canteen.line_ministry = None
        canteen.sector_list = [Sector.EDUCATION_PRIMAIRE]
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)
