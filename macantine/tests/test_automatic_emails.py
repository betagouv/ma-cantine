from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from data.factories import CanteenFactory, UserFactory
from macantine import tasks


class TestAutomaticEmails(TestCase):
    def test_no_canteen_first_reminder(self):
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
        # TODO: Mock SIB API to ensure the endpoint is hit only once with the right info

        jean.refresh_from_db()
        anna.refresh_from_db()
        sophie.refresh_from_db()
        fred.refresh_from_db()

        self.assertIsNotNone(jean.email_no_canteen_first_reminder)
        self.assertIsNone(anna.email_no_canteen_first_reminder)
        self.assertIsNone(sophie.email_no_canteen_first_reminder)

    def test_no_canteen_second_reminder(self):
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
        )
        tasks.no_canteen_second_reminder()
        # TODO: Mock SIB API to ensure the endpoint is hit only once with the right info

        jean.refresh_from_db()
        anna.refresh_from_db()
        sophie.refresh_from_db()
        fred.refresh_from_db()
        marie.refresh_from_db()

        self.assertIsNotNone(marie.email_no_canteen_second_reminder)
        self.assertIsNone(jean.email_no_canteen_second_reminder)
        self.assertIsNone(anna.email_no_canteen_second_reminder)
        self.assertIsNone(sophie.email_no_canteen_second_reminder)
