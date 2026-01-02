from django.test import TestCase

from data.factories import CanteenFactory, UserFactory
from data.models import Canteen, User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_with_canteens = UserFactory()
        cls.user_without_canteens = UserFactory()

        cls.canteen_empty = CanteenFactory(managers=[cls.user_with_canteens])
        Canteen.objects.filter(id=cls.canteen_empty.id).update(
            production_type=None, management_type=None, economic_model=None
        )
        cls.canteen_centrale = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            satellite_canteens_count=1,
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

    def test_queryset_with_canteen_stats(self):
        user_qs = User.objects.with_canteen_stats()

        user_with_canteens = user_qs.get(id=self.user_with_canteens.id)
        user_without_canteens = user_qs.get(id=self.user_without_canteens.id)

        self.assertEqual(user_with_canteens.nb_cantines, 5)
        self.assertEqual(user_with_canteens.nb_cantines_groupe, 1)
        self.assertEqual(user_with_canteens.nb_cantines_site, 2)
        self.assertEqual(user_with_canteens.nb_cantines_satellite, 1)
        self.assertEqual(user_with_canteens.nb_cantines_gestion_concedee, 1)

        self.assertEqual(user_without_canteens.nb_cantines, 0)
        self.assertEqual(user_without_canteens.nb_cantines_groupe, 0)
        self.assertEqual(user_without_canteens.nb_cantines_site, 0)
        self.assertEqual(user_without_canteens.nb_cantines_satellite, 0)
        self.assertEqual(user_without_canteens.nb_cantines_gestion_concedee, 0)

    def test_model_method_update_data(self):
        self.assertIsNone(self.user_with_canteens.data)

        user_qs = User.objects.with_canteen_stats()
        self.user_with_canteens = user_qs.get(id=self.user_with_canteens.id)
        self.user_with_canteens.update_data()
        self.user_with_canteens.refresh_from_db()

        self.assertEqual(self.user_with_canteens.data["nb_cantines"], 5)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_groupe"], 1)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_site"], 2)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_satellite"], 1)
        self.assertEqual(self.user_with_canteens.data["nb_cantines_gestion_concedee"], 1)

        self.user_without_canteens = user_qs.get(id=self.user_without_canteens.id)
        self.user_without_canteens.update_data()
        self.user_without_canteens.refresh_from_db()

        self.assertEqual(self.user_without_canteens.data["nb_cantines"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_groupe"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_site"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_satellite"], 0)
        self.assertEqual(self.user_without_canteens.data["nb_cantines_gestion_concedee"], 0)
