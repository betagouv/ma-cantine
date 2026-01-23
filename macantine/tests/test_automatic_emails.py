from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from data.factories import CanteenFactory, UserFactory
from macantine import brevo, tasks


class TestAutomaticEmails(TestCase):
    @mock.patch("macantine.brevo.send_sib_template")
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
        jean = UserFactory(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
        )

        # Should not send email because user already has a canteen
        anna = UserFactory(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Anna",
            last_name="Logue",
        )
        canteen_anna = CanteenFactory()
        canteen_anna.managers.add(anna)

        # Should not send email because account is too recent
        sophie = UserFactory(
            date_joined=(today - timedelta(days=1)),
            email_no_canteen_first_reminder=None,
            first_name="Sophie",
            last_name="Stiqué",
        )

        # Should not send email because already sent 10 minutes ago
        fred = UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(minutes=10)),
            first_name="Fred",
            last_name="Ulcorant",
        )
        tasks.no_canteen_first_reminder()

        # Email is only sent once to Jean
        brevo.send_sib_template.assert_called_once_with(
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

    @mock.patch("macantine.brevo.send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=1)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_no_canteen_dev_profile(self, _):
        """
        The email should be not be sent to users with a dev profile, even
        if they have all other parameters
        """
        today = timezone.now()

        # Should not send email
        jean = UserFactory(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
            is_dev=True,
        )

        tasks.no_canteen_first_reminder()
        brevo.send_sib_template.assert_not_called()

        jean.refresh_from_db()
        self.assertIsNone(jean.email_no_canteen_first_reminder)

    @mock.patch("macantine.brevo.send_sib_template")
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
        jean = UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(days=1)),
            email_no_canteen_second_reminder=None,
            first_name="Jean",
            last_name="Sérien",
        )

        # Should not send because user has a canteen
        anna = UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(days=10)),
            email_no_canteen_second_reminder=None,
            first_name="Anna",
            last_name="Logue",
        )
        canteen_anna = CanteenFactory()
        canteen_anna.managers.add(anna)

        # Should not send because she hasn't received the first reminder
        sophie = UserFactory(
            date_joined=(today - timedelta(weeks=3)),
            email_no_canteen_first_reminder=None,
            email_no_canteen_second_reminder=None,
            first_name="Sophie",
            last_name="Stiqué",
        )

        # Should not send because it has already been sent
        fred = UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=2)),
            email_no_canteen_second_reminder=(today - timedelta(weeks=1)),
            first_name="Fred",
            last_name="Ulcorant",
        )

        # Should send
        marie = UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            username="marie.olait",
            first_name="",
            last_name="",
            email="marie.olait@example.com",
        )
        tasks.no_canteen_second_reminder()

        # Email is only sent once to Marie
        brevo.send_sib_template.assert_called_once_with(2, {"PRENOM": ""}, "marie.olait@example.com", "marie.olait")

        jean.refresh_from_db()
        anna.refresh_from_db()
        sophie.refresh_from_db()
        fred.refresh_from_db()
        marie.refresh_from_db()

        self.assertIsNotNone(marie.email_no_canteen_second_reminder)
        self.assertIsNone(jean.email_no_canteen_second_reminder)
        self.assertIsNone(anna.email_no_canteen_second_reminder)
        self.assertIsNone(sophie.email_no_canteen_second_reminder)

    @mock.patch("macantine.brevo.send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=2)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_no_canteen_second_reminder_dev(self, _):
        """
        The second reminder email should not be sent to dev users
        """
        today = timezone.now()

        marie = UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            first_name="Marie",
            last_name="Olait",
            email="marie.olait@example.com",
            is_dev=True,
        )
        tasks.no_canteen_second_reminder()
        brevo.send_sib_template.assert_not_called()

        marie.refresh_from_db()
        self.assertIsNone(marie.email_no_canteen_second_reminder)

    @mock.patch("macantine.brevo.send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=None)
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=None)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_no_template_settings(self, _):
        today = timezone.now()
        # Should send first email if template was entered
        UserFactory(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
        )

        # Should send second email if template was entered
        UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            first_name="Marie",
            last_name="Olait",
            email="marie.olait@example.com",
        )
        tasks.no_canteen_first_reminder()
        tasks.no_canteen_second_reminder()

        brevo.send_sib_template.assert_not_called()

    @mock.patch("macantine.brevo.send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=1)
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=2)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_emails_should_only_be_sent_once(self, _):
        today = timezone.now()
        # Should send first email
        UserFactory(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
        )

        # Should send second email
        UserFactory(
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
        brevo.send_sib_template.assert_called_once_with(
            1, {"PRENOM": "Jean"}, "jean.serien@example.com", "Jean Sérien"
        )

        brevo.send_sib_template.reset_mock()

        tasks.no_canteen_second_reminder()
        tasks.no_canteen_second_reminder()
        tasks.no_canteen_second_reminder()
        brevo.send_sib_template.assert_called_once_with(
            2, {"PRENOM": "Marie"}, "marie.olait@example.com", "Marie Olait"
        )

    @mock.patch("macantine.brevo.send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_FIRST=1)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_email_opt_out_first_reminder(self, _):
        """
        The email should not be sent to users that have opted-out of the
        reminder emails.
        """
        today = timezone.now()

        jean = UserFactory(
            date_joined=(today - timedelta(weeks=1)),
            email_no_canteen_first_reminder=None,
            first_name="Jean",
            last_name="Sérien",
            email="jean.serien@example.com",
            opt_out_reminder_emails=True,
        )
        tasks.no_canteen_first_reminder()

        brevo.send_sib_template.assert_not_called()

        self.assertIsNone(jean.email_no_canteen_first_reminder)

    @mock.patch("macantine.brevo.send_sib_template")
    @override_settings(TEMPLATE_ID_NO_CANTEEN_SECOND=2)
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_opt_out_second_reminder(self, _):
        """
        The email should not be sent to users that have opted-out of the
        reminder emails.
        """
        today = timezone.now()

        marie = UserFactory(
            date_joined=(today - timedelta(weeks=2)),
            email_no_canteen_first_reminder=(today - timedelta(weeks=1)),
            email_no_canteen_second_reminder=None,
            first_name="Marie",
            last_name="Olait",
            email="marie.olait@example.com",
            opt_out_reminder_emails=True,
        )
        tasks.no_canteen_second_reminder()

        brevo.send_sib_template.assert_not_called()

        marie.refresh_from_db()

        self.assertIsNone(marie.email_no_canteen_second_reminder)
