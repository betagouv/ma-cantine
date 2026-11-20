import json
import logging
from unittest import mock

# import sib_api_v3_sdk
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from sib_api_v3_sdk.rest import ApiException

from common.tests.utils import date_in_campaign
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic, User
from macantine import brevo, tasks


class BrevoUserDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def _find_payload_for_user(contacts, user_email):
        return next(filter(lambda x: x.email == user_email, contacts))

    @freeze_time(date_in_campaign(2025))
    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_without_canteen(self, batch_update_mock, create_contact_mock):
        user_without_canteen = UserFactory()

        # run task to fill the User.data field
        call_command("user_update_data")
        call_command("user_update_brevo_contacts")
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_DATE_INSCRIPTION"), "2026-01-13")
        self.assertEqual(attributes.get("MA_CANTINE_COMPTE_DEV"), user_without_canteen.is_dev)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_site(self, batch_update_mock, create_contact_mock):
        user_with_canteen = UserFactory()
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user_with_canteen])

        # run task to fill the User.data field
        call_command("user_update_data")
        call_command("user_update_brevo_contacts")
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_site_diagnostic(self, batch_update_mock, create_contact_mock):
        user_with_canteen = UserFactory()
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user_with_canteen])
        DiagnosticFactory(year=2022, canteen=canteen_site)
        DiagnosticFactory(year=2025, canteen=canteen_site)

        # run task to fill the User.data field
        call_command("user_update_data")
        call_command("user_update_brevo_contacts")
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_TODO_2025"), 1)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_site_diagnostic_td(self, batch_update_mock, create_contact_mock):
        user_with_canteen = UserFactory()
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user_with_canteen])
        with freeze_time(date_in_campaign(2022)):
            DiagnosticFactory(year=2021, canteen=canteen_site)  # not teledeclared
        with freeze_time(date_in_campaign(2025)):
            DiagnosticFactory(year=2025, canteen=canteen_site).teledeclare(applicant=user_with_canteen)

        # run tasks to fill the Canteen.declaration_donnees_year & User.data fields
        tasks.canteen_fill_declaration_donnees_year_field()
        call_command("user_update_data")
        call_command("user_update_brevo_contacts")
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_TODO_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_sat_groupe_diagnostic(self, batch_update_mock, create_contact_mock):
        user_with_canteen_sat = UserFactory()
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[])
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=canteen_groupe,
            managers=[user_with_canteen_sat],
        )
        DiagnosticFactory(
            year=2022,
            canteen=canteen_groupe,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        DiagnosticFactory(
            year=2025,
            canteen=canteen_groupe,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        # run tasks to fill the Canteen.declaration_donnees_year & User.data fields
        tasks.canteen_fill_declaration_donnees_year_field()
        call_command("user_update_data")
        call_command("user_update_brevo_contacts")
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_sat_groupe_diagnostic_td(self, batch_update_mock, create_contact_mock):
        user_with_canteen_groupe = UserFactory()
        user_with_canteen_sat = UserFactory()
        canteen_groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE, managers=[user_with_canteen_groupe]
        )
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=canteen_groupe,
            managers=[user_with_canteen_sat],
        )
        with freeze_time(date_in_campaign(2022)):
            DiagnosticFactory(
                year=2022,
                canteen=canteen_groupe,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            )  # not teledeclared
        with freeze_time(date_in_campaign(2025)):
            DiagnosticFactory(
                year=2025,
                canteen=canteen_groupe,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            ).teledeclare(applicant=user_with_canteen_groupe)

        # run tasks to fill the Canteen.declaration_donnees_year & User.data fields
        tasks.canteen_fill_declaration_donnees_year_field()
        call_command("user_update_data")
        call_command("user_update_brevo_contacts")
        self.assertEqual(create_contact_mock.call_count, 2)
        batch_update_mock.assert_not_called()

        # user_with_canteen_groupe
        payload = next(
            call.args[0]
            for call in create_contact_mock.call_args_list
            if call.args[0].email == user_with_canteen_groupe.email
        )
        attributes = payload.attributes
        self.assertEqual(attributes.get("NOM_COMPLET"), user_with_canteen_groupe.get_full_name())
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 1)
        # user_with_canteen_sat
        payload = next(
            call.args[0]
            for call in create_contact_mock.call_args_list
            if call.args[0].email == user_with_canteen_sat.email
        )
        attributes = payload.attributes
        self.assertEqual(attributes.get("NOM_COMPLET"), user_with_canteen_sat.get_full_name())
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 1)  # TODO: should we set to 0?
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 1)  # groupe has td


class BrevoUserSyncDateTest(TestCase):
    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_sync_sets_brevo_last_update_date_without_user_save(self, batch_update_mock, create_contact_mock):
        user_to_create = UserFactory()
        user_to_update = UserFactory()
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        User.objects.filter(id=user_to_update.id).update(brevo_last_update_date=two_days_ago)

        # direct update: no User.save() (validations, avatar optimization...)
        with mock.patch.object(User, "save") as save_mock:
            call_command("user_update_brevo_contacts")
        save_mock.assert_not_called()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_called_once()

        user_to_create.refresh_from_db()
        user_to_update.refresh_from_db()
        self.assertIsNotNone(user_to_create.brevo_last_update_date)
        self.assertGreater(user_to_update.brevo_last_update_date, two_days_ago)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact", side_effect=Exception("Brevo error"))
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts", side_effect=Exception("Brevo error"))
    def test_sync_error_keeps_brevo_last_update_date(self, batch_update_mock, create_contact_mock):
        user_to_create = UserFactory()
        user_to_update = UserFactory()
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        User.objects.filter(id=user_to_update.id).update(brevo_last_update_date=two_days_ago)

        call_command("user_update_brevo_contacts")

        user_to_create.refresh_from_db()
        user_to_update.refresh_from_db()
        self.assertIsNone(user_to_create.brevo_last_update_date)
        self.assertEqual(user_to_update.brevo_last_update_date, two_days_ago)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_sync_logs_counts(self, batch_update_mock, create_contact_mock):
        UserFactory.create_batch(2)
        user_to_update = UserFactory()
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        User.objects.filter(id=user_to_update.id).update(brevo_last_update_date=two_days_ago)

        # logging is disabled in the tests (see macantine/tests/__init__.py): enable it for this test only
        logging.disable(logging.NOTSET)
        self.addCleanup(logging.disable, logging.CRITICAL)
        with self.assertLogs("macantine.management.commands.user_update_brevo_contacts", level="INFO") as logs:
            call_command("user_update_brevo_contacts")
        # counted before the sync
        self.assertTrue(any("(2 to create, 1 to update)" in message for message in logs.output))


def brevo_api_exception(status, body):
    error = ApiException(status=status, reason="Error")
    error.body = json.dumps(body).encode()
    return error


def brevo_contact_not_found_exception(indexes):
    return brevo_api_exception(
        404, {"code": "document_not_found", "message": f"No contact found for indexes {indexes}"}
    )


@mock.patch("macantine.brevo.time.sleep")
class BrevoUserBatchContactsNotFoundTest(TestCase):
    def setUp(self):
        self.users = UserFactory.create_batch(3)
        self.two_days_ago = timezone.now() - timezone.timedelta(days=2)
        User.objects.filter(id__in=[user.id for user in self.users]).update(brevo_last_update_date=self.two_days_ago)

    def _sync(self):
        users = list(User.objects.filter(id__in=[user.id for user in self.users]).order_by("id"))
        return brevo.update_existing_brevo_contacts([users], timezone.now())

    @mock.patch("macantine.brevo.contacts_api_instance.get_contact_info")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_missing_contact_is_flagged_and_batch_retried(self, batch_update_mock, get_contact_mock, _):
        batch_update_mock.side_effect = [brevo_contact_not_found_exception("1"), None]
        get_contact_mock.side_effect = brevo_api_exception(404, {"code": "document_not_found"})

        flagged_user_ids = self._sync()

        self.assertEqual(flagged_user_ids, [self.users[1].id])
        get_contact_mock.assert_called_once_with(self.users[1].email)
        # retried without the missing contact
        self.assertEqual(batch_update_mock.call_count, 2)
        retried_emails = [contact.email for contact in batch_update_mock.call_args.args[0].contacts]
        self.assertEqual(retried_emails, [self.users[0].email, self.users[2].email])
        # flagged (excluded from the next syncs), the others are synced
        self.assertTrue(User.objects.get(id=self.users[1].id).brevo_is_deleted)
        self.assertEqual(User.objects.get(id=self.users[1].id).brevo_last_update_date, self.two_days_ago)
        for user in [self.users[0], self.users[2]]:
            self.assertFalse(User.objects.get(id=user.id).brevo_is_deleted)
            self.assertGreater(User.objects.get(id=user.id).brevo_last_update_date, self.two_days_ago)

    @mock.patch("macantine.brevo.contacts_api_instance.get_contact_info")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_several_missing_contacts(self, batch_update_mock, get_contact_mock, _):
        batch_update_mock.side_effect = [brevo_contact_not_found_exception("0, 2"), None]
        get_contact_mock.side_effect = brevo_api_exception(404, {"code": "document_not_found"})

        flagged_user_ids = self._sync()

        self.assertEqual(flagged_user_ids, [self.users[0].id, self.users[2].id])
        retried_emails = [contact.email for contact in batch_update_mock.call_args.args[0].contacts]
        self.assertEqual(retried_emails, [self.users[1].email])

    @mock.patch("macantine.brevo.contacts_api_instance.get_contact_info")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_contact_exists_in_brevo_nobody_flagged(self, batch_update_mock, get_contact_mock, _):
        # the index doesn't match a missing contact: don't flag anyone
        batch_update_mock.side_effect = brevo_contact_not_found_exception("1")
        get_contact_mock.return_value = {"email": self.users[1].email}

        flagged_user_ids = self._sync()

        self.assertEqual(flagged_user_ids, [])
        batch_update_mock.assert_called_once()
        self.assertEqual(User.objects.filter(brevo_is_deleted=True).count(), 0)
        self.assertEqual(User.objects.filter(brevo_last_update_date=self.two_days_ago).count(), 3)

    @mock.patch("macantine.brevo.contacts_api_instance.get_contact_info")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_other_errors_nobody_flagged(self, batch_update_mock, get_contact_mock, _):
        for error in [
            brevo_api_exception(404, {"code": "document_not_found", "message": "unexpected message"}),
            brevo_api_exception(400, {"code": "invalid_parameter", "message": "Invalid email address"}),
            brevo_api_exception(500, {"code": "internal_error"}),
            Exception("network error"),
        ]:
            with self.subTest(error=str(error)):
                batch_update_mock.reset_mock()
                batch_update_mock.side_effect = error

                flagged_user_ids = self._sync()

                self.assertEqual(flagged_user_ids, [])
                batch_update_mock.assert_called_once()
                get_contact_mock.assert_not_called()
                self.assertEqual(User.objects.filter(brevo_is_deleted=True).count(), 0)
                self.assertEqual(User.objects.filter(brevo_last_update_date=self.two_days_ago).count(), 3)

    @mock.patch("macantine.brevo.contacts_api_instance.get_contact_info")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_retries_are_limited(self, batch_update_mock, get_contact_mock, _):
        # each attempt reveals another missing contact: stops after 1 + CONTACT_BULK_UPDATE_MAX_RETRIES attempts
        self.users.append(UserFactory(brevo_last_update_date=self.two_days_ago))
        batch_update_mock.side_effect = brevo_contact_not_found_exception("0")
        get_contact_mock.side_effect = brevo_api_exception(404, {"code": "document_not_found"})

        flagged_user_ids = self._sync()

        self.assertEqual(batch_update_mock.call_count, 1 + brevo.CONTACT_BULK_UPDATE_MAX_RETRIES)
        self.assertEqual(flagged_user_ids, [user.id for user in self.users[:3]])
        # the last user is neither flagged nor synced (retried the next night)
        last_user = User.objects.get(id=self.users[3].id)
        self.assertFalse(last_user.brevo_is_deleted)
        self.assertEqual(last_user.brevo_last_update_date, self.two_days_ago)
