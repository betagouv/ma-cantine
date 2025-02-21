import filecmp

from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from data.factories import CanteenFactory
from data.models import ImportFailure, ImportType

from .utils import authenticate


class TestImportDiagnosticsAPI(APITestCase):
    def _assertImportFailureCreated(self, user, type, file_path):
        self.assertEqual(ImportFailure.objects.count(), 1)
        self.assertEqual(ImportFailure.objects.first().user, user)
        self.assertEqual(ImportFailure.objects.first().import_type, type)
        self.assertTrue(filecmp.cmp(file_path, ImportFailure.objects.first().file.path, shallow=False))

    @authenticate
    def test_complete_diagnostic_error(self):
        file_path = "./api/tests/files/diagnostics/diagnostics_complete_bad.csv"
        with open(file_path) as diag_file:
            self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})

        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_COMPLETE, file_path)

    @authenticate
    def test_error_not_a_manager(self):
        CanteenFactory.create(siret="21340172201787")
        my_canteen = CanteenFactory.create(siret="73282932000074")
        my_canteen.managers.add(authenticate.user)
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv"

        with open(file_path) as diag_file:
            self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

    @authenticate
    def test_invalid_sectors_error(self):
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_sectors.csv"
        with open(file_path) as diag_file:
            self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

    @authenticate
    def test_staff_import_non_staff_error(self):
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_staff_good_new_canteen.csv"
        with open(file_path) as diag_file:
            self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

    @authenticate
    def test_several_error(self):
        CanteenFactory.create(siret="42111303053388")
        CanteenFactory.create(siret="42111303053388")
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad.csv"

        with open(file_path) as diag_file:
            self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

    @override_settings(CSV_IMPORT_MAX_SIZE=1)
    @authenticate
    def test_max_size_error(self):
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_separator_semicolon_decimal_number.csv"
        with open(file_path) as diag_file:
            self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

    @authenticate
    def test_managers_invalid_email_error(self):
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_separator_semicolon_add_managers.csv"
        with open(file_path) as diag_file:
            self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

    @authenticate
    def test_success_diagnostic_import(self):
        with open("./api/tests/files/diagnostics/diagnostics_complete_good.csv") as diag_file:
            self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})

        self.assertFalse(ImportFailure.objects.exists())

    @authenticate
    def test_mandatory_total_ht_error(self):
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_separator_semicolon_no_total_ht.csv"
        with open(file_path) as diag_file:
            self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

        self._assertImportFailureCreated(authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
