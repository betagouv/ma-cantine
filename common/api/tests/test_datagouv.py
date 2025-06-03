import json
import unittest

import requests_mock

from common.api.datagouv import (
    DATAGOUV_API_URL,
    PAT_DATAGOUV_DATASET_ID,
    PAT_DATAGOUV_RESOURCE_ID,
    map_pat_list_to_communes_insee_code,
)


@requests_mock.Mocker()
class TestDataGouvAPI(unittest.TestCase):
    def test_map_pat_list_to_communes_insee_code(self, mock):
        mock.get(
            f"{DATAGOUV_API_URL}/datasets/{PAT_DATAGOUV_DATASET_ID}/resources/{PAT_DATAGOUV_RESOURCE_ID}",
            text=json.dumps(
                {
                    "id": "96606cae-0b3b-4910-9d8b-65e3dd7f1bda",
                    "title": "pats-20250224-win1252.csv",
                    "url": "https://static.data.gouv.fr/resources/pat-projets-alimentaires-territoriaux-description/20250224-103639/pats-20250224-win1252.csv",
                }
            ),
        )
        pat_csv_text = (
            "id;lien_vers_la_fiche_pat;nom_administratif;nom_usuel;regions;departement;epci;communes_code_insee\n"
        )
        pat_csv_text += '891;https://france-pat.fr/pat/redon-agglomeration/;"Programme Agricole et Alimentaire de Territoire de REDON Agglomération";;"Pays de la Loire, Bretagne";"Ille-et-Vilaine, Loire-Atlantique, Morbihan";;35145,56232,44185,56011,56216,56250,44067,35045,35268,35285,35064,35151,35219,56221,35236,56154,56239,35013,35237,56001,56223,44123,35328,44057,44092,56194,35294,44044,44128,56060,44007\n'
        pat_csv_text += '1263;https://france-pat.fr/pat/pat-du-bassin-de-bourg-en-bresse/;"PAT du Bassin de Bourg-en-Bresse";"PAT Grand Bourg Agglomération : Relocaliser la valeur ajoutée sur le territoire";Auvergne-Rhône-Alpes;Ain;;01230,01212,01364,01367,01163,01029,01147,01296,01108,01232,01124,01128,01388,01380,01433,01196,01040,01406,01127,01321,01391,01445,01236,01432,01229,01266,01309,01038,01387,01346,01024,01375,01140,01115,01301,01125,01408,01177,01195,01259,01429,01065,01344,01264,01385,01150,01053,01447,01072,01317,01369,01184,01254,01245,01336,01289,01405,01069,01422,01211,01197,01374,01425,01106,01151,01145,01451,01241,01350,01139,01437,01130,01095,01426\n'
        mock.get(
            "https://static.data.gouv.fr/resources/pat-projets-alimentaires-territoriaux-description/20250224-103639/pats-20250224-win1252.csv",
            text=pat_csv_text,
        )

        pat_list_to_communes_insee_code = map_pat_list_to_communes_insee_code()
        self.assertEqual(len(pat_list_to_communes_insee_code), 105)
        self.assertIn("35145", pat_list_to_communes_insee_code)
        self.assertEqual(pat_list_to_communes_insee_code["35145"][0]["pat"], "891")
        self.assertEqual(
            pat_list_to_communes_insee_code["35145"][0]["pat_lib"],
            "Programme Agricole et Alimentaire de Territoire de REDON Agglomération",
        )
