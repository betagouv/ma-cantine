from rest_framework.test import APITestCase
from data.factories import CanteenFactory
from .utils import authenticate


# site diagnostics contain the data that concerns the site in question
# sometimes this data might come from a central kitchen
class TestSiteDiagnosticsApi(APITestCase):
    def _create_canteen_for_user(user, canteen_data={}):
        canteen = CanteenFactory.create(**canteen_data)
        canteen.managers.add(authenticate.user)
        return canteen

    @authenticate
    def test_fetch_for_site(self):
        """
        For a canteen that manages itself, site diagnostics are the same as their diagnostics
        """
        pass

    @authenticate
    def test_fetch_for_central_kitchen_no_site(self):
        """
        For a central kitchen without a site, site diagnostics are the same as their diagnostics
        """
        pass

    @authenticate
    def test_fetch_for_central_kitchen_with_site(self):
        """
        For a central kitchen with a site, site diagnostics are the same as their diagnostics
        """
        pass

    @authenticate
    def test_fetch_for_satellite_no_central(self):
        """
        For a satellite without a central kitchen, site diagnostics are the same as their diagnostics
        """
        pass

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
