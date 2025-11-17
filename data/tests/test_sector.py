from django.test import TestCase

from data.models.sector import Sector, SectorCategory, get_sector_category_from_sector


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
            get_sector_category_from_sector(Sector.HEALTH_HOPITAL),
        )
        self.assertEqual(
            SectorCategory.SOCIAL,
            get_sector_category_from_sector(Sector.SOCIAL_CRECHE),
        )
        self.assertEqual(
            SectorCategory.LEISURE,
            get_sector_category_from_sector(Sector.LEISURE_CENTRE_VACANCE),
        )
        self.assertEqual(
            SectorCategory.AUTRES,
            get_sector_category_from_sector(Sector.AUTRES_AUTRE),
        )
