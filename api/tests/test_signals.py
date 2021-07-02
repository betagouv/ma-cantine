from data.models import ProvisionalManager
from data.factories.provisionalmanager import ProvisionalManagerFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class TestSignals(APITestCase):
    def test_new_user_linked_successfully(self):
        """
        A new user with an email matching the email in the provisional managers table, 
        should be added to the list of canteen managers
        """
        pms = [
            ProvisionalManagerFactory.create(email="smith@example.com"),
            ProvisionalManagerFactory.create(email="smith@example.com")
        ]
        canteens = [pms[0].canteen, pms[1].canteen]

        user = get_user_model()(email="smith@example.com", username="smith.example")
        user.save()

        for canteen in canteens:
            self.assertTrue(len(canteen.managers.all()) > 1)
            self.assertEqual(canteen.managers.all().filter(email="smith@example.com").count(), 1)

        self.assertEqual(len(ProvisionalManager.objects.all()), 0)