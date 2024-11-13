import json

import pandas as pd
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory, UserFactory
from data.models import Teledeclaration
from macantine.etl.analysis import (
    ETL_ANALYSIS_CANTEEN,
    ETL_ANALYSIS_TD,
    aggregate_col,
    get_egalim_hors_bio,
)
from macantine.etl.utils import format_td_sector_column


class TestETLAnalysisCanteen(TestCase):

    def test_transformed_dataset_match_schema(self):
        etl = ETL_ANALYSIS_CANTEEN()
        SectorFactory.create(id=1, name="Sector factory", category="Category factory")

        schema = json.load(open("data/schemas/schema_analysis_cantines.json"))
        schema_cols = [i["name"] for i in schema["fields"]]
        canteen_1 = CanteenFactory(
            name="Cantine", siret="11007001800012", city_insee_code="29021", department="29", region="53", sectors=[1]
        )
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
        first_canteen = canteens[canteens.id == canteen_1.id].iloc[0]
        self.assertEqual(first_canteen["departement_lib"], "Finistère")
        self.assertEqual(first_canteen["region_lib"], "Bretagne")
        self.assertEqual(first_canteen["secteur"], "Sector factory")
        self.assertEqual(first_canteen["spe"], False)


class TestETLAnalysisTD(TestCase):

    def test_extraction_teledeclaration(self):
        """
        Only teledeclarations that occurred during teledeclaration campaigns should be extracted
        """
        canteen = CanteenFactory.create(siret="98648424243607")
        applicant = UserFactory.create()
        with freeze_time("1991-01-14"):  # Faking time to mock creation_date
            diagnostic_1990 = DiagnosticFactory.create(canteen=canteen, year=1990, diagnostic_type=None)
            _ = Teledeclaration.create_from_diagnostic(diagnostic_1990, applicant)

        with freeze_time("2023-05-14"):  # Faking time to mock creation_date
            diagnostic_2022 = DiagnosticFactory.create(canteen=canteen, year=2022, diagnostic_type=None)
            td_2022 = Teledeclaration.create_from_diagnostic(diagnostic_2022, applicant)

        with freeze_time("2024-02-14"):  # Faking time to mock creation_date
            diagnostic_2023 = DiagnosticFactory.create(canteen=canteen, year=2023, diagnostic_type=None)
            td_2023 = Teledeclaration.create_from_diagnostic(diagnostic_2023, applicant)

        # This TD should not be extracted as its canteen has been deleted during the campaign
        with freeze_time("2024-02-14"):  # Faking time to mock creation_date
            canteen_deleted_during_campaign = CanteenFactory.create(siret="28838740672960")
            diagnostic_out_of_range = DiagnosticFactory.create(
                canteen=canteen_deleted_during_campaign, year=2023, diagnostic_type=None
            )
            Teledeclaration.create_from_diagnostic(diagnostic_out_of_range, applicant)
            canteen_deleted_during_campaign.delete()

        etl_stats = ETL_ANALYSIS_TD()

        etl_stats.extract_dataset()
        self.assertEqual(
            len(etl_stats.df),
            2,
            "There should be two teledeclaration. None for 1990 (no campaign). One for 2022 and one for 2023",
        )
        self.assertEqual(etl_stats.df[etl_stats.df.id == td_2022.id].year.iloc[0], 2022)
        self.assertEqual(etl_stats.df[etl_stats.df.id == td_2023.id].year.iloc[0], 2023)

    def test_get_egalim_hors_bio(self):
        data = {
            "0": {
                "canteen_id": 1,
                "teledeclaration.value_externality_performance_ht": 10,
                "teledeclaration.value_sustainable_ht": 10,
                "teledeclaration.value_egalim_others_ht": 10,
            },
            "1": {
                "canteen_id": 1,
                "teledeclaration.value_externality_performance_ht": 10,
                "teledeclaration.value_sustainable_ht": 10,
            },
        }
        df = pd.DataFrame.from_dict(data, orient="index")
        df["value_somme_egalim_hors_bio_ht"] = df.apply(get_egalim_hors_bio, axis=1)
        self.assertEqual(df.iloc[0]["value_somme_egalim_hors_bio_ht"], 30)
        self.assertEqual(df.iloc[1]["value_somme_egalim_hors_bio_ht"], 20)

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
