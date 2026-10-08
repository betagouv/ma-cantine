from django.test import TestCase

from oauth2_provider.models import get_application_model

from data.factories import (
    ApplicationFactory,
    CanteenFactory,
    DiagnosticFactory,
    PurchaseFactory,
    WasteMeasurementFactory,
)
from data.models import Canteen, Oauth2ProviderApplicationExtra
from data.models.creation_source import CreationSource
from data.models.oauth2 import annotate_with_created_counts


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


class AnnotateWithCreatedCountsTest(TestCase):
    def test_created_counts(self):
        application = ApplicationFactory()
        other_application = ApplicationFactory()
        api = {"creation_source": CreationSource.API, "creation_source_api_oauth2_application": application}
        CanteenFactory(**api)
        deleted_canteen = CanteenFactory(**api)
        Canteen.all_objects.filter(id=deleted_canteen.id).update(deletion_date=deleted_canteen.creation_date)
        CanteenFactory(creation_source=CreationSource.API, creation_source_api_oauth2_application=other_application)
        DiagnosticFactory(**api)
        DiagnosticFactory(**api)
        DiagnosticFactory(**api)
        PurchaseFactory(**api)
        WasteMeasurementFactory(**api)

        application = annotate_with_created_counts(get_application_model().objects.filter(id=application.id)).get()

        self.assertEqual(application.canteens_created_count, 2)  # deleted canteen included
        self.assertEqual(application.diagnostics_created_count, 3)
        self.assertEqual(application.purchases_created_count, 1)
        self.assertEqual(application.waste_measurements_created_count, 1)

    def test_created_counts_zero(self):
        application = annotate_with_created_counts(get_application_model().objects.filter(id=ApplicationFactory().id))
        application = application.get()

        self.assertEqual(application.canteens_created_count, 0)
        self.assertEqual(application.diagnostics_created_count, 0)
        self.assertEqual(application.purchases_created_count, 0)
        self.assertEqual(application.waste_measurements_created_count, 0)
