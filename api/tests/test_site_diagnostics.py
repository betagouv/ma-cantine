from django.urls import reverse
from rest_framework.test import APITestCase
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen
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
        self.assertEqual(site_diagnostic["valueTotalHt"], 1000)
        self.assertEqual(site_diagnostic["hasWasteDiagnostic"], True)

    @authenticate
    def test_fetch_for_site(self):
        """
        For a canteen that manages itself, site diagnostics are the same as their diagnostics
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_fetch_for_central_kitchen_no_site(self):
        """
        For a central kitchen without a site, site diagnostics are the same as their diagnostics
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_fetch_for_central_kitchen_with_site(self):
        """
        For a central kitchen with a site, site diagnostics are the same as their diagnostics
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_fetch_for_satellite_no_central(self):
        """
        For a satellite without a central kitchen, site diagnostics are the same as their diagnostics
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        canteen.managers.add(authenticate.user)

        self._test_site_diagnostics_same_as_diagnostics(canteen)

    @authenticate
    def test_fetch_for_satellite_central_all(self):
        """
        For a satellite with a central kitchen declaring all, satellite diagnostics are the same as
        central kitchen diagnostics
        """
        pass

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
