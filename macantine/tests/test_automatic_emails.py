from unittest import mock
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from django.test.utils import override_settings
from data.factories import CanteenFactory, UserFactory, DiagnosticFactory
from data.models import Canteen
from macantine import tasks


class TestAutomaticEmails(TestCase):
    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=1)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_no_canteen_first_reminder(self, _):
        """
        The email should be sent to users who have joined more
        than a week ago but have not created any canteens nor have they
        previously received the email.
        """
        today = timezone.now()

        # Should send email
        jean = UserFactory.create(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
        )

        # Should not send email because user already has a canteen
        anna = UserFactory.create(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Anna",
            last_name="Logue",
        )
        canteen_anna = CanteenFactory.create()
        canteen_anna.managers.add(anna)

        # Should not send email because account is too recent
        sophie = UserFactory.create(
            date_joined=(today - timedelta(days=1)),
            email_no_canteen_first_reminder=None,
            first_name="Sophie",
            last_name="Stiqué",
        )

        # Should not send email because already sent 10 minutes ago
        fred = UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(minutes=10)),
            first_name="Fred",
            last_name="Ulcorant",
        )
        tasks.no_canteen_first_reminder()

        # Email is only sent once to Jean
        tasks._send_sib_template.assert_called_once_with(
            1, {"PRENOM": "Jean"}, "jean.serien@example.com", "Jean Sérien"
        )

        # DB objects are updated
        jean.refresh_from_db()
        anna.refresh_from_db()
        sophie.refresh_from_db()
        fred.refresh_from_db()

        self.assertIsNotNone(jean.email_no_canteen_first_reminder)
        self.assertIsNone(anna.email_no_canteen_first_reminder)
        self.assertIsNone(sophie.email_no_canteen_first_reminder)

    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=2)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_no_canteen_second_reminder(self, _):
        """
        The second reminder email should be sent to users who have joined more
        than two weeks ago, have not created any canteens, and have already
        received the first email at least a week ago (the text references it)
        """
        today = timezone.now()

        # Should not send because first reminder was only sent yesterday
        jean = UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(days=1)),
            email_no_canteen_second_reminder=None,
            first_name="Jean",
            last_name="Sérien",
        )

        # Should not send because user has a canteen
        anna = UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(days=10)),
            email_no_canteen_second_reminder=None,
            first_name="Anna",
            last_name="Logue",
        )
        canteen_anna = CanteenFactory.create()
        canteen_anna.managers.add(anna)

        # Should not send because she hasn't received the first reminder
        sophie = UserFactory.create(
            date_joined=(today - timedelta(weeks=3)),
            email_no_canteen_first_reminder=None,
            email_no_canteen_second_reminder=None,
            first_name="Sophie",
            last_name="Stiqué",
        )

        # Should not send because it has already been sent
        fred = UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=2)),
            email_no_canteen_second_reminder=(today - timedelta(weeks=1)),
            first_name="Fred",
            last_name="Ulcorant",
        )

        # Should send
        marie = UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            first_name="Marie",
            last_name="Olait",
            email="marie.olait@example.com",
        )
        tasks.no_canteen_second_reminder()

        # Email is only sent once to Jean
        tasks._send_sib_template.assert_called_once_with(
            2, {"PRENOM": "Marie"}, "marie.olait@example.com", "Marie Olait"
        )

        jean.refresh_from_db()
        anna.refresh_from_db()
        sophie.refresh_from_db()
        fred.refresh_from_db()
        marie.refresh_from_db()

        self.assertIsNotNone(marie.email_no_canteen_second_reminder)
        self.assertIsNone(jean.email_no_canteen_second_reminder)
        self.assertIsNone(anna.email_no_canteen_second_reminder)
        self.assertIsNone(sophie.email_no_canteen_second_reminder)

    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=None)
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=None)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_no_template_settings(self, _):
        today = timezone.now()
        # Should send first email if template was entered
        UserFactory.create(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
        )

        # Should send second email if template was entered
        UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            first_name="Marie",
            last_name="Olait",
            email="marie.olait@example.com",
        )
        tasks.no_canteen_first_reminder()
        tasks.no_canteen_second_reminder()

        tasks._send_sib_template.assert_not_called()

    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=1)
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=2)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_emails_should_only_be_sent_once(self, _):
        today = timezone.now()
        # Should send first email
        UserFactory.create(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
        )

        # Should send second email
        UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            first_name="Marie",
            last_name="Olait",
            email="marie.olait@example.com",
        )

        # Even if we triggered the functions several times, only one email
        # should be sent per person
        tasks.no_canteen_first_reminder()
        tasks.no_canteen_first_reminder()
        tasks.no_canteen_first_reminder()
        tasks._send_sib_template.assert_called_once_with(
            1, {"PRENOM": "Jean"}, "jean.serien@example.com", "Jean Sérien"
        )

        tasks._send_sib_template.reset_mock()

        tasks.no_canteen_second_reminder()
        tasks.no_canteen_second_reminder()
        tasks.no_canteen_second_reminder()
        tasks._send_sib_template.assert_called_once_with(
            2, {"PRENOM": "Marie"}, "marie.olait@example.com", "Marie Olait"
        )

    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_DIAGNOSTIC_FIRST=1)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_no_diagnostic_first_reminder(self, _):
        """
        The email should be sent to managers of a canteen created more than
        a week ago, and without any diagnostics.
        """
        today = timezone.now()

        # We create a canteen with no diagnostics managed by
        # Jean and Anna. Both should receive the email since
        # the canteen was created more than a week ago.
        jean = UserFactory.create(
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
        )
        anna = UserFactory.create(
            first_name="Anna",
            last_name="Logue",
            email="anna.logue@example.com",
        )
        canteen_no_diagnostics = CanteenFactory.create(
            managers=[
                anna,
                jean,
            ]
        )
        Canteen.objects.filter(pk=canteen_no_diagnostics.id).update(creation_date=(today - timedelta(weeks=2)))

        # We create another canteen with no diagnostics managed by
        # Sophie, but this time no email should be sent since the
        # canteen was only created three days ago.
        sophie = UserFactory.create(
            first_name="Sophie",
            last_name="Stiqué",
        )
        canteen_no_diagnostics_recent = CanteenFactory.create(
            managers=[
                sophie,
            ]
        )
        Canteen.objects.filter(pk=canteen_no_diagnostics_recent.id).update(creation_date=(today - timedelta(days=3)))

        # We create a canteen with diagnostics. Because of this,
        # managers should not be notified.
        fred = UserFactory.create(
            first_name="Fred",
            last_name="Ulcorant",
        )

        canteen_with_diagnostics = CanteenFactory.create(
            managers=[
                fred,
            ]
        )
        Canteen.objects.filter(pk=canteen_with_diagnostics.id).update(creation_date=(today - timedelta(weeks=3)))
        DiagnosticFactory.create(canteen=canteen_with_diagnostics)

        # Finally, we create a canteen with no diagnostics for which
        # an email has already been sent, so the managers should not
        # be notified again.
        lena = UserFactory.create(
            first_name="Lena",
            last_name="Godard",
            email="lena.godard@example.com",
        )
        canteen_no_diagnostics_contacted = CanteenFactory.create(
            email_no_diagnostic_first_reminder=(today - timedelta(weeks=1)),
            managers=[
                lena,
            ],
        )
        Canteen.objects.filter(pk=canteen_no_diagnostics_contacted.id).update(
            creation_date=(today - timedelta(weeks=2))
        )

        # From all of these managers, only jean and anna should be notified.
        tasks.no_diagnostic_first_reminder()

        # Email is only sent once to Jean
        tasks._send_sib_template.assert_called
        self.assertEqual(tasks._send_sib_template.call_count, 2)
        call_args_list = tasks._send_sib_template.call_args_list
        self.assertEqual(call_args_list[0][0][2], "jean.serien@example.com")
        self.assertEqual(call_args_list[1][0][2], "anna.logue@example.com")

        # DB objects are updated
        canteen_no_diagnostics.refresh_from_db()
        self.assertIsNotNone(canteen_no_diagnostics.email_no_diagnostic_first_reminder)

    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=1)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_email_opt_out_first_reminder(self, _):
        """
        The email should not be sent to users that have opted-out of the
        reminder emails.
        """
        today = timezone.now()

        jean = UserFactory.create(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
            opt_out_reminder_emails=True,
        )
        tasks.no_canteen_first_reminder()

        tasks._send_sib_template.assert_not_called()

        self.assertIsNone(jean.email_no_canteen_first_reminder)

    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=2)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_opt_out_second_reminder(self, _):
        """
        The email should not be sent to users that have opted-out of the
        reminder emails.
        """
        today = timezone.now()

        marie = UserFactory.create(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            first_name="Marie",
            last_name="Olait",
            email="marie.olait@example.com",
            opt_out_reminder_emails=True,
        )
        tasks.no_canteen_second_reminder()

        # Email is only sent once to Jean
        tasks._send_sib_template.assert_not_called()

        marie.refresh_from_db()

        self.assertIsNone(marie.email_no_canteen_second_reminder)

    @mock.patch("macantine.tasks._send_sib_template")
    @override_settings(TEMPLATE_ID_NO_DIAGNOSTIC_FIRST=1)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_opt_out_no_diagnostic_first_reminder(self, _):
        """
        The email should not be sent to users that have opted-out of the
        reminder emails.
        """
        today = timezone.now()

        # Only Anna should receive the email since Jean has opted out
        jean = UserFactory.create(
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
            opt_out_reminder_emails=True,
        )
        anna = UserFactory.create(
            first_name="Anna",
            last_name="Logue",
            email="anna.logue@example.com",
        )
        canteen_no_diagnostics = CanteenFactory.create(
            managers=[
                anna,
                jean,
            ]
        )
        Canteen.objects.filter(pk=canteen_no_diagnostics.id).update(creation_date=(today - timedelta(weeks=2)))

        tasks.no_diagnostic_first_reminder()

        # Email is only sent once to Anna
        tasks._send_sib_template.assert_called
        self.assertEqual(tasks._send_sib_template.call_count, 1)
        call_args_list = tasks._send_sib_template.call_args_list
        self.assertEqual(call_args_list[0][0][2], "anna.logue@example.com")

        # DB objects are updated
        canteen_no_diagnostics.refresh_from_db()
        self.assertIsNotNone(canteen_no_diagnostics.email_no_diagnostic_first_reminder)
