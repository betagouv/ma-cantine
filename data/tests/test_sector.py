from django.test import TestCase

from data.models.sector import (
    Sector,
    SectorCategory,
    get_sector_category_from_sector,
    is_sector_with_line_ministry,
    get_sector_lib_list_from_sector_list,
    get_category_lib_list_from_sector_list,
)


class SectorTextChoicesTest(TestCase):
    def test_get_sector_label_list_from_sector_list(self):
        for TUPLE in [
            (None, []),
            ([], []),
            (["Inconnu"], []),
            ([Sector.SANTE_HOPITAL], ["Hôpitaux"]),
            ([Sector.SANTE_HOPITAL, Sector.SOCIAL_CRECHE], ["Hôpitaux", "Crèche"]),
        ]:
            with self.subTest(TUPLE=TUPLE):
                self.assertEqual(get_sector_lib_list_from_sector_list(TUPLE[0]), TUPLE[1])

    def test_get_sector_category_from_sector(self):
        for TUPLE in [
            (None, SectorCategory.AUTRES),
            ("", SectorCategory.AUTRES),
            ("Inconnu", SectorCategory.AUTRES),
            (Sector.ADMINISTRATION_PRISON, SectorCategory.ADMINISTRATION),
            (Sector.ENTERPRISE_ENTREPRISE, SectorCategory.ENTERPRISE),
            (Sector.EDUCATION_PRIMAIRE, SectorCategory.EDUCATION),
            (Sector.SANTE_HOPITAL, SectorCategory.HEALTH),
            (Sector.SOCIAL_CRECHE, SectorCategory.SOCIAL),
            (Sector.LOISIR_CENTRE_VACANCES, SectorCategory.LEISURE),
            (Sector.AUTRES_AUTRE, SectorCategory.AUTRES),
        ]:
            with self.subTest(TUPLE=TUPLE):
                self.assertEqual(get_sector_category_from_sector(TUPLE[0]), TUPLE[1])

    def test_get_category_lib_list_from_sector_list(self):
        for TUPLE in [
            (None, []),
            ([], []),
            (["Inconnu"], ["Autres"]),
            ([Sector.SANTE_HOPITAL], ["Santé"]),
            ([Sector.SANTE_HOPITAL, Sector.SANTE_AUTRE], ["Santé"]),
            ([Sector.SANTE_HOPITAL, Sector.SOCIAL_CRECHE], ["Santé", "Social / Médico-social"]),
        ]:
            with self.subTest(TUPLE=TUPLE):
                self.assertEqual(get_category_lib_list_from_sector_list(TUPLE[0]), TUPLE[1])

    def test_is_sector_with_line_ministry(self):
        self.assertTrue(is_sector_with_line_ministry(Sector.ADMINISTRATION_PRISON))
        self.assertTrue(is_sector_with_line_ministry(Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE))
        self.assertFalse(is_sector_with_line_ministry(Sector.EDUCATION_PRIMAIRE))
        self.assertFalse(is_sector_with_line_ministry(Sector.SANTE_HOPITAL))
