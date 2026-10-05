from django.test import TestCase
from oauth2_provider.models import get_application_model

from data.factories import UserFactory
from data.models import Oauth2ProviderApplicationExtra

Application = get_application_model()


class Oauth2ProviderApplicationExtraTest(TestCase):
    def create_application(self):
        return Application.objects.create(
            name="Test Application",
            user=UserFactory(),
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris="http://localhost",
        )

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
