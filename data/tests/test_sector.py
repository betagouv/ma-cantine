from django.test import TestCase

from data.models.sector import (
    Sector,
    SectorCategory,
    get_sector_category_from_sector,
    is_sector_with_line_ministry,
    get_sector_label_list_from_sector_list,
)


class SectorTextChoicesTest(TestCase):
    def test_get_sector_label_list_from_sector_list(self):
        self.assertEqual(get_sector_label_list_from_sector_list(None), [])
        self.assertEqual(get_sector_label_list_from_sector_list([]), [])
        self.assertEqual(get_sector_label_list_from_sector_list([Sector.SANTE_HOPITAL]), ["Hôpitaux"])
        self.assertEqual(
            get_sector_label_list_from_sector_list([Sector.SANTE_HOPITAL, Sector.SOCIAL_CRECHE]),
            ["Hôpitaux", "Crèche"],
        )
        self.assertEqual(get_sector_label_list_from_sector_list(["Inconnu"]), [])

    def test_get_sector_category_from_sector(self):
        self.assertEqual(get_sector_category_from_sector(None), SectorCategory.AUTRES)
        self.assertEqual(
            get_sector_category_from_sector(Sector.ADMINISTRATION_PRISON),
            SectorCategory.ADMINISTRATION,
        )
        self.assertEqual(
            get_sector_category_from_sector(Sector.ENTERPRISE_ENTREPRISE),
            SectorCategory.ENTERPRISE,
        )
        self.assertEqual(
            get_sector_category_from_sector(Sector.EDUCATION_PRIMAIRE),
            SectorCategory.EDUCATION,
        )
        self.assertEqual(
            get_sector_category_from_sector(Sector.SANTE_HOPITAL),
            SectorCategory.HEALTH,
        )
        self.assertEqual(
            get_sector_category_from_sector(Sector.SOCIAL_CRECHE),
            SectorCategory.SOCIAL,
        )
        self.assertEqual(
            get_sector_category_from_sector(Sector.LOISIR_CENTRE_VACANCES),
            SectorCategory.LEISURE,
        )
        self.assertEqual(
            get_sector_category_from_sector(Sector.AUTRES_AUTRE),
            SectorCategory.AUTRES,
        )

    def test_is_sector_with_line_ministry(self):
        self.assertTrue(is_sector_with_line_ministry(Sector.ADMINISTRATION_PRISON))
        self.assertTrue(is_sector_with_line_ministry(Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE))
        self.assertFalse(is_sector_with_line_ministry(Sector.EDUCATION_PRIMAIRE))
        self.assertFalse(is_sector_with_line_ministry(Sector.SANTE_HOPITAL))
