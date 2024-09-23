import json

import requests_mock
from django.test import TestCase

from data.department_choices import Department
from data.factories import CanteenFactory, SectorFactory, UserFactory
from macantine import tasks, utils


@requests_mock.Mocker()
class TestGeolocationBot(TestCase):
    api_url = "https://api-adresse.data.gouv.fr/search/csv/"

    def test_number_of_api_calls(self, mock):
        """
        There should be one request for every 70 canteens
        """
        manager = UserFactory.create()  # Avoids integrity errors from user creation
        sector = SectorFactory.create()
        for i in range(130):
            CanteenFactory.create(
                city=None,
                geolocation_bot_attempts=0,
                postal_code="69003",
                managers=[manager],
                sectors=[sector],
            )

        address_api_text = "id,citycode,postcode,result_citycode,result_postcode,result_city,result_context\n"
        address_api_text += '21340172201787,,11111,00000,11111,Ma ville,"01,Something,Other"\n'
        mock.post(self.api_url, text=address_api_text)

        tasks.fill_missing_geolocation_data_using_insee_code_or_postcode()

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

        tasks.fill_missing_geolocation_data_using_insee_code_or_postcode()

        canteen.refresh_from_db()
        self.assertEqual(canteen.city, "Lyon")
        self.assertEqual(canteen.city_insee_code, "69383")
        self.assertEqual(canteen.postal_code, "69003")
        self.assertEqual(canteen.department, "69")
        self.assertEqual(canteen.geolocation_bot_attempts, 1)

    def test_candidate_canteens(self, _):
        """
        Only canteens with either postal code or INSEE code
        that have not been queried more than ten times
        are considered candidates.
        Data that we want to recover is: city, department, INSEE, postal code
        """
        candidate_canteens = [
            CanteenFactory.create(city=None, geolocation_bot_attempts=0, postal_code="69003", city_insee_code="69383"),
            CanteenFactory.create(
                department=None, geolocation_bot_attempts=9, postal_code="69003", city_insee_code="69383"
            ),
            CanteenFactory.create(
                department=Department.ain,
                city="Une ville",
                geolocation_bot_attempts=4,
                postal_code=None,
                city_insee_code="69883",
            ),
            CanteenFactory.create(
                department=Department.ain,
                city="Une ville",
                geolocation_bot_attempts=1,
                postal_code="69003",
                city_insee_code=None,
            ),
        ]
        _ = [
            CanteenFactory.create(city=None, geolocation_bot_attempts=10, postal_code="69003"),
            CanteenFactory.create(
                city=None,
                geolocation_bot_attempts=0,
                postal_code="69",
                city_insee_code=None,
            ),
            CanteenFactory.create(
                city=None,
                geolocation_bot_attempts=0,
                city_insee_code="6009",
                postal_code=None,
            ),
            CanteenFactory.create(
                department=None,
                geolocation_bot_attempts=1,
                city_insee_code=None,
                postal_code=None,
            ),
        ]
        result = list(tasks._get_candidate_canteens_for_code_geobot())
        self.assertEqual(len(result), 4)
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

        tasks.fill_missing_geolocation_data_using_insee_code_or_postcode()

        canteen.refresh_from_db()
        self.assertEqual(canteen.geolocation_bot_attempts, 1)


@requests_mock.Mocker()
class TestGeolocationWithSiretBot(TestCase):
    api_url = "https://api.insee.fr/entreprises/sirene/siret/"

    def test_candidate_canteens(self, _):
        """
        Only canteens with no city_insee_code and with a SIRET
        """
        candidate_canteen = CanteenFactory.create(city_insee_code=None, siret="89394682276911")
        _ = [
            CanteenFactory.create(city_insee_code=29890),
            CanteenFactory.create(city_insee_code=None, siret=None),
        ]
        result = list(tasks._get_candidate_canteens_for_siret_geobot())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, candidate_canteen.id)

    def test_get_geo_data(self, mock):
        """
        Should retrieve geo info for a canteen that have a SIRET
        """
        siret_canteen = "89394682276911"
        token = "Fake token"
        candidate_canteen = CanteenFactory.create(city_insee_code=None, siret=siret_canteen)
        # Call the service to hit the mocked API.
        mock.post(
            "https://api.insee.fr/token",
            json={"token_type": "bearer", "access_token": token},
        )
        city_insee_code = "29352"

        mock.get(
            self.api_url + siret_canteen,
            headers={"Authorization": f"Bearer {token}"},
            text=json.dumps(
                {
                    "etablissement": {
                        "uniteLegale": {"denominationUniteLegale": "cantine test"},
                        "adresseEtablissement": {
                            "codeCommuneEtablissement": city_insee_code,
                            "codePostalEtablissement": "29890",
                            "libelleCommuneEtablissement": "Ville test",
                        },
                    },
                }
            ),
            status_code=200,
        )
        response = utils.fetch_geo_data_from_api_insee_sirene_by_siret(candidate_canteen.siret, {}, token)
        self.assertEquals(response["cityInseeCode"], city_insee_code)

    def test_geolocation_with_siret_data_filled(self, mock):
        """
        Geolocation data should be filled with the response
        from the API
        """
        token = "Fake token"
        siret_canteen = "89394682276911"
        canteen = CanteenFactory.create(city_insee_code=None, siret=siret_canteen)
        mock.post(
            "https://api.insee.fr/token",
            json={"token_type": "bearer", "access_token": token},
        )

        city_insee_code = "29352"

        mock.get(
            self.api_url + siret_canteen,
            headers={"Authorization": f"Bearer {token}"},
            text=json.dumps(
                {
                    "etablissement": {
                        "uniteLegale": {"denominationUniteLegale": "cantine test"},
                        "adresseEtablissement": {
                            "codeCommuneEtablissement": city_insee_code,
                            "codePostalEtablissement": "29890",
                            "libelleCommuneEtablissement": "Ville test",
                        },
                    },
                }
            ),
            status_code=200,
        )

        tasks.fill_missing_geolocation_data_using_siret()

        canteen.refresh_from_db()
        self.assertEqual(canteen.city_insee_code, "29352")
        self.assertEqual(canteen.postal_code, "29890")
