from django.urls import reverse
from rest_framework.test import APITestCase
from data.factories import CanteenFactory, DiagnosticFactory, CompleteDiagnosticFactory
from data.models import Canteen, Diagnostic
from .utils import authenticate


# site diagnostics contain the data that concerns the site in question
# sometimes this data might come from a central kitchen
class TestSiteDiagnosticsApi(APITestCase):
    def _test_site_diagnostics_same_as_diagnostics(self, canteen):
        diagnostic = DiagnosticFactory.create(canteen=canteen, value_total_ht=1000, has_waste_diagnostic=True)

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))
        body = response.json()

        serialized_site_diagnostics = body.get("siteDiagnostics")
        self.assertEqual(len(serialized_site_diagnostics), 1)
        site_diagnostic = serialized_site_diagnostics[0]
        self.assertEqual(site_diagnostic["id"], diagnostic.id)
        self.assertNotIn("valueTotalHt", site_diagnostic)
        self.assertEqual(site_diagnostic["hasWasteDiagnostic"], True)

    @authenticate
    def test_fetch_for_site(self):
        """
        For a canteen that manages itself, site diagnostics are the same as their diagnostics
        with raw financial data removed
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_fetch_for_central_kitchen_no_site(self):
        """
        For a central kitchen without a site, site diagnostics are the same as their diagnostics
        with raw financial data removed
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_fetch_for_central_kitchen_with_site(self):
        """
        For a central kitchen with a site, site diagnostics are the same as their diagnostics
        with raw financial data removed
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_fetch_for_satellite_no_central(self):
        """
        For a satellite without a central kitchen, site diagnostics are the same as their diagnostics
        with raw financial data removed
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_provide_appro_percentages_for_simple_diagnostic_type(self):
        """
        Instead of asking the front to calculate percentages for simple diagnostic types,
        send them from the backend regardless of production type.
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        DiagnosticFactory.create(
            canteen=canteen, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE, value_total_ht=100, value_bio_ht=50
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))
        body = response.json()

        serialized_site_diagnostics = body.get("siteDiagnostics")
        site_diagnostic = serialized_site_diagnostics[0]
        self.assertEqual(site_diagnostic["percentageValueBioHt"], 0.5)

    @authenticate
    def test_provide_appro_percentages_for_complete_diagnostic_type(self):
        """
        For complete diagnostic types, send percentages of simple and complete values,
        regardless of production type
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = CompleteDiagnosticFactory.create(
            canteen=canteen,
            value_total_ht=10000,
            value_viandes_volailles_bio=0,
            value_produits_de_la_mer_bio=0,
            value_fruits_et_legumes_bio=2000,
            value_charcuterie_bio=3000,
            value_produits_laitiers_bio=0,
            value_boulangerie_bio=0,
            value_boissons_bio=0,
            value_autres_bio=0,
        )
        diagnostic.full_clean()
        diagnostic.save()

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))
        body = response.json()

        serialized_site_diagnostics = body.get("siteDiagnostics")
        site_diagnostic = serialized_site_diagnostics[0]
        self.assertEqual(site_diagnostic["percentageValueFruitsEtLegumesBio"], 0.2)
        self.assertEqual(site_diagnostic["percentageValueBioHt"], 0.5)
        self.assertNotIn("valueFruitsEtLegumesBio", site_diagnostic)
        self.assertNotIn("valueBioHt", site_diagnostic)

    @authenticate
    def test_fetch_for_satellite_central_all(self):
        """
        For a satellite with a central kitchen declaring all, satellite diagnostics are the same as
        central kitchen diagnostics, but with financial data masked
        """
        central = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="17756964123440")
        diagnostic = DiagnosticFactory.create(
            canteen=central,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            value_total_ht=1000,
            value_sustainable_ht=500,
            value_externality_performance_ht=200,
            has_waste_diagnostic=True,
        )
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="17756964123440"
        )
        canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))
        body = response.json()

        serialized_site_diagnostics = body.get("siteDiagnostics")
        self.assertEqual(len(serialized_site_diagnostics), 1)
        site_diagnostic = serialized_site_diagnostics[0]
        self.assertEqual(site_diagnostic["id"], diagnostic.id)
        self.assertEqual(site_diagnostic["canteenId"], central.id)  # TODO: how will this work for merged diags?
        self.assertEqual(site_diagnostic["percentageValueTotalHt"], 1)
        self.assertEqual(site_diagnostic["percentageValueSustainableHt"], 0.5)
        self.assertEqual(site_diagnostic["percentageValueExternalityPerformanceHt"], 0.2)
        self.assertEqual(site_diagnostic["hasWasteDiagnostic"], True)
        self.assertNotIn("valueTotalHt", site_diagnostic, "central kitchen financial data is masked")
        self.assertNotIn("valueSustainableHt", site_diagnostic, "central kitchen financial data is masked")
        self.assertNotIn("valueExternalityPerformanceHt", site_diagnostic, "central kitchen financial data is masked")

    @authenticate
    def test_fetch_for_satellite_central_appro_simple(self):
        """
        For a satellite with a central kitchen declaring simple appro data, site diagnostics should
        have masked central kitchen appro data, and satellite quali data
        """
        # add one quali field to CC to see that it is overridden
        # add one simple appro field to satellite to see that it is overridden
        # also check masking appro data
        pass

    @authenticate
    def test_fetch_for_satellite_central_appro_complete(self):
        """
        For a satellite with a central kitchen declaring simple appro data, site diagnostics should
        have masked central kitchen appro data, and satellite quali data
        """
        # add one quali field to CC to see that it is overridden
        # add one complete appro field to satellite to see that it is overridden
        # also check masking appro data
        # also test that there is some data that helps to identify the diagnostic as not belonging to the satellite
        pass

    @authenticate
    def test_fetch_for_satellite_no_data(self):
        """
        Even if data from target diag is None, should use that and not the data in the other diag
        """
        # create CC diag with quali data but no appro data
        # create satellite diag with appro data but no quali
        # site_diagnostic should contain all Nones
        pass

    @authenticate
    def test_fetch_mixed_site_diagnostics(self):
        """
        If a canteen changes status throughout the years, return the right site_diagnostic for each year
        """
        # year 1 : canteen site
        # year 2 : satellite with CC 1 appro
        # year 3 : satellite with CC 2 all
        # year 4 : central ?
        # year 5 : site
        pass
