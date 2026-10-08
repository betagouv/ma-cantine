from django.test import TestCase

from data.factories import ApplicationFactory
from data.models import Oauth2ProviderApplicationExtra


class Oauth2ProviderApplicationExtraTest(TestCase):
    def create_application(self):
        return ApplicationFactory(name="Test Application")

    def test_extra_created_on_application_creation(self):
        application = self.create_application()

        self.assertEqual(Oauth2ProviderApplicationExtra.objects.count(), 1)
        self.assertEqual(application.extra.company_name, "")

    def test_extra_not_recreated_on_application_update(self):
        application = self.create_application()
        application.extra.company_name = "Éditeur"
        application.extra.save()

        application.name = "Test Application (renamed)"
        application.save()

        self.assertEqual(Oauth2ProviderApplicationExtra.objects.count(), 1)
        application.refresh_from_db()
        self.assertEqual(application.extra.company_name, "Éditeur")

    def test_extra_deleted_with_application(self):
        application = self.create_application()
        application.delete()

        self.assertEqual(Oauth2ProviderApplicationExtra.objects.count(), 0)
