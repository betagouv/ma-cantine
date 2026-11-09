from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice

from data.admin.diagnostic import DiagnosticAdmin
from data.factories import DiagnosticFactory, UserFactory
from data.models import Diagnostic


class DiagnosticAdminTest(TestCase):
    def setUp(self):
        self.model_admin = DiagnosticAdmin(Diagnostic, admin.site)
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.request = RequestFactory().get("/")
        self.request.user = self.user

    def test_get_form_labels_depend_on_the_year(self):
        for year, valeur_bio_label in [
            (2025, "Bio - Valeur annuelle HT"),
            (2026, "Total des achats bio ou avec mention « En conversion vers l'agriculture biologique »"),
        ]:
            with self.subTest(year=year):
                diagnostic = Diagnostic(year=year, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
                form = self.model_admin.get_form(self.request, diagnostic)
                self.assertEqual(form.base_fields["valeur_bio"].label, valeur_bio_label)
                # also used by the readonly fields (e.g. teledeclared diagnostics)
                self.assertEqual(form._meta.labels["valeur_bio"], valeur_bio_label)

    def test_get_form_without_obj(self):
        form = self.model_admin.get_form(self.request)
        self.assertIsNone(form._meta.labels)

    def test_change_view_teledeclared_diagnostic_readonly_fields_labels(self):
        diagnostic = DiagnosticFactory(
            year=2026,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            status=Diagnostic.DiagnosticStatus.SUBMITTED,
        )
        device = TOTPDevice.objects.create(user=self.user, name="test", confirmed=True)
        self.client.force_login(self.user)
        # Mark the OTP device as verified for this session, as django_otp.login() would
        session = self.client.session
        session["otp_device_id"] = device.persistent_id
        session.save()

        response = self.client.get(reverse("admin:data_diagnostic_change", args=[diagnostic.id]))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["has_change_permission"])  # all the fields are readonly
        self.assertContains(
            response,
            #  : non-breaking space before the label suffix (french locale)
            "<label>Total des achats bio ou avec mention « En conversion vers l'agriculture biologique » :</label>",
            html=True,
        )
