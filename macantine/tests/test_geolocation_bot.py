import json

import requests_mock
from django.test import TestCase

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from common.api.decoupage_administratif import DECOUPAGE_ADMINISTRATIF_API_URL
from common.api.recherche_entreprises import fetch_geo_data_from_siret
from data.department_choices import Department
from data.factories import CanteenFactory, SectorFactory, UserFactory
from data.models import Canteen
from macantine import tasks


@requests_mock.Mocker()
class TestGeolocationUsingInseeCodeBot(TestCase):
    def test_number_of_api_calls(self, mock):
        """
        There should be one request for every canteens
        """
        manager = UserFactory.create()  # Avoids integrity errors from user creation
        sector = SectorFactory.create()
        for i in range(130):
            CanteenFactory.create(
                city=None,
                geolocation_bot_attempts=0,
                city_insee_code="69383",
                managers=[manager],
                sectors=[sector],
            )
        mock.get(
            f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes",
            text=json.dumps(
                [
                    {
                        "nom": "Grenoble",
                        "code": "38185",
                        "codeDepartement": "38",
                        "siren": "213801855",
                        "codeEpci": "200040715",
                        "codeRegion": "84",
                        "codesPostaux": ["38000", "38100"],
                        "population": 156389,
                    }
                ]
            ),
        )
        mock.get(
            f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis",
            text=json.dumps(
                [
                    {
                        "nom": "Grenoble-Alpes-Métropole",
                        "code": "200040715",
                        "codesDepartements": ["38"],
                        "codesRegions": ["84"],
                        "population": 449509,
                    }
                ]
            ),
        )
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        tasks.fill_missing_geolocation_data_using_insee_code()

        self.assertEqual(mock.call_count, 4)

    def test_geolocation_data_filled(self, mock):
        """
        Geolocation data should be filled with the response
        from the API
        """
        canteen = CanteenFactory.create(city_insee_code="38185", city=None, geolocation_bot_attempts=0)

        mock.get(
            f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes",
            text=json.dumps(
                [
                    {
                        "nom": "Grenoble",
                        "code": "38185",
                        "codeDepartement": "38",
                        "siren": "213801855",
                        "codeEpci": "200040715",
                        "codeRegion": "84",
                        "codesPostaux": ["38000", "38100"],
                        "population": 156389,
                    }
                ]
            ),
        )
        mock.get(
            f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis",
            text=json.dumps(
                [
                    {
                        "nom": "Grenoble-Alpes-Métropole",
                        "code": "200040715",
                        "codesDepartements": ["38"],
                        "codesRegions": ["84"],
                        "population": 449509,
                    }
                ]
            ),
        )
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        tasks.fill_missing_geolocation_data_using_insee_code()

        canteen.refresh_from_db()
        self.assertEqual(canteen.geolocation_bot_attempts, 1)  # incremented
        self.assertEqual(canteen.city, "Grenoble")
        self.assertEqual(canteen.city_insee_code, "38185")
        self.assertEqual(canteen.postal_code, "38000")  # filled
        self.assertEqual(canteen.epci, "200040715")  # filled
        self.assertEqual(canteen.epci_lib, "Grenoble-Alpes-Métropole")  # filled
        self.assertEqual(canteen.pat_list, ["1294"])  # filled
        self.assertEqual(canteen.pat_lib_list, ["PAT du Département de l'Isère"])  # filled
        self.assertEqual(canteen.department, "38")  # filled
        self.assertEqual(canteen.department_lib, "Isère")  # filled
        self.assertEqual(canteen.region, "84")  # filled
        self.assertEqual(canteen.region_lib, "Auvergne-Rhône-Alpes")  # filled
        self.assertEqual(canteen.geolocation_bot_attempts, 1)

    def test_candidate_canteens(self, _):
        """
        Only canteens with INSEE code
        that have not been queried more than ten times
        are considered candidates.
        Data that we want to recover is: city, postal code, department, region
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
        ]
        _ = [
            CanteenFactory.create(
                department=Department.ain,
                city="Une ville",
                geolocation_bot_attempts=1,
                postal_code="69003",
                city_insee_code=None,
            ),
            CanteenFactory.create(city=None, geolocation_bot_attempts=20, postal_code="69003"),
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

        result = list(tasks._get_candidate_canteens_for_insee_code_geobot())

        self.assertEqual(len(result), 3)
        for canteen in candidate_canteens:
            match = list(filter(lambda x: x.id == canteen.id, result))
            self.assertEqual(len(match), 1)

    def test_geolocation_bot_count(self, mock):
        """
        On every attempt, the geolocation bot count of the
        canteen increases, even if the API returns an error.
        """
        canteen = CanteenFactory.create(city=None, geolocation_bot_attempts=0, city_insee_code="69883")

        mock.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes", text="", status_code=403)
        mock.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis?fields=nom,code", text=json.dumps([]), status_code=403)
        mock_get_pat_dataset_resource(mock, success=False)
        mock_get_pat_csv(mock, success=False)

        tasks.fill_missing_geolocation_data_using_insee_code()

        canteen.refresh_from_db()
        self.assertEqual(canteen.geolocation_bot_attempts, 1)


@requests_mock.Mocker()
class TestGeolocationBotUsingSiret(TestCase):
    api_url = "https://recherche-entreprises.api.gouv.fr/search?etat_administratif=A&page=1&per_page=1&mtm_campaign=ma-cantine&q="

    def test_candidate_canteens(self, _):
        """
        Only canteens with no city_insee_code and with a SIRET
        """
        candidate_canteen = CanteenFactory.create(city_insee_code=None, siret="89394682276911")
        CanteenFactory.create(city_insee_code=29890)  # canteen with city_insee_code
        canteen_without_siret = CanteenFactory.create(city_insee_code=None)
        Canteen.objects.filter(id=canteen_without_siret.id).update(siret=None)  # override validations

        result = list(tasks._get_candidate_canteens_for_siret_to_insee_code_bot())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, candidate_canteen.id)

    def test_get_geo_data(self, mock):
        """
        Should retrieve geo info for a canteen that have a SIRET
        """
        siret_canteen = "89394682276911"
        candidate_canteen = CanteenFactory.create(city_insee_code=None, siret=siret_canteen)
        city_insee_code = "29352"

        mock.get(
            self.api_url + siret_canteen,
            text=json.dumps(
                {
                    "results": [
                        {
                            "siren": "923412845",
                            "nom_complet": "Wrong name",
                            "matching_etablissements": [
                                {
                                    "commune": "29352",
                                    "code_postal": "75001",
                                    "libelle_commune": "PARIS",
                                    "liste_enseignes": ["Foo"],
                                    "etat_administratif": "A",
                                }
                            ],
                        }
                    ],
                    "total_results": 1,
                },
            ),
            status_code=200,
        )
        response = fetch_geo_data_from_siret(candidate_canteen.siret)
        self.assertEqual(response["cityInseeCode"], city_insee_code)

    def test_geolocation_with_siret_data_filled(self, mock):
        """
        Geolocation data should be filled with the response
        from the API
        """
        siret_canteen = "89394682276911"
        canteen = CanteenFactory.create(city_insee_code=None, siret=siret_canteen)
        city_insee_code = "29352"
        code_postal = "29890"
        mock.get(
            self.api_url + siret_canteen,
            text=json.dumps(
                {
                    "results": [
                        {
                            "siren": "923412845",
                            "nom_complet": "A Name",
                            "matching_etablissements": [
                                {
                                    "commune": city_insee_code,
                                    "code_postal": code_postal,
                                    "libelle_commune": "PARIS",
                                    "liste_enseignes": ["Foo"],
                                    "etat_administratif": "A",
                                }
                            ],
                        }
                    ],
                    "total_results": 1,
                },
            ),
            status_code=200,
        )

        tasks.fill_missing_insee_code_using_siret()

        canteen.refresh_from_db()
        self.assertEqual(canteen.city_insee_code, city_insee_code)
        self.assertEqual(canteen.postal_code, None)  # will be filled by the geo bot
