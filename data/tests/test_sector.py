from django.test import TestCase

from data.models.sector import Sector, SectorCategory, get_sector_category_from_sector, is_sector_with_line_ministry


class SectorTextChoicesTest(TestCase):
    def test_get_sector_category_from_sector(self):
        self.assertEqual(
            SectorCategory.ADMINISTRATION,
            get_sector_category_from_sector(Sector.ADMINISTRATION_PRISON),
        )
        self.assertEqual(
            SectorCategory.ENTERPRISE,
            get_sector_category_from_sector(Sector.ENTERPRISE_ENTREPRISE),
        )
        self.assertEqual(
            SectorCategory.EDUCATION,
            get_sector_category_from_sector(Sector.EDUCATION_PRIMAIRE),
        )
        self.assertEqual(
            SectorCategory.HEALTH,
            get_sector_category_from_sector(Sector.SANTE_HOPITAL),
        )
        self.assertEqual(
            SectorCategory.SOCIAL,
            get_sector_category_from_sector(Sector.SOCIAL_CRECHE),
        )
        self.assertEqual(
            SectorCategory.LEISURE,
            get_sector_category_from_sector(Sector.LOISIR_CENTRE_VACANCES),
        )
        self.assertEqual(
            SectorCategory.AUTRES,
            get_sector_category_from_sector(Sector.AUTRES_AUTRE),
        )

    def test_is_sector_with_line_ministry(self):
        self.assertTrue(is_sector_with_line_ministry(Sector.ADMINISTRATION_PRISON))
        self.assertTrue(is_sector_with_line_ministry(Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE))
        self.assertFalse(is_sector_with_line_ministry(Sector.EDUCATION_PRIMAIRE))
        self.assertFalse(is_sector_with_line_ministry(Sector.SANTE_HOPITAL))
