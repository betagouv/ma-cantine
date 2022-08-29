import requests_mock
from django.test import TestCase
from data.factories import CanteenFactory
from macantine import tasks


@requests_mock.Mocker()
class TestGeolocationBot(TestCase):
    api_url = "https://api-adresse.data.gouv.fr/search/csv/"

    def test_number_of_api_calls(self, mock):
        """
        There should be one request for every 50 canteens
        """
        for i in range(75):
            CanteenFactory.create(city=None, geolocation_bot_attempts=0, postal_code="69003")

        address_api_text = "id,citycode,postcode,result_citycode,result_postcode,result_city,result_context\n"
        address_api_text += '21340172201787,,11111,00000,11111,Ma ville,"01,Something,Other"\n'
        mock.post(self.api_url, text=address_api_text)

        tasks.fill_missing_geolocation_data()

        self.assertEqual(mock.call_count, 2)

    def test_geolocation_data_filled(self, mock):
        """
        Geolocation data should be filled with the response
        from the API
        """
        canteen = CanteenFactory.create(city=None, geolocation_bot_attempts=0, postal_code="69003")
        address_api_text = "id,citycode,postcode,result_citycode,result_postcode,result_city,result_context\n"
        address_api_text += f'{canteen.id},,69003,69383,69003,Lyon,"69, Rhône, Auvergne-Rhône-Alpes"\n'
        mock.post(self.api_url, text=address_api_text)

        tasks.fill_missing_geolocation_data()

        canteen.refresh_from_db()
        self.assertEqual(canteen.city, "Lyon")
        self.assertEqual(canteen.city_insee_code, "69383")
        self.assertEqual(canteen.postal_code, "69003")
        self.assertEqual(canteen.department, "69")
        self.assertEqual(canteen.geolocation_bot_attempts, 1)

    def test_candidate_canteens(self, _):
        """
        Only canteens with either postal code or INSEE code
        that have not been queried more than three times
        are considered candidates
        """
        candidate_canteens = [
            CanteenFactory.create(city=None, geolocation_bot_attempts=0, postal_code="69003"),
            CanteenFactory.create(department=None, geolocation_bot_attempts=2, city_insee_code="69383"),
            CanteenFactory.create(department=None, geolocation_bot_attempts=1, city_insee_code="69383"),
        ]
        _ = [
            CanteenFactory.create(city=None, geolocation_bot_attempts=3, postal_code="69003"),
            CanteenFactory.create(department="69", city="Lyon", geolocation_bot_attempts=2),
            CanteenFactory.create(department=None, geolocation_bot_attempts=1, city_insee_code=None, postal_code=None),
        ]
        result = list(tasks._get_candidate_canteens())
        self.assertEqual(len(result), 3)
        for canteen in candidate_canteens:
            match = list(filter(lambda x: x.id == canteen.id, result))
            self.assertEqual(len(match), 1)

    def test_geolocation_bot_count(self, mock):
        """
        On every attempt, the geolocation bot count of the
        canteen increases, even if the API returns an error.
        """
        canteen = CanteenFactory.create(city=None, geolocation_bot_attempts=0, postal_code="69003")
        mock.post(self.api_url, text="", status_code=403)

        tasks.fill_missing_geolocation_data()

        canteen.refresh_from_db()
        self.assertEqual(canteen.geolocation_bot_attempts, 1)
