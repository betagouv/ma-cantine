from django.test import TestCase

from data.models.canteen_petite_structure import get_petite_structure_daily_meal_count_threshold
from data.models.sector import Sector


class CanteenPetiteStructureTest(TestCase):
    def test_get_petite_structure_daily_meal_count_threshold(self):
        for TUPLE in [
            (None, None),
            ([], None),
            ([Sector.EDUCATION_PRIMAIRE], 30),
            ([Sector.EDUCATION_ENSEIGNEMENT_AGRICOLE], 30),
            ([Sector.SOCIAL_CRECHE], 30),
            ([Sector.SANTE_HOPITAL], 70),
            ([Sector.SOCIAL_EHPAD], 70),
            ([Sector.LOISIR_CENTRE_VACANCES], 70),
            ([Sector.EDUCATION_SECONDAIRE_COLLEGE], None),  # not eligible
            ([Sector.ADMINISTRATION_PRISON], None),  # not eligible
            ([Sector.SANTE_HOPITAL, Sector.SOCIAL_EHPAD], None),  # several sectors (even if eligible)
            ([Sector.EDUCATION_PRIMAIRE, Sector.EDUCATION_SECONDAIRE_COLLEGE], None),  # several sectors
        ]:
            with self.subTest(sector_list=TUPLE[0]):
                self.assertEqual(get_petite_structure_daily_meal_count_threshold(TUPLE[0]), TUPLE[1])
