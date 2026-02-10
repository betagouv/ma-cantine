from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from data.factories import CanteenFactory, UserFactory, DiagnosticFactory
from data.models import Canteen, User
from macantine import tasks


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_with_canteens = UserFactory()
        cls.user_without_canteens = UserFactory()

        cls.canteen_empty = CanteenFactory(managers=[cls.user_with_canteens])
        cls.canteen_empty.management_type = None
        cls.canteen_empty.production_type = None
        cls.canteen_empty.economic_model = None
        cls.canteen_empty.save(skip_validations=True)
        cls.canteen_groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=None,
            managers=[cls.user_with_canteens],
        )
        cls.canteen_centrale = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[cls.user_with_canteens],
        )
        cls.canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[cls.user_with_canteens],
        )
        cls.canteen_site_armee = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[cls.user_with_canteens],
        )
        cls.canteen_site_concedee = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.CONCEDED,
            economic_model=Canteen.EconomicModel.PRIVATE,
            managers=[cls.user_with_canteens],
        )

        cls.canteen_centrale_diagnostic_teledeclared = DiagnosticFactory(year=2025, canteen=cls.canteen_centrale)
        cls.canteen_site_armee_diagnostic = DiagnosticFactory(year=2025, canteen=cls.canteen_site_armee)

        with freeze_time("2026-01-30"):  # during the 2025 campaign
            cls.canteen_centrale_diagnostic_teledeclared.teledeclare(applicant=cls.user_with_canteens)

        tasks.canteen_fill_declaration_donnees_year_field()

    def test_queryset_brevo_to_create(self):
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.brevo_to_create().count(), 2)

    def test_queryset_brevo_to_update(self):
        # No users have brevo_last_update_date set yet
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.brevo_to_update().count(), 0)

        # Set brevo_last_update_date for the first user
        now = timezone.now()
        User.objects.filter(id=self.user_with_canteens.id).update(brevo_last_update_date=now)
        self.assertEqual(User.objects.brevo_to_update().count(), 0)

        # Set brevo_last_update_date for the other user to 2 days ago
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        User.objects.filter(id=self.user_without_canteens.id).update(brevo_last_update_date=two_days_ago)
        self.assertEqual(User.objects.brevo_to_update().count(), 1)

        # delete the other user from brevo
        User.objects.filter(id=self.user_without_canteens.id).update(brevo_is_deleted=True)
        self.assertEqual(User.objects.brevo_to_update().count(), 0)

    def test_queryset_with_canteen_stats(self):
        user_qs = User.objects.with_canteen_stats()

        user_with_canteens = user_qs.get(id=self.user_with_canteens.id)
        user_without_canteens = user_qs.get(id=self.user_without_canteens.id)

        self.assertEqual(user_with_canteens.nb_cantines, 6)
        self.assertEqual(user_with_canteens.nb_cantines_groupe, 1 + 1)
        self.assertEqual(user_with_canteens.nb_cantines_site, 2)
        self.assertEqual(user_with_canteens.nb_cantines_satellite, 1)
        self.assertEqual(user_with_canteens.nb_cantines_gestion_concedee, 1)

        self.assertEqual(user_without_canteens.nb_cantines, 0)
        self.assertEqual(user_without_canteens.nb_cantines_groupe, 0)
        self.assertEqual(user_without_canteens.nb_cantines_site, 0)
        self.assertEqual(user_without_canteens.nb_cantines_satellite, 0)
        self.assertEqual(user_without_canteens.nb_cantines_gestion_concedee, 0)

    def test_queryset_with_canteen_diagnostic_stats(self):
        user_qs = User.objects.with_canteen_diagnostic_stats()

        user_with_canteens = user_qs.get(id=self.user_with_canteens.id)
        user_without_canteens = user_qs.get(id=self.user_without_canteens.id)

        self.assertEqual(user_with_canteens.nb_cantines_bilan_2025, 2)
        self.assertEqual(user_with_canteens.nb_cantines_bilan_todo_2025, 4)  # nb_cantines - nb_bilans_2025
        self.assertEqual(user_with_canteens.nb_cantines_td_2025, 1)
        # self.assertEqual(user_with_canteens.nb_cantines_td_todo_2025, 1)  # nb_bilans_2025 - nb_td_2025

        self.assertEqual(user_without_canteens.nb_cantines_bilan_2025, 0)
        self.assertEqual(user_without_canteens.nb_cantines_bilan_todo_2025, 0)
        self.assertEqual(user_without_canteens.nb_cantines_td_2025, 0)
        # self.assertEqual(user_without_canteens.nb_cantines_td_todo_2025, 0)

    def test_model_method_update_data(self):
        self.assertIsNone(self.user_with_canteens.data)

        user_qs = User.objects.with_canteen_stats().with_canteen_diagnostic_stats()
        self.user_with_canteens = user_qs.get(id=self.user_with_canteens.id)
        self.user_with_canteens.update_data()
        self.user_with_canteens.refresh_from_db()

        self.assertEqual(self.user_with_canteens.data["nb_cantines"], 6)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_groupe"], 1 + 1)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_site"], 2)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_satellite"], 1)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_gestion_concedee"], 1)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_bilan_2025"], 2)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_bilan_todo_2025"], 4)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_td_2025"], 1)
        # self.assertEqual(self.user_with_canteens.data["nb_cantines_td_todo_2025"], 1)

        self.user_without_canteens = user_qs.get(id=self.user_without_canteens.id)
        self.user_without_canteens.update_data()
        self.user_without_canteens.refresh_from_db()

        self.assertEqual(self.user_without_canteens.data["nb_cantines"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_groupe"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_site"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_satellite"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_gestion_concedee"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_bilan_2025"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_bilan_todo_2025"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_td_2025"], 0)
        # self.assertEqual(self.user_without_canteens.data["nb_cantines_td_todo_2025"], 0)
