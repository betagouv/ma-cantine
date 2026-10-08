from django.test import TestCase

from data.models.geo import Region
from data.models.diagnostic_teledeclaration_egalim_objectives import (
    EGALIM_OBJECTIVES,
    get_egalim_group,
    get_egalim_objectives,
    has_egalim_objectives,
    objectifs_egalim_atteints,
)


class EgalimObjectivesTest(TestCase):
    def test_get_egalim_objectives(self):
        self.assertEqual(get_egalim_objectives(2025, "APPRO"), EGALIM_OBJECTIVES[2025]["APPRO"])
        self.assertEqual(get_egalim_objectives("2025", "APPRO"), EGALIM_OBJECTIVES[2025]["APPRO"])
        # years outside of EGALIM_OBJECTIVES: fallback to the first or last defined year
        self.assertEqual(get_egalim_objectives(2019, "APPRO"), EGALIM_OBJECTIVES[2021]["APPRO"])
        self.assertEqual(get_egalim_objectives(2100, "APPRO"), EGALIM_OBJECTIVES[max(EGALIM_OBJECTIVES)]["APPRO"])
        # unknown label
        with self.assertRaises(ValueError):
            get_egalim_objectives(2025, "UNKNOWN")

    def test_has_egalim_objectives(self):
        self.assertTrue(has_egalim_objectives(2025, "APPRO"))
        self.assertFalse(has_egalim_objectives(2025, "APPRO_VIANDES_PRODUITS_DE_LA_MER"))
        self.assertTrue(has_egalim_objectives(2026, "APPRO_VIANDES_PRODUITS_DE_LA_MER"))
        self.assertTrue(has_egalim_objectives(2100, "APPRO_VIANDES_PRODUITS_DE_LA_MER"))  # fallback to last year
        self.assertFalse(has_egalim_objectives(2026, "UNKNOWN"))

    def test_get_egalim_group(self):
        self.assertEqual(get_egalim_group([Region.bretagne]), "hexagone")
        self.assertEqual(get_egalim_group([Region.guadeloupe]), "groupe_1")
        self.assertEqual(get_egalim_group([Region.mayotte]), "groupe_2")
        self.assertEqual(get_egalim_group([Region.saint_pierre_et_miquelon]), "groupe_3")
        self.assertEqual(get_egalim_group([Region.bretagne, Region.guadeloupe]), "hexagone")
        self.assertEqual(get_egalim_group([Region.guadeloupe, Region.bretagne]), "hexagone")
        self.assertEqual(get_egalim_group([Region.guadeloupe, Region.martinique]), "groupe_1")
        self.assertEqual(get_egalim_group([Region.guadeloupe, Region.mayotte]), "groupe_1")
        self.assertEqual(get_egalim_group([]), "hexagone")
        self.assertEqual(get_egalim_group(None), "hexagone")

    def test_objectifs_egalim_atteints(self):
        # hexagone
        for pourcentage_bio, pourcentage_egalim, canteen_region, resultat in [
            # hexagone (ou sans région)
            (20, 50, None, True),
            (20, 50, Region.bretagne, True),
            (19, 50, Region.bretagne, False),
            (20, 49, Region.bretagne, False),
            # groupe 1
            (5, 20, Region.guadeloupe, True),
            (4, 20, Region.guadeloupe, False),
            (5, 19, Region.guadeloupe, False),
            # groupe 2
            (2, 5, Region.mayotte, True),
            (1, 5, Region.mayotte, False),
            (2, 4, Region.mayotte, False),
            # groupe 3
            (10, 30, Region.saint_pierre_et_miquelon, True),
            (9, 30, Region.saint_pierre_et_miquelon, False),
            (10, 29, Region.saint_pierre_et_miquelon, False),
            # missing percentage (e.g. no valeur_totale)
            (None, 50, Region.bretagne, None),
            (20, None, Region.bretagne, None),
            (None, None, Region.bretagne, None),
        ]:
            with self.subTest(pourcentage_bio=pourcentage_bio, pourcentage_egalim=pourcentage_egalim):
                self.assertEqual(
                    objectifs_egalim_atteints(2025, canteen_region, pourcentage_bio, pourcentage_egalim),
                    resultat,
                )

    def test_objectifs_egalim_atteints_2026(self):
        # since 2026: viandes_volailles & produits_de_la_mer objectives (60%, all regions)
        for (
            pourcentage_bio,
            pourcentage_egalim,
            canteen_region,
            pourcentage_viandes_volailles_egalim,
            pourcentage_produits_de_la_mer_egalim,
            resultat,
        ) in [
            # all objectives reached
            (20, 50, Region.bretagne, 60, 60, True),
            (5, 20, Region.guadeloupe, 60, 60, True),
            # viandes_volailles or produits_de_la_mer objective not reached
            (20, 50, Region.bretagne, 59, 60, False),
            (20, 50, Region.bretagne, 60, 59, False),
            (5, 20, Region.guadeloupe, 59, 60, False),
            # bio or egalim objective not reached
            (19, 50, Region.bretagne, 60, 60, False),
            (20, 49, Region.bretagne, 60, 60, False),
            # viandes_volailles or produits_de_la_mer unknown
            (20, 50, Region.bretagne, None, 60, None),
            (20, 50, Region.bretagne, 60, None, None),
            (20, 50, Region.bretagne, None, None, None),
            # ... but another objective is not reached
            (19, 50, Region.bretagne, None, 60, False),
            (20, 50, Region.bretagne, None, 59, False),
        ]:
            with self.subTest(
                pourcentage_bio=pourcentage_bio,
                pourcentage_egalim=pourcentage_egalim,
                canteen_region=canteen_region,
                pourcentage_viandes_volailles_egalim=pourcentage_viandes_volailles_egalim,
                pourcentage_produits_de_la_mer_egalim=pourcentage_produits_de_la_mer_egalim,
            ):
                self.assertEqual(
                    objectifs_egalim_atteints(
                        2026,
                        canteen_region,
                        pourcentage_bio,
                        pourcentage_egalim,
                        pourcentage_viandes_volailles_egalim=pourcentage_viandes_volailles_egalim,
                        pourcentage_produits_de_la_mer_egalim=pourcentage_produits_de_la_mer_egalim,
                    ),
                    resultat,
                )
        # before 2026: viandes_volailles & produits_de_la_mer are ignored
        self.assertTrue(objectifs_egalim_atteints(2025, Region.bretagne, 20, 50, 0, None))
