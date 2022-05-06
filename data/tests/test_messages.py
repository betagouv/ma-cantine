from django.test import TestCase
from django.core import mail
from django.test.utils import override_settings
from django.utils.timezone import now
from data.models import Message
from data.factories import MessageFactory, CanteenFactory, UserFactory


@override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
@override_settings(CONTACT_EMAIL="contact@example.com")
class TestMessageModel(TestCase):
    def test_send_message(self):
        canteen = CanteenFactory.create()
        managers = [UserFactory.create(), UserFactory.create()]
        canteen.managers.set(managers)
        message = MessageFactory.create(destination_canteen=canteen, sender_email="test@example.com")
        self.assertEqual(message.status, Message.Status.PENDING)

        message.send()
        message.refresh_from_db()

        email = mail.outbox[0]
        self.assertEqual(len(email.to), canteen.managers.all().count() + 1)
        self.assertIn(managers[0].email, email.to)
        self.assertIn(managers[1].email, email.to)
        self.assertIn("contact@example.com", email.to)
        self.assertEqual(email.from_email, "no-reply@example.com")
        self.assertEqual(len(email.reply_to), 1)
        self.assertEqual(email.reply_to[0], "test@example.com")

        self.assertIsNotNone(message.sent_date)
        self.assertEqual(message.status, Message.Status.SENT)

    def test_resend_message(self):
        message = MessageFactory.create(status=Message.Status.SENT, sent_date=now())
        self.assertRaises(Exception, message.send)

    def test_block_message(self):
        message = MessageFactory.create()
        message.block()
        message.refresh_from_db()
        self.assertEqual(message.status, Message.Status.BLOCKED)

    def test_block_sent_message(self):
        message = MessageFactory.create(status=Message.Status.SENT, sent_date=now())
        self.assertRaises(Exception, message.block)
