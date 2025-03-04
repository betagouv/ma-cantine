from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.utils import override_settings
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen


class TestCanteenModel(TestCase):
    def test_create_canteen(self):
        # siret: normalize on save
        canteen = CanteenFactory.create(siret="756 656 218 99905")
        self.assertEqual(canteen.siret, "75665621899905")  # normalized
        # region: get from department on save
        canteen = CanteenFactory.create(department="38", region=None)
        self.assertEqual(canteen.region, "84")  # Auvergne-Rhône-Alpes

    def test_create_canteen_siret_validation(self):
        # siret: cannot be empty
        for siret in ["", None]:
            self.assertRaises(ValidationError, CanteenFactory, siret=siret)

    @freeze_time("2024-01-20")
    def test_appro_and_service_diagnostics_in_past_ordered_year_desc(self):
        canteen = CanteenFactory.create()
        DiagnosticFactory(canteen=canteen, year=2024)
        DiagnosticFactory(canteen=canteen, year=2022)
        DiagnosticFactory(canteen=canteen, year=2023)
        canteen.refresh_from_db()

        self.assertEqual(canteen.appro_diagnostics.count(), 2)
        self.assertEqual(canteen.appro_diagnostics.first().year, 2023)
        self.assertEqual(canteen.service_diagnostics.count(), 2)
        self.assertEqual(canteen.service_diagnostics.first().year, 2023)
        self.assertEqual(canteen.latest_published_year, 2023)

    def test_soft_delete_canteen(self):
        """
        The delete method should "soft delete" a canteen and have it hidden by default
        from querysets, unless specifically asked for
        """
        canteen = CanteenFactory.create()
        canteen.delete()
        qs = Canteen.objects.all()
        self.assertEqual(qs.count(), 0, "Soft deleted canteen is not visible in default queryset")
        qs = Canteen.all_objects.all()
        self.assertEqual(qs.count(), 1, "Soft deleted canteens can be accessed in custom queryset")


class TestCanteenQueryset(TestCase):
    @classmethod
    def setUpTestData(cls):
        CanteenFactory(line_ministry=None, publication_status=Canteen.PublicationStatus.PUBLISHED)
        cls.canteen_published_armee = CanteenFactory(
            line_ministry=Canteen.Ministries.ARMEE, publication_status=Canteen.PublicationStatus.PUBLISHED
        )
        cls.canteen_draft = CanteenFactory(line_ministry=None, publication_status=Canteen.PublicationStatus.DRAFT)

    @override_settings(PUBLISH_BY_DEFAULT=False)
    def test_publicly_visible(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_visible()
        self.assertEqual(qs.count(), 2)
        self.assertTrue(self.canteen_draft not in qs)

    @override_settings(PUBLISH_BY_DEFAULT=False)
    def test_publicly_hidden(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_hidden()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.canteen_draft)

    @override_settings(PUBLISH_BY_DEFAULT=True)
    def test_publicly_visible_publish_by_default(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_visible()
        self.assertEqual(qs.count(), 2)
        self.assertTrue(self.canteen_published_armee not in qs)

    @override_settings(PUBLISH_BY_DEFAULT=True)
    def test_publicly_hidden_publish_by_default(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_hidden()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.canteen_published_armee)
