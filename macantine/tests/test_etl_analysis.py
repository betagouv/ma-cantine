import json
from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from api.serializers import DiagnosticAnalysisSerializer
from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory, UserFactory
from data.models import Canteen, Diagnostic
from macantine.etl.analysis import (
    ETL_ANALYSIS_CANTEEN,
    ETL_ANALYSIS_TELEDECLARATIONS,
    aggregate_col,
)
from macantine.etl.utils import format_td_sector_column, get_objectif_zone_geo


class TestETLAnalysisCanteen(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sector = SectorFactory.create(id=1, name="Sector factory", category="Category factory")
        cls.canteen_1 = CanteenFactory(
            name="Cantine",
            siret="19382111300027",
            city_insee_code="38185",
            epci="200040715",
            epci_lib="Grenoble-Alpes-Métropole",
            department="38",
            department_lib="Isère",
            region="84",
            region_lib="Auvergne-Rhône-Alpes",
            sectors=[cls.sector],
            line_ministry=Canteen.Ministries.AGRICULTURE,
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        cls.canteen_2 = CanteenFactory(sectors=[cls.sector])

    def test_canteen_extract(self):
        etl = ETL_ANALYSIS_CANTEEN()
        etl.extract_dataset()
        self.assertEqual(len(etl.df.id.unique()), 2, "There should be two different canteens")
        self.assertEqual(etl.get_dataset().iloc[0]["id"], self.canteen_2.id, "Order by created date descending")

    def test_canteen_transform_dataset_match_schema(self):
        etl = ETL_ANALYSIS_CANTEEN()
        schema = json.load(open("data/schemas/export_analysis/schema_cantines.json"))
        schema_cols = [i["name"] for i in schema["fields"]]
        etl.extract_dataset()
        etl.transform_dataset()
        canteens = etl.df

        # Check the schema matching
        self.assertEqual(
            len(canteens.columns),
            len(schema_cols),
            "The columns should match have the same length as the number of elements in the schema.",
        )
        self.assertEqual(
            set(canteens.columns), set(schema_cols), "The columns names should match the schema field names."
        )

        # Check the generated columns
        canteen_1 = canteens[canteens.id == self.canteen_1.id].iloc[0]
        self.assertEqual(canteen_1["epci"], "200040715")
        self.assertEqual(canteen_1["epci_lib"], "Grenoble-Alpes-Métropole")
        self.assertEqual(canteen_1["departement"], "38")
        self.assertEqual(canteen_1["departement_lib"], "Isère")
        self.assertEqual(canteen_1["region"], "84")
        self.assertEqual(canteen_1["region_lib"], "Auvergne-Rhône-Alpes")
        self.assertEqual(canteen_1["secteur"], "Sector factory")
        self.assertEqual(canteen_1["ministere_tutelle"], "Agriculture, Alimentation et Forêts")
        self.assertEqual(canteen_1["type_gestion"], "Directe")
        self.assertEqual(canteen_1["type_production"], "Cantine qui produit les repas sur place")
        self.assertEqual(canteen_1["modele_economique"], "Public")
        self.assertEqual(canteen_1["spe"], "Oui")  # because line_ministry is set

        canteen_2 = canteens[canteens.id == self.canteen_2.id].iloc[0]
        self.assertEqual(canteen_2["ministere_tutelle"], None)
        self.assertEqual(canteen_2["type_gestion"], None)
        self.assertEqual(canteen_2["type_production"], None)
        self.assertEqual(canteen_2["modele_economique"], None)
        self.assertEqual(canteen_2["spe"], "Non")


class TestETLAnalysisTD(TestCase):
    def test_extraction_teledeclaration(self):
        applicant = UserFactory.create()
        canteen = CanteenFactory.create(siret="98648424243607")
        canteen_deleted = CanteenFactory.create(
            siret="12345678901234", deletion_date=timezone.make_aware(datetime.strptime("2023-03-31", "%Y-%m-%d"))
        )
        canteen_no_siret = CanteenFactory.create()

        with freeze_time("2023-03-30"):  # during the 2022 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2022, diagnostic_type=None, teledeclaration_id=1)
            diagnostic.teledeclare(applicant=applicant)
            diagnostic_canteen_deleted = DiagnosticFactory(
                canteen=canteen_deleted, year=2022, diagnostic_type=None, teledeclaration_id=2
            )
            diagnostic_canteen_deleted.teledeclare(applicant=applicant)
            diagnostic_canteen_no_siret = DiagnosticFactory(
                canteen=canteen_no_siret, year=2022, diagnostic_type=None, teledeclaration_id=3
            )
            diagnostic_canteen_no_siret.teledeclare(applicant=applicant)

        etl_stats = ETL_ANALYSIS_TELEDECLARATIONS()
        etl_stats.extract_dataset()

        self.assertEqual(etl_stats.len_dataset(), 1)

    def test_get_egalim_sans_bio(self):
        test_cases = [
            {
                "name": "1",
                "date_mocked": "2023-03-30",  # during the 2022 campai
                "year": 2022,
                "data": {
                    "value_total_ht": 100,
                    "value_bio_ht_agg": 0,
                    "value_externality_performance_ht_agg": 10,
                    "value_sustainable_ht_agg": 10,
                    "value_egalim_others_ht_agg": 10,
                },
                "expected_outcome": 30,
            },
            {
                "name": "2",
                "date_mocked": "2023-03-30",  # during the 2022 campai
                "year": 2022,
                "data": {
                    "value_total_ht": 100,
                    "value_bio_ht_agg": 0,
                    "value_externality_performance_ht_agg": 10,
                    "value_sustainable_ht_agg": 10,
                    "value_egalim_others_ht_agg": None,
                },
                "expected_outcome": 20,
            },
        ]

        for tc in test_cases:
            canteen = CanteenFactory()
            with freeze_time(tc["date_mocked"]):  # Faking time to mock creation_date
                diagnostic = DiagnosticFactory.create(
                    canteen=canteen,
                    year=tc["year"],
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                    value_total_ht=tc["data"]["value_total_ht"],
                    value_bio_ht=tc["data"]["value_bio_ht_agg"],
                    value_sustainable_ht=tc["data"]["value_sustainable_ht_agg"],
                    value_externality_performance_ht=tc["data"]["value_externality_performance_ht_agg"],
                    value_egalim_others_ht=tc["data"]["value_egalim_others_ht_agg"],
                )
                diagnostic.teledeclare(applicant=UserFactory.create())

                self.serializer_data = {
                    "value_total_ht": tc["data"]["value_total_ht"],
                    "value_bio_ht": tc["data"]["value_bio_ht_agg"],
                    "value_externality_performance_ht": tc["data"]["value_externality_performance_ht_agg"],
                    "value_sustainable_ht": tc["data"]["value_sustainable_ht_agg"],
                    "value_egalim_others_ht": tc["data"]["value_egalim_others_ht_agg"],
                }

                self.serializer = DiagnosticAnalysisSerializer(
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
                        "value_bio_ht": pd.NA,
                        "value_bio_boulange_ht": 5,
                        "value_bio_viande_ht": 5,
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
                        "value_bio_ht": 5,
                        "value_bio_boulange_ht": 5,
                        "value_bio_viande_ht": 5,
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
                        "value_bio_ht": pd.NA,
                        "value_bio_boulange_ht": 5,
                        "value_bio_viande_ht": 5,
                        "value_awesome_viande_ht": 5,
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
            self.assertEqual(td_aggregated.iloc[0][f"teledeclaration.value_{tc['categ']}_ht"], tc["expected_outcome"])

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
        test_cases = [
            {
                "name": "Valid cout denrees",
                "date_mocked": "2023-03-30",  # during the 2022 campai
                "year": 2022,
                "data": {
                    "value_total_ht": 1,
                    "yearly_meal_count": 1,
                },
                "expected_outcome": 1,
            },
            {
                "name": "Invalid cout denrees",
                "date_mocked": "2023-03-30",  # during the 2022 campai
                "year": 2022,
                "data": {
                    "value_total_ht": 1,
                    "yearly_meal_count": 0,
                },
                "expected_outcome": -1,
            },
        ]

        for tc in test_cases:
            with freeze_time(tc["date_mocked"]):  # Faking time to mock creation_date
                canteen = CanteenFactory(yearly_meal_count=tc["data"]["yearly_meal_count"])
                diagnostic = DiagnosticFactory.create(
                    canteen=canteen, year=tc["year"], value_total_ht=tc["data"]["value_total_ht"]
                )
                diagnostic.teledeclare(applicant=UserFactory.create())

                self.serializer_data = {
                    "yearly_meal_count": tc["data"]["yearly_meal_count"],
                    "value_total_ht": tc["data"]["value_total_ht"],
                }

                self.serializer = DiagnosticAnalysisSerializer(
                    instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
                )
                data = self.serializer.data

                self.assertEqual(data["cout_denrees"], tc["expected_outcome"])

    def test_geo_columns(self):
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_with_geo_data = CanteenFactory.create(
                department="38",
                department_lib="Isère",
                region="84",
                region_lib="Auvergne-Rhône-Alpes",
                epci="200040715",
                epci_lib="Grenoble-Alpes-Métropole",
            )
            diagnostic = DiagnosticFactory.create(canteen=canteen_with_geo_data, year=2022)
            diagnostic.teledeclare(applicant=UserFactory.create())

        self.serializer = DiagnosticAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
        )
        data = self.serializer.data

        self.assertEqual(data["departement"], "38")
        self.assertEqual(data["lib_departement"], "Isère")
        self.assertEqual(data["region"], "84")
        self.assertEqual(data["lib_region"], "Auvergne-Rhône-Alpes")

        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_half_geo_data = CanteenFactory.create(
                department="38",
                department_lib=None,
                region="84",
                region_lib=None,
                epci="200040715",
                epci_lib=None,
            )
            diagnostic_half_geo = DiagnosticFactory.create(canteen=canteen_half_geo_data, year=2022)
            diagnostic_half_geo.teledeclare(applicant=UserFactory.create())

        self.serializer_half_geo = DiagnosticAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic_half_geo.id)
        )
        data = self.serializer_half_geo.data

        self.assertEqual(data["departement"], "38")
        self.assertEqual(data["lib_departement"], "Isère")  # filled with the serializer
        self.assertEqual(data["region"], "84")
        self.assertEqual(data["lib_region"], "Auvergne-Rhône-Alpes")  # filled with the serializer

        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_without_geo_data = CanteenFactory.create(
                department=None,
                department_lib=None,
                region=None,
                region_lib=None,
                epci=None,
                epci_lib=None,
            )
            diagnostic_without_geo = DiagnosticFactory.create(canteen=canteen_without_geo_data, year=2022)
            diagnostic_without_geo.teledeclare(applicant=UserFactory.create())

        self.serializer_without_geo = DiagnosticAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic_without_geo.id)
        )
        data_no_geo = self.serializer_without_geo.data

        self.assertEqual(data_no_geo["departement"], None)
        self.assertEqual(data_no_geo["lib_departement"], None)
        self.assertEqual(data_no_geo["region"], None)
        self.assertEqual(data_no_geo["lib_region"], None)

    def test_line_ministry_and_spe(self):
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_with_line_ministry = CanteenFactory.create(line_ministry=Canteen.Ministries.AGRICULTURE)
            diagnostic = DiagnosticFactory.create(canteen=canteen_with_line_ministry, year=2022)
            diagnostic.teledeclare(applicant=UserFactory.create())

        self.serializer = DiagnosticAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic.id)
        )
        data = self.serializer.data

        self.assertEqual(data["line_ministry"], Canteen.Ministries.AGRICULTURE)
        self.assertEqual(data["spe"], "Oui")

        with freeze_time("2023-03-30"):  # during the 2022 campaign
            canteen_without_line_ministry = CanteenFactory.create(line_ministry=None)
            diagnostic_without_line_ministry = DiagnosticFactory.create(
                canteen=canteen_without_line_ministry, year=2022
            )
            diagnostic_without_line_ministry.teledeclare(applicant=UserFactory.create())

        self.serializer_without_line_ministry = DiagnosticAnalysisSerializer(
            instance=Diagnostic.objects.with_meal_price().get(id=diagnostic_without_line_ministry.id)
        )
        data_without_line_ministry = self.serializer_without_line_ministry.data

        self.assertEqual(data_without_line_ministry["line_ministry"], None)
        self.assertEqual(data_without_line_ministry["spe"], "Non")

    def test_flatten_td(self):
        data = {
            "id": {2: 1, 3: 2, 4: 3},
            "year": {2: 2024, 3: 2024, 4: 2024},
            "canteen_id": {2: 1, 3: 2, 4: 3},
            "name": {2: "Cantine A", 3: "Cantine B", 4: "Cantine C"},
            "siret": {2: "siretA", 3: "siretB", 4: "siretC"},
            "daily_meal_count": {2: 38.0, 3: None, 4: None},
            "yearly_meal_count": {2: 10, 3: 100, 4: 300},
            "production_type": {2: "site", 3: "central", 4: "central_serving"},
            "cuisine_centrale": {2: "B) non", 3: "A) oui", 4: "A) oui"},
            "central_producer_siret": {2: None, 3: None, 4: None},
            "diagnostic_type": {2: None, 3: None, 4: None},
            "satellite_canteens_count": {2: None, 3: 206.0, 4: 2},
            "value_total_ht": {2: 100, 3: 1000, 4: 1500},
            "value_bio_ht": {2: None, 3: 100, 4: 0},
            "tmp_satellites": {
                2: None,
                3: [
                    {
                        "id": 20,
                        "name": "SAT 1",
                        "siret": "21930055500196",
                        "yearly_meal_count": 60,
                        "sectors": [{"Secteur A"}, {"Secteur B"}],
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
            },
        }

        etl = ETL_ANALYSIS_TELEDECLARATIONS()
        etl.df = pd.DataFrame.from_dict(data)
        etl.flatten_central_kitchen_td()
        self.assertEqual(len(etl.df[etl.df.canteen_id == 2]), 0)  # Central kitchen filtered out
        self.assertEqual(len(etl.df[etl.df.canteen_id == 20]), 1)  # Satellite created
        self.assertEqual(etl.df[etl.df.canteen_id == 20].iloc[0].value_total_ht, 500)  # Appro value split
        self.assertEqual(etl.df[etl.df.canteen_id == 20].iloc[0].secteur, "Secteurs multiples")  # Appro value split
        self.assertEqual(len(etl.df[etl.df.canteen_id == 3]), 1)  # Central kitchen filtered out
        self.assertEqual(etl.df[etl.df.canteen_id == 3].iloc[0].value_total_ht, 500)  # Appro value split
        self.assertEqual(etl.df[etl.df.canteen_id == 30].iloc[0].value_total_ht, 500)  # Appro value split
        self.assertEqual(etl.df[etl.df.canteen_id == 31].iloc[0].yearly_meal_count, 300 / 3)
        self.assertTrue(np.isnan(etl.df[etl.df.canteen_id == 1].iloc[0].value_bio_ht))  # Nulls are processed as nulls
        self.assertEqual(
            etl.df[etl.df.canteen_id == 3].iloc[0].value_bio_ht, 0
        )  # Zeros are processed as zeros and not nulls

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
