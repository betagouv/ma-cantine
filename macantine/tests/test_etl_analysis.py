import json

import numpy as np
import pandas as pd
import pytest
from django.test import TestCase
from freezegun import freeze_time

from api.serializers import DiagnosticTeledeclaredAnalysisSerializer
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector
from macantine.etl.analysis import ETL_ANALYSIS_CANTEEN, ETL_ANALYSIS_TELEDECLARATIONS, aggregate_col
from macantine.etl.utils import format_td_sector_column, get_objectif_zone_geo
from macantine.tests.test_etl_common import setUpTestData as ETLCommonSetUpTestData
from macantine.utils import TELEDECLARATION_CURRENT_VERSION


class CanteenETLAnalysisTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls)

    def test_canteen_extract(self):
        self.assertEqual(Canteen.all_objects.count(), 7)
        self.assertEqual(Canteen.objects.count(), 6)  # 1 is deleted

        etl = ETL_ANALYSIS_CANTEEN()

        self.assertEqual(etl.len_dataset(), 0)  # before extraction

        etl.extract_dataset()

        self.assertEqual(etl.len_dataset(), 6)  # 1 is deleted
        self.assertEqual(
            etl.get_dataset().iloc[0]["id"], self.canteen_site_earlier.id
        )  # Order by created date ascending

    def test_canteen_transform(self):
        schema = json.load(open("data/schemas/export_analysis/schema_cantines.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        etl = ETL_ANALYSIS_CANTEEN()
        etl.extract_dataset()
        etl.transform_dataset()

        # Check the schema matching
        self.assertEqual(len(etl.df.columns), len(schema_cols))
        self.assertEqual(set(etl.df.columns), set(schema_cols))

        # Check the generated columns
        canteen_site = etl.df[etl.df.id == self.canteen_site.id].iloc[0]
        self.assertEqual(canteen_site["epci"], "200040715")
        self.assertEqual(canteen_site["epci_lib"], "Grenoble-Alpes-Métropole")
        self.assertEqual(canteen_site["pat_liste"], "1294,1295")
        self.assertEqual(
            canteen_site["pat_lib_liste"],
            "PAT du Département de l'Isère,Projet Alimentaire inter Territorial de la Grande région grenobloise",
        )
        self.assertEqual(canteen_site["departement"], "38")
        self.assertEqual(canteen_site["departement_lib"], "Isère")
        self.assertEqual(canteen_site["region"], "84")
        self.assertEqual(canteen_site["region_lib"], "Auvergne-Rhône-Alpes")
        self.assertEqual(canteen_site["type_gestion"], "Directe")
        self.assertEqual(canteen_site["type_production"], "Restaurant avec cuisine sur place")
        self.assertEqual(canteen_site["modele_economique"], "Public")
        self.assertEqual(canteen_site["secteur"], "Hôpitaux,Crèche")
        self.assertEqual(canteen_site["categorie"], "Santé,Social / Médico-social")
        self.assertEqual(canteen_site["ministere_tutelle"], None)
        self.assertEqual(canteen_site["spe"], "Non")
        self.assertEqual(str(canteen_site["declaration_donnees_2022"]), "True")
        self.assertEqual(str(canteen_site["declaration_donnees_2025"]), "False")
        self.assertEqual(canteen_site["adresses_gestionnaires"], "gestionnaire1@example.com,gestionnaire2@example.com")

        canteen_site_armee = etl.df[etl.df.id == self.canteen_site_armee.id].iloc[0]
        self.assertEqual(canteen_site_armee["secteur"], "Restaurants des prisons")
        self.assertEqual(canteen_site_armee["categorie"], "Administration")
        self.assertEqual(canteen_site_armee["ministere_tutelle"], "Armées")
        self.assertEqual(canteen_site_armee["spe"], "Oui")  # because line_ministry is set

        canteen_site_without_manager = etl.df[etl.df.id == self.canteen_site_without_manager.id].iloc[0]
        self.assertEqual(canteen_site_without_manager["adresses_gestionnaires"], "")

        canteen_satellite = etl.df[etl.df.id == self.canteen_satellite.id].iloc[0]
        self.assertEqual(canteen_satellite["groupe_id"], self.canteen_groupe.id)


class TeledeclarationETLAnalysisTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls, with_diagnostics=True)

    def test_teledeclaration_extract(self):
        # all years combined
        # 2022: 3 teledeclarations (1 groupe with 1 satellite)
        # 2023: 1 teledeclaration (1 is cancelled, 1 armee)
        # 2024: 1 teledeclaration
        etl_td = ETL_ANALYSIS_TELEDECLARATIONS()
        etl_td.extract_dataset()

        self.assertEqual(etl_td.len_dataset(), 3 + 1 + 1)
        self.assertEqual(
            etl_td.df.iloc[0]["id"], self.canteen_site_earlier_diagnostic_2022.teledeclaration_id
        )  # Order by teledeclaration created date ascending

    def test_teledeclaration_transform(self):
        schema = json.load(open("data/schemas/export_analysis/schema_teledeclarations.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        etl_td = ETL_ANALYSIS_TELEDECLARATIONS()
        etl_td.extract_dataset()
        etl_td.transform_dataset()

        # Check the schema matching
        self.assertEqual(len(etl_td.df.columns), len(schema_cols))
        self.assertEqual(set(etl_td.df.columns), set(schema_cols))

        canteen_site_diagnostic_2024 = etl_td.df[etl_td.df.id == self.canteen_site_diagnostic_2024.teledeclaration_id][
            etl_td.df.year == 2024
        ].iloc[0]
        self.assertEqual(canteen_site_diagnostic_2024["id"], self.canteen_site_diagnostic_2024.teledeclaration_id)
        self.assertEqual(canteen_site_diagnostic_2024["year"], 2024)
        self.assertEqual(canteen_site_diagnostic_2024["version"], str(TELEDECLARATION_CURRENT_VERSION))
        self.assertEqual(canteen_site_diagnostic_2024["email"], self.canteen_site_manager_1.email)
        self.assertEqual(canteen_site_diagnostic_2024["canteen_id"], self.canteen_site.id)
        self.assertEqual(canteen_site_diagnostic_2024["siret"], "21380185500015")
        self.assertEqual(canteen_site_diagnostic_2024["name"], "Cantine")
        self.assertEqual(canteen_site_diagnostic_2024["central_producer_siret"], None)
        self.assertEqual(canteen_site_diagnostic_2024["secteur"], "Hôpitaux,Crèche")
        self.assertEqual(canteen_site_diagnostic_2024["categorie"], "Santé,Social / Médico-social")
        self.assertEqual(canteen_site_diagnostic_2024["line_ministry"], None)
        self.assertGreater(
            canteen_site_diagnostic_2024["ratio_bio"],
            0,
            "The bio value is aggregated from bio fields and should be greater than 0",
        )

        canteen_groupe_diagnostic_2022_satellite = etl_td.df[etl_td.df.canteen_id == self.canteen_satellite.id][
            etl_td.df.year == 2022
        ].iloc[0]
        self.assertEqual(
            canteen_groupe_diagnostic_2022_satellite["id"], self.canteen_groupe_diagnostic_2022.teledeclaration_id
        )
        self.assertEqual(
            canteen_groupe_diagnostic_2022_satellite["secteur"], "Ecole primaire (maternelle et élémentaire)"
        )
        self.assertEqual(canteen_groupe_diagnostic_2022_satellite["categorie"], "Enseignement")

    def test_get_egalim_sans_bio(self):
        test_cases = [
            {
                "name": "1",
                "date_mocked": "2023-03-30",  # during the 2022 campai
                "year": 2022,
                "data": {
                    "valeur_totale": 100,
                    "valeur_bio_agg": 0,
                    "valeur_externalites_performance_agg": 10,
                    "valeur_siqo_agg": 10,
                    "valeur_egalim_autres_agg": 10,
                },
                "expected_outcome": 30,
            },
            {
                "name": "2",
                "date_mocked": "2023-03-30",  # during the 2022 campai
                "year": 2022,
                "data": {
                    "valeur_totale": 100,
                    "valeur_bio_agg": 0,
                    "valeur_externalites_performance_agg": 10,
                    "valeur_siqo_agg": 10,
                    "valeur_egalim_autres_agg": None,
                },
                "expected_outcome": 20,
            },
        ]

        for tc in test_cases:
            canteen = CanteenFactory()
            with freeze_time(tc["date_mocked"]):  # Faking time to mock creation_date
                diagnostic = DiagnosticFactory(
                    canteen=canteen,
                    year=tc["year"],
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                    valeur_totale=tc["data"]["valeur_totale"],
                    valeur_bio=tc["data"]["valeur_bio_agg"],
                    valeur_siqo=tc["data"]["valeur_siqo_agg"],
                    valeur_externalites_performance=tc["data"]["valeur_externalites_performance_agg"],
                    valeur_egalim_autres=tc["data"]["valeur_egalim_autres_agg"],
                )
                diagnostic.teledeclare(applicant=UserFactory())

                self.serializer_data = {
                    "valeur_totale": tc["data"]["valeur_totale"],
                    "valeur_bio": tc["data"]["valeur_bio_agg"],
                    "valeur_externalites_performance": tc["data"]["valeur_externalites_performance_agg"],
                    "valeur_siqo": tc["data"]["valeur_siqo_agg"],
                    "valeur_egalim_autres": tc["data"]["valeur_egalim_autres_agg"],
                }

                self.serializer = DiagnosticTeledeclaredAnalysisSerializer(
                    instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
                )
                data = self.serializer.data
                self.assertEqual(int(data["ratio_egalim_sans_bio"]), tc["expected_outcome"])

    def test_aggregate_col(self):
        test_cases = [
            {
                "name": "Regular aggregation",
                "data": {
                    "0": {
                        "id": 1,
                        "valeur_bio": pd.NA,
                        "valeur_bio_boulange": 5,
                        "valeur_bio_viande": 5,
                    }
                },
                "categ": "bio",
                "sub_categ": ["_bio"],
                "expected_outcome": 10,
            },
            {
                "name": "No double count by exluding potential aggregated value from sum",
                "data": {
                    "0": {
                        "id": 1,
                        "valeur_bio": 5,
                        "valeur_bio_boulange": 5,
                        "valeur_bio_viande": 5,
                    }
                },
                "categ": "bio",
                "sub_categ": ["_bio"],
                "expected_outcome": 10,
            },
            {
                "name": "Multiple sub categ",
                "data": {
                    "0": {
                        "id": 1,
                        "valeur_bio": pd.NA,
                        "valeur_bio_boulange": 5,
                        "valeur_bio_viande": 5,
                        "valeur_awesome_viande": 5,
                    }
                },
                "categ": "bio",
                "sub_categ": ["_bio", "_awesome"],
                "expected_outcome": 15,
            },
        ]
        for tc in test_cases:
            td_complete = pd.DataFrame.from_dict(tc["data"], orient="index")
            td_aggregated = aggregate_col(td_complete, tc["categ"], tc["sub_categ"])
            self.assertEqual(td_aggregated.iloc[0][f"teledeclaration.valeur_{tc['categ']}"], tc["expected_outcome"])

    def test_check_column_matches_substring(self):
        data = {
            "0": {
                "id": 1,
            }
        }
        df = pd.DataFrame.from_dict(data, orient="index")
        with self.assertRaises(KeyError):
            aggregate_col(df, "categ_A", ["_non_existing_sub_categ"])

    def test_transform_sector_column(self):
        data = {
            "0": {
                "canteen_id": 1,
                "canteen.sectors": [
                    {
                        "id": 12,
                        "name": "Ecole primaire (maternelle et élémentaire)",
                        "category": "education",
                        "has_line_ministry": False,
                    }
                ],
            },
            "1": {
                "canteen_id": 2,
                "canteen.sectors": [
                    {
                        "id": 1,
                        "name": "Secondaire collège",
                    },
                    {
                        "id": 12,
                        "name": "Ecole primaire (maternelle et élémentaire)",
                    },
                    {
                        "id": 28,
                        "name": "Secondaire lycée (hors agricole)",
                    },
                ],
            },
            "2": {
                "canteen_id": 2,
                "canteen.sectors": None,
            },
        }
        df = pd.DataFrame.from_dict(data, orient="index")
        df[["secteur", "categorie"]] = df.apply(
            lambda x: format_td_sector_column(x, "canteen.sectors"), axis=1, result_type="expand"
        )
        self.assertEqual(df.iloc[0]["secteur"], "Ecole primaire (maternelle et élémentaire)")
        self.assertEqual(df.iloc[0]["categorie"], "education")
        self.assertEqual(df.iloc[1]["secteur"], "Secteurs multiples")
        self.assertEqual(df.iloc[1]["categorie"], "Catégories multiples")

    def test_cout_denrees(self):
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_ok = CanteenFactory(daily_meal_count=10, yearly_meal_count=2000)
            diagnostic = DiagnosticFactory(canteen=canteen_ok, year=2022, valeur_totale=1000)
            diagnostic.teledeclare(applicant=UserFactory())

            self.serializer_data = {
                "yearly_meal_count": canteen_ok.yearly_meal_count,
                "valeur_totale": diagnostic.valeur_totale,
            }
            self.serializer = DiagnosticTeledeclaredAnalysisSerializer(
                instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
            )
            data = self.serializer.data

            self.assertEqual(data["cout_denrees"], 0.5)

        with freeze_time("2022-08-30"):  # during the 2021 campaign
            canteen_invalid_yearly_meal_count = CanteenFactory(daily_meal_count=10, yearly_meal_count=2000)
            canteen_invalid_yearly_meal_count.yearly_meal_count = 0  # invalid data
            canteen_invalid_yearly_meal_count.save(skip_validations=True)
            canteen_invalid_yearly_meal_count.refresh_from_db()
            diagnostic = DiagnosticFactory(canteen=canteen_invalid_yearly_meal_count, year=2021, valeur_totale=1000)
            diagnostic.teledeclare(applicant=UserFactory(), skip_validations=True)

            self.serializer_data = {
                "yearly_meal_count": canteen_invalid_yearly_meal_count.yearly_meal_count,
                "valeur_totale": diagnostic.valeur_totale,
            }
            self.serializer = DiagnosticTeledeclaredAnalysisSerializer(
                instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
            )
            data = self.serializer.data

            self.assertEqual(data["cout_denrees"], -1)

    def test_geo_columns(self):
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_with_geo_data = CanteenFactory(
                department="38",
                department_lib="Isère",
                region="84",
                region_lib="Auvergne-Rhône-Alpes",
                epci="200040715",
                epci_lib="Grenoble-Alpes-Métropole",
            )
            diagnostic = DiagnosticFactory(canteen=canteen_with_geo_data, year=2022)
            diagnostic.teledeclare(applicant=UserFactory())

        self.serializer = DiagnosticTeledeclaredAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
        )
        data = self.serializer.data

        self.assertEqual(data["departement"], "38")
        self.assertEqual(data["lib_departement"], "Isère")
        self.assertEqual(data["region"], "84")
        self.assertEqual(data["lib_region"], "Auvergne-Rhône-Alpes")

        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_half_geo_data = CanteenFactory(
                department="38",
                department_lib=None,
                region="84",
                region_lib=None,
                epci="200040715",
                epci_lib=None,
            )
            diagnostic_half_geo = DiagnosticFactory(canteen=canteen_half_geo_data, year=2022)
            diagnostic_half_geo.teledeclare(applicant=UserFactory())

        self.serializer_half_geo = DiagnosticTeledeclaredAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic_half_geo.id)
        )
        data = self.serializer_half_geo.data

        self.assertEqual(data["departement"], "38")
        self.assertEqual(data["lib_departement"], "Isère")  # filled with the serializer
        self.assertEqual(data["region"], "84")
        self.assertEqual(data["lib_region"], "Auvergne-Rhône-Alpes")  # filled with the serializer

        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_without_geo_data = CanteenFactory(
                department=None,
                department_lib=None,
                region=None,
                region_lib=None,
                epci=None,
                epci_lib=None,
            )
            diagnostic_without_geo = DiagnosticFactory(canteen=canteen_without_geo_data, year=2022)
            diagnostic_without_geo.teledeclare(applicant=UserFactory())

        self.serializer_without_geo = DiagnosticTeledeclaredAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic_without_geo.id)
        )
        data_no_geo = self.serializer_without_geo.data

        self.assertEqual(data_no_geo["departement"], None)
        self.assertEqual(data_no_geo["lib_departement"], None)
        self.assertEqual(data_no_geo["region"], None)
        self.assertEqual(data_no_geo["lib_region"], None)

    def test_line_ministry_and_spe(self):
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_with_line_ministry = CanteenFactory(
                line_ministry=Canteen.Ministries.AGRICULTURE,
                sector_list=[Sector.ADMINISTRATION_ARMEE],
                economic_model=Canteen.EconomicModel.PUBLIC,
            )
            diagnostic = DiagnosticFactory(canteen=canteen_with_line_ministry, year=2022)
            diagnostic.teledeclare(applicant=UserFactory())

        self.serializer = DiagnosticTeledeclaredAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
        )
        data = self.serializer.data

        self.assertEqual(data["line_ministry"], Canteen.Ministries.AGRICULTURE)
        self.assertEqual(data["spe"], "Oui")

        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_without_line_ministry = CanteenFactory(line_ministry=None)
            diagnostic_without_line_ministry = DiagnosticFactory(canteen=canteen_without_line_ministry, year=2022)
            diagnostic_without_line_ministry.teledeclare(applicant=UserFactory())

        self.serializer_without_line_ministry = DiagnosticTeledeclaredAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic_without_line_ministry.id)
        )
        data_without_line_ministry = self.serializer_without_line_ministry.data

        self.assertEqual(data_without_line_ministry["line_ministry"], None)
        self.assertEqual(data_without_line_ministry["spe"], "Non")

    def test_flatten_td(self):
        data = {
            "id": {2: 1, 3: 2, 4: 3, 5: 4},
            "year": {2: 2024, 3: 2024, 4: 2024, 5: 2025},
            "canteen_id": {2: 1, 3: 2, 4: 3, 5: 4},
            "name": {2: "Cantine A", 3: "Cantine B", 4: "Cantine C", 5: "Cantine D"},
            "siret": {2: "siretA", 3: "siretB", 4: "siretC", 5: "siretD"},
            "daily_meal_count": {2: 38.0, 3: None, 4: None, 5: None},
            "yearly_meal_count": {2: 10, 3: 100, 4: 300, 5: 400},
            "production_type": {2: "site", 3: "central", 4: "central_serving", 5: "groupe"},
            "cuisine_centrale": {2: "B) non", 3: "A) oui", 4: "A) oui", 5: "B) oui"},
            "central_producer_siret": {2: None, 3: None, 4: None, 5: None},
            "diagnostic_type": {2: None, 3: None, 4: None, 5: None},
            "satellite_canteens_count": {2: None, 3: 206.0, 4: 2, 5: 1},
            "valeur_totale": {2: 100, 3: 1000, 4: 1500, 5: 2000},
            "valeur_bio": {2: None, 3: 100, 4: 0, 5: 0},
            "tmp_satellites": {
                2: None,
                3: [
                    {
                        "id": 20,
                        "name": "SAT 1",
                        "siret": "21930055500196",
                        "yearly_meal_count": 60,
                        "sectors": [{"name": "Secteur A"}, {"name": "Secteur B"}],
                    },
                    {
                        "id": 21,
                        "name": "SAT 2",
                        "siret": "21930055500188",
                        "yearly_meal_count": 40,
                    },
                ],
                4: [
                    {
                        "id": 30,
                        "name": "SATELLITE 1",
                        "siret": "31930055500123",
                        "yearly_meal_count": 120,
                    },
                    {
                        "id": 31,
                        "name": "SATELLITE 2",
                        "siret": "31930055500456",
                        "yearly_meal_count": None,
                    },
                ],
                5: [
                    {
                        "id": 40,
                        "name": "SATELLITE 1",
                        "siret": "21340172201787",
                        "yearly_meal_count": 120,
                    },
                ],
            },
        }

        etl = ETL_ANALYSIS_TELEDECLARATIONS()
        etl.df = pd.DataFrame.from_dict(data)
        etl.flatten_central_kitchen_td()
        # site
        self.assertTrue(np.isnan(etl.df[etl.df.canteen_id == 1].iloc[0].valeur_bio))  # Nulls are processed as nulls
        self.assertEqual(
            len(etl.df[etl.df.canteen_id.isin([2, 3, 4])]), 0
        )  # groupe, central & central_serving filtered out
        # central
        self.assertEqual(len(etl.df[etl.df.canteen_id == 20]), 1)
        self.assertEqual(etl.df[etl.df.canteen_id == 20].iloc[0].valeur_totale, 500)  # Appro value split
        self.assertEqual(etl.df[etl.df.canteen_id == 20].iloc[0].secteur, "Secteur A,Secteur B")  # Appro value split
        # central_serving
        self.assertEqual(etl.df[etl.df.canteen_id == 30].iloc[0].valeur_totale, 750)  # Appro value split
        self.assertEqual(etl.df[etl.df.canteen_id == 31].iloc[0].valeur_totale, 750)  # Appro value split
        self.assertEqual(etl.df[etl.df.canteen_id == 31].iloc[0].yearly_meal_count, 300 / 2)
        self.assertEqual(
            etl.df[etl.df.canteen_id == 30].iloc[0].valeur_bio, 0
        )  # Zeros are processed as zeros and not nulls
        # groupe
        self.assertEqual(etl.df[etl.df.canteen_id == 40].iloc[0].valeur_totale, 2000)  # 1 satellite, no split

    def test_delete_duplicates_cc_csat_with_duplicates(self):
        etl_instance = ETL_ANALYSIS_TELEDECLARATIONS()
        etl_instance.df = pd.DataFrame(
            {
                "id": [10, 20, 30],
                "canteen_id": [1, 1, 2],
                "year": [2023, 2023, 2023],
                "genere_par_cuisine_centrale": [
                    True,
                    False,
                    True,
                ],
                "other_column": [10, 20, 30],
            }
        )
        etl_instance.delete_duplicates_cc_csat()
        assert len(etl_instance.df) == 2
        assert etl_instance.df.iloc[0]["id"] == 10

    def test_delete_duplicates_cc_csat_no_duplicates(self):
        etl_instance = ETL_ANALYSIS_TELEDECLARATIONS()
        etl_instance.df = pd.DataFrame(
            {
                "canteen_id": [1, 2],
                "year": [2023, 2023],
                "genere_par_cuisine_centrale": [False, True],
                "other_column": [10, 20],
            }
        )
        etl_instance.delete_duplicates_cc_csat()
        assert len(etl_instance.df) == 2


@pytest.mark.parametrize(
    "department, expected",
    [
        (974, "non renseigné"),  # Special case for department 974
        ("2A", "France métropolitaine"),  # Corsica department code
        ("2B", "France métropolitaine"),  # Corsica department code
        (75, "France métropolitaine"),  # Metropolitan France
        (976, "DROM (Mayotte)"),  # Mayotte
        (971, "DROM (hors Mayotte)"),  # Guadeloupe
        (972, "DROM (hors Mayotte)"),  # Martinique
        (978, "DROM (hors Mayotte)"),  # Saint-Martin
        ("nan", "non renseigné"),  # String "nan"
        (None, "non renseigné"),  # None value
        (pd.NA, "non renseigné"),  # Pandas NA
        (999, "non renseigné"),  # Invalid department
    ],
)
def test_get_objectif_zone_geo(department, expected):
    assert get_objectif_zone_geo(department) == expected
