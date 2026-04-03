from unittest import skipIf

from django.conf import settings
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, ImportFailure, ImportType, Sector


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensUpdateImportApiErrorTest(APITestCase):
    def test_unauthenticated(self):
        response = self.client.post(reverse("canteens_update_import"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_validata_missing_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        canteen = CanteenFactory()
        canteen.managers.add(authenticate.user)

        file_path = "./api/tests/files/canteens/canteens_update_bad_no_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_UPDATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["field"], "Première ligne du fichier incorrecte")
        self.assertEqual(
            errors[0]["title"],
            "Elle doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_error_canteen_not_found(self):
        """
        User cannot update a canteen that doesn't exist
        """
        file_path = "./api/tests/files/canteens/canteens_update_bad_canteen_not_found.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_UPDATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["message"], "Une cantine avec le siret « 999999 » n'existe pas sur la plateforme.")

    @authenticate
    def test_error_permission_denied(self):
        """
        User cannot update a canteen they don't manage
        """
        canteen = CanteenFactory(id=9999999999)
        self.assertNotIn(authenticate.user, canteen.managers.all())

        file_path = "./api/tests/files/canteens/canteens_update_bad_permission_denied.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_UPDATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("Vous n'êtes pas un gestionnaire de cette cantine", errors[0]["message"])

    @authenticate
    def test_error_invalid_city_insee_code(self):
        """
        City insee code must be 5 characters when siren_unite_legale is provided
        """
        canteen = CanteenFactory(id=9999999997)
        canteen.managers.add(authenticate.user)

        file_path = "./api/tests/files/canteens/canteens_update_bad_invalid_insee_code.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_UPDATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'Code INSEE' : Le code INSEE « 750 » n'est pas valide, il doit contenir 5 caractères (ex : 75056).",
        )

    @authenticate
    def test_error_invalid_manager_email(self):
        """
        Manager email must be valid
        """
        canteen = CanteenFactory(id=9999999996)
        canteen.managers.add(authenticate.user)

        file_path = "./api/tests/files/canteens/canteens_update_bad_invalid_email.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_UPDATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'email' : Un adresse email des gestionnaires (invalid-email) n'est pas valide.",
        )

    @authenticate
    def test_error_invalid_siret(self):
        """
        Siret must be valid
        """
        canteen = CanteenFactory(id=12345)
        canteen.managers.add(authenticate.user)

        file_path = "./api/tests/files/canteens/canteens_update_bad_invalid_siret.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_UPDATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["message"], "Champ 'siret' : 14 caractères numériques sont attendus")

    @authenticate
    def test_error_missing_city_insee_code(self):
        """
        City insee code is required when siren_unite_legale is provided
        """
        canteen = CanteenFactory(id=9999999997)
        canteen.managers.add(authenticate.user)

        file_path = "./api/tests/files/canteens/canteens_update_bad_missing_insee_code.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_UPDATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'Code INSEE' : Le code INSEE est obligatoire pour les cantines avec le 'siren_unite_legale' de renseigné.",
        )

    @authenticate
    def test_when_errors_count_is_0(self):
        CanteenFactory(siret="21340172201787", managers=[authenticate.user], id=9999999993)

        file_path = "./api/tests/files/canteens/canteens_update_bad_one_error.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertTrue(len(body["errors"]) > 0)


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensUpdateImportApiGroupeTeledeclarationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.groupe_canteen = CanteenFactory(id=9999999992, production_type=Canteen.ProductionType.GROUPE)
        cls.satellite_canteen = CanteenFactory(
            id=9999999991,
            siret=None,
            siren_unite_legale="213401722",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.groupe_canteen,
        )
        cls.teledeclaration = DiagnosticFactory(canteen=cls.groupe_canteen, year=2024)

    @freeze_time("2025-02-20")  # during the 2024 campaign
    @authenticate
    def test_error_groupe_with_teledeclaration_during_campaign(self):
        """
        User cannot add a satellite to a groupe that has a teledeclared diagnostic for the current campaign during the teledeclaration campaign
        """
        # Create a teledeclared diagnostic for the groupe
        self.groupe_canteen.managers.add(authenticate.user)
        self.satellite_canteen.managers.add(authenticate.user)
        self.teledeclaration.teledeclare(applicant=authenticate.user)

        # Import
        file_path = "./api/tests/files/canteens/canteens_update_bad_groupe_teledeclared.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertIn(
            "Vous ne pouvez pas ajouter de restaurant satellite au groupe « 9999999992 », car il possède un bilan télédéclaré (campagne de télédéclaration en cours). Veuillez annuler la télédéclaration pour pouvoir ajouter le(s) restaurant(s) satellite(s).",
            errors[0]["message"],
        )

    @authenticate
    def test_success_groupe_with_teledeclaration_cancelled_during_correction_campaign(self):
        """
        User can add it canteen to a groupe if the groupe has cancelled its teledeclaration
        """
        self.groupe_canteen.managers.add(authenticate.user)
        self.satellite_canteen.managers.add(authenticate.user)
        with freeze_time("2025-01-20"):  # during the 2024 campaign
            self.teledeclaration.teledeclare(applicant=authenticate.user)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            self.teledeclaration.cancel()

            file_path = "./api/tests/files/canteens/canteens_update_bad_groupe_teledeclared.csv"
            with open(file_path) as canteen_file:
                response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            body = response.json()
            errors = body["errors"]
            self.assertEqual(body["count"], 1)
            self.assertEqual(len(body["canteens"]), 1)
            self.assertEqual(len(errors), 0)
            self.assertEqual(self.satellite_canteen.groupe, self.groupe_canteen)

    @authenticate
    def test_success_groupe_with_teledeclaration_after_campaign(self):
        """
        User can add a satellite to a groupe that has a teledeclared diagnostic for the current campaign after the teledeclaration campaign
        """
        self.groupe_canteen.managers.add(authenticate.user)
        self.satellite_canteen.managers.add(authenticate.user)

        # Create a teledeclared diagnostic for the groupe and the satellite
        with freeze_time("2025-01-20"):  # during the 2024 campaign
            self.teledeclaration.teledeclare(applicant=authenticate.user)

        # Import
        with freeze_time("2025-07-20"):
            file_path = "./api/tests/files/canteens/canteens_update_bad_groupe_teledeclared.csv"
            with open(file_path) as canteen_file:
                response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            body = response.json()
            errors = body["errors"]
            self.assertEqual(body["count"], 1)
            self.assertEqual(len(body["canteens"]), 1)
            self.assertEqual(len(errors), 0)

    @freeze_time("2025-01-20")  # during the 2024 campaign
    @authenticate
    def test_success_groupe_teledeclaration_cancelled_during_campaign(self):
        """
        User can add a satellite to a groupe that does not have a teledeclared diagnostic for the current campaign during the campaign
        """
        # Create a teledeclared diagnostic for the groupe
        self.groupe_canteen.managers.add(authenticate.user)
        self.satellite_canteen.managers.add(authenticate.user)
        self.teledeclaration.teledeclare(applicant=authenticate.user)

        # Cancel the teledeclared diagnostic
        self.teledeclaration.cancel()

        # Import
        file_path = "./api/tests/files/canteens/canteens_update_bad_groupe_teledeclared.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(errors), 0)


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensUpdateImportApiSuccessTest(APITestCase):
    @authenticate
    def test_update_multiple_canteens(self):
        """
        Should be able to update multiple canteens at once
        """
        canteen1 = CanteenFactory(
            id=9999999993,
            siret="21340172201787",
            name="Canteen 1",
            daily_meal_count=3,
            yearly_meal_count=420,
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
        )
        canteen1.siret = None
        canteen1.siren_unite_legale = "213401722"
        canteen1.save(skip_validations=True)
        canteen2 = CanteenFactory(
            id=9999999994,
            siren_unite_legale=None,
            siret="50250039850458",
            name="Canteen 2",
            daily_meal_count=6,
            yearly_meal_count=840,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            management_type=Canteen.ManagementType.CONCEDED,
            economic_model=Canteen.EconomicModel.PRIVATE,
            sector_list=[Sector.ENTERPRISE_ENTREPRISE],
        )
        canteen2.siren_unite_legale = None
        canteen2.save(skip_validations=True)
        canteen1.managers.add(authenticate.user)
        canteen2.managers.add(authenticate.user)

        file_path = "./api/tests/files/canteens/canteens_update_good_multiple.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(body["count"], 2)
        self.assertEqual(len(body["canteens"]), 2)
        self.assertEqual(len(errors), 0, errors)

        canteen1.refresh_from_db()
        canteen2.refresh_from_db()
        # siret / siren
        self.assertEqual(canteen1.siret, "21340172201787")
        self.assertEqual(canteen1.siren_unite_legale, None)
        self.assertEqual(canteen2.siret, None)
        self.assertEqual(canteen2.siren_unite_legale, "502500398")
        # nom
        self.assertEqual(canteen1.name, "Canteen 1 Updated")
        self.assertEqual(canteen2.name, "Canteen 2 Updated")
        # code insee
        self.assertEqual(canteen2.city_insee_code, "75010")
        # nombre de repas par jour
        self.assertEqual(canteen1.daily_meal_count, 100)
        self.assertEqual(canteen2.daily_meal_count, 200)
        # nombre de repas par an
        self.assertEqual(canteen1.yearly_meal_count, 10000)
        self.assertEqual(canteen2.yearly_meal_count, 20000)
        # type de production
        self.assertEqual(canteen1.production_type, Canteen.ProductionType.ON_SITE_CENTRAL)
        self.assertEqual(canteen2.production_type, Canteen.ProductionType.ON_SITE)
        # type de gestion
        self.assertEqual(canteen1.management_type, Canteen.ManagementType.CONCEDED)
        self.assertEqual(canteen2.management_type, Canteen.ManagementType.DIRECT)
        # modèle économique
        self.assertEqual(canteen1.economic_model, Canteen.EconomicModel.PRIVATE)
        self.assertEqual(canteen2.economic_model, Canteen.EconomicModel.PUBLIC)
        # secteurs
        self.assertEqual(canteen1.sector_list, [Sector.ENTERPRISE_ENTREPRISE])
        self.assertEqual(canteen2.sector_list, [Sector.EDUCATION_PRIMAIRE])

    @authenticate
    def test_update_canteen_with_siret_and_insee_code(self):
        """
        Should be able to update a canteen with a siret and if an insee code is in import file it's not saved
        """
        canteen = CanteenFactory(
            id=9999999995,
            siret="21340172201787",
        )
        canteen.managers.add(authenticate.user)

        canteen.city_insee_code = "75020"
        canteen.save(skip_validations=True)
        self.assertEqual(canteen.city_insee_code, "75020")

        file_path = "./api/tests/files/canteens/canteens_update_good_insee.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(errors), 0, errors)

        canteen.refresh_from_db()
        self.assertEqual(canteen.city_insee_code, "75020")

    # TODO : add test admin can update canteen they don't manage
    @authenticate
    def test_update_canteen_as_admin(self):
        """
        Should be able to update a canteen if not manager but admin
        """
        canteen = CanteenFactory(
            id=9999999998,
            siret="21340172201787",
            name="Ma cantine",
        )
        user = authenticate.user
        user.is_staff = True
        user.save()

        file_path = "./api/tests/files/canteens/canteens_update_good_one.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(errors), 0, errors)

        canteen.refresh_from_db()
        self.assertEqual(canteen.name, "Test Canteen")

    @authenticate
    def test_update_canteen_with_excel_file(self):
        """
        Should be able to update a canteen with an excel file
        """
        canteen = CanteenFactory(
            id=9999999998,
            siret="21340172201787",
            name="Ma cantine",
        )
        canteen.managers.add(authenticate.user)

        file_path = "./api/tests/files/canteens/canteens_update_good_one.xlsx"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(reverse("canteens_update_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(errors), 0, errors)

        canteen.refresh_from_db()
        self.assertEqual(canteen.name, "Test Canteen")
