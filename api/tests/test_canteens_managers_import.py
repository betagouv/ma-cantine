from unittest import skipIf

from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory, UserFactory
from data.models import ImportFailure, ImportType, ManagerInvitation


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensManagersImportApiNonAdminErrorTest(APITestCase):
    def test_unauthenticated(self):
        """
        Anonymous users should receive 403 Forbidden
        """
        response = self.client.post(reverse("canteens_managers_import"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_non_staff_user_forbidden(self):
        """
        Non-staff authenticated users should receive a PermissionDenied error
        """
        CanteenFactory(siret="21340172201787")

        file_path = "./api/tests/files/canteen_managers/canteen_managers_good.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            "Vous n'avez pas les permissions nécessaires pour importer des gestionnaires en masse.",
            errors[0]["message"],
        )


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensManagersImportApiErrorTest(APITestCase):
    @authenticate
    def test_validata_missing_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        # Hack : this test works because file has no header and has less columns than the expected header
        # TODO: remove this hack add fix it in other imports
        file_path = "./api/tests/files/canteen_managers/canteen_managers_bad_no_header.csv"
        with open(file_path, "rb") as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_MANAGERS, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["field"], "Première ligne du fichier incorrecte")

    @authenticate
    def test_validata_wrong_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        file_path = "./api/tests/files/canteen_managers/canteen_managers_bad_wrong_header.csv"
        with open(file_path, "rb") as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_MANAGERS, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertGreater(len(errors), 0)
        for error in errors:
            self.assertTrue(error["title"].startswith("Valeur incorrecte vous avez écrit"))

    @authenticate
    def test_validata_extra_header_error(self):
        """
        A file should not be valid if it has extra columns
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        file_path = "./api/tests/files/canteen_managers/canteen_managers_bad_extra_header.csv"
        with open(file_path, "rb") as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_MANAGERS, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("colonnes supplémentaires", errors[0]["field"])

    @authenticate
    def test_validata_empty_rows_error(self):
        """
        A file should not be valid if it contains empty rows
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        file_path = "./api/tests/files/canteen_managers/canteen_managers_bad_empty_rows.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_MANAGERS, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertTrue(errors[0]["field"].startswith("ligne vide"))

    @authenticate
    def test_canteen_not_found(self):
        """
        Import should fail if the SIRET doesn't match any existing canteen
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        file_path = "./api/tests/files/canteen_managers/canteen_managers_bad_siret_not_found.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_MANAGERS, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("Aucune cantine avec le SIRET", errors[0]["message"])

    @authenticate
    def test_invalid_manager_email(self):
        """
        Import should fail if an email in gestionnaires_additionnels is invalid
        """
        user = authenticate.user
        user.is_staff = True
        user.save()
        CanteenFactory(siret="21340172201787")

        file_path = "./api/tests/files/canteen_managers/canteen_managers_bad_invalid_email.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_MANAGERS, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("n'est pas valide", errors[0]["message"])

    @authenticate
    def test_when_errors_count_is_0(self):
        user = authenticate.user
        user.is_staff = True
        user.save()
        CanteenFactory(siret="21340172201787")
        CanteenFactory(siret="40419443300078")

        file_path = "./api/tests/files/canteen_managers/canteen_managers_bad_one_error.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertTrue(len(body["errors"]) > 0)

    @authenticate
    @override_settings(CSV_IMPORT_MAX_SIZE=1)
    def test_file_above_max_size(self):
        """
        Files exceeding CSV_IMPORT_MAX_SIZE should fail
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        file_path = "./api/tests/files/canteen_managers/canteen_managers_good.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_MANAGERS, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertIn("trop grand", errors[0]["message"])


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensManagersImportApiSuccessTest(APITestCase):
    @authenticate
    def test_admin_import_managers_success(self):
        """
        Staff user should successfully add managers to existing canteens without sending invitation emails
        """
        user = authenticate.user
        user.is_staff = True
        user.save()
        canteen = CanteenFactory(siret="21340172201787")
        canteen.managers.clear()

        self.assertEqual(canteen.managers.count(), 0)
        self.assertEqual(ManagerInvitation.objects.count(), 0)

        file_path = "./api/tests/files/canteen_managers/canteen_managers_good.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(errors), 0, errors)

        # Check managers were added via invitations (silently, no email sent)
        canteen.refresh_from_db()
        self.assertEqual(canteen.managers.count(), 0)
        self.assertEqual(ManagerInvitation.objects.filter(canteen=canteen).count(), 2)
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen, email="manager1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen, email="manager2@example.com"))

        # Verify import source was updated
        self.assertEqual(canteen.import_source, "test_import")

    @authenticate
    def test_admin_import_managers_existing_manager(self):
        """
        If manager is already on the canteen, should not fail (IntegrityError caught)
        """
        user = authenticate.user
        user.is_staff = True
        user.save()
        existing_manager = UserFactory(email="manager1@example.com")
        canteen = CanteenFactory(siret="21340172201787")
        canteen.managers.add(existing_manager)

        file_path = "./api/tests/files/canteen_managers/canteen_managers_good.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        # Existing manager should still be there
        canteen.refresh_from_db()
        self.assertIn(existing_manager, canteen.managers.all())

    @authenticate
    def test_admin_import_multiple_canteens(self):
        """
        Staff user can import managers for multiple canteens at once
        """
        user = authenticate.user
        user.is_staff = True
        user.save()
        canteen1 = CanteenFactory(siret="21340172201787")
        canteen1.managers.clear()
        canteen2 = CanteenFactory(siret="21380185500015")
        canteen2.managers.clear()

        file_path = "./api/tests/files/canteen_managers/canteen_managers_good_multiple.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 2)
        self.assertEqual(len(body["canteens"]), 2)
        self.assertEqual(len(errors), 0, errors)

        # Check managers were added to both canteens
        self.assertEqual(ManagerInvitation.objects.filter(canteen=canteen1).count(), 2)
        self.assertEqual(ManagerInvitation.objects.filter(canteen=canteen2).count(), 1)

    @authenticate
    def test_import_excel_file(self):
        """
        Staff user can import Excel (.xlsx) files
        """
        user = authenticate.user
        user.is_staff = True
        user.save()
        canteen = CanteenFactory(siret="21340172201787")
        canteen.managers.clear()

        file_path = "./api/tests/files/canteen_managers/canteen_managers_good.xlsx"
        with open(file_path, "rb") as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)
        self.assertEqual(len(body["canteens"]), 1)

        # Check managers were added
        self.assertEqual(ManagerInvitation.objects.filter(canteen=canteen).count(), 2)

    @authenticate
    def test_import_for_canteen_not_filled(self):
        """
        Staff user can add managers to a canteen not filled
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        # Create a canteen with an error in a field
        canteen = CanteenFactory(siret="21340172201787")
        canteen.yearly_meal_count = None
        canteen.save(skip_validations=True)
        canteen.managers.clear()

        self.assertFalse(canteen.is_filled)

        file_path = "./api/tests/files/canteen_managers/canteen_managers_good.csv"
        with open(file_path) as managers_file:
            response = self.client.post(reverse("canteens_managers_import"), {"file": managers_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)
