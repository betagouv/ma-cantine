from unittest import mock

# import sib_api_v3_sdk
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, TeledeclarationFactory, UserFactory
from data.models import Canteen, Diagnostic, Teledeclaration
from macantine import tasks


class TestBrevoUserData(TestCase):
    def _find_payload_for_user(contacts, user_email):
        return next(filter(lambda x: x.email == user_email, contacts))

    @freeze_time("2021-01-20")
    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_create_new_user(self, batch_update_mock, create_contact_mock):
        """
        A new user without canteens will have all paramteres related to the diagnostic,
        TD and publication to `False` because they can't be missing them without even having
        a canteen.
        """
        new_user = UserFactory()
        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_DATE_INSCRIPTION"), "2021-01-20")
        self.assertEqual(attributes.get("MA_CANTINE_COMPTE_DEV"), new_user.is_dev)
        self.assertEqual(attributes.get("MA_CANTINE_COMPTE_ELU_E"), new_user.is_elected_official)
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), False)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_has_empty_canteen(self, batch_update_mock, create_contact_mock):
        """
        As soon as a user has a canteen, pending actions will follow and all paramteres
        related to the diagnostic, TD and publication will be active
        """
        user = UserFactory()
        CanteenFactory(managers=[user])

        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_has_canteen_with_diag(self, batch_update_mock, create_contact_mock):
        user = UserFactory()
        canteen = CanteenFactory(managers=[user])

        DiagnosticFactory(year=2021, canteen=canteen)
        DiagnosticFactory(year=2022, canteen=canteen)

        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_has_canteen_with_td(self, batch_update_mock, create_contact_mock):
        user = UserFactory()
        canteen = CanteenFactory(managers=[user])

        diag_2021 = DiagnosticFactory(year=2021, canteen=canteen)
        diag_2022 = DiagnosticFactory(year=2022, canteen=canteen)

        TeledeclarationFactory(
            diagnostic=diag_2021,
            year=2021,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"year": 2021},
            canteen=canteen,
            applicant=user,
        )
        TeledeclarationFactory(
            diagnostic=diag_2022,
            year=2022,
            status=Teledeclaration.TeledeclarationStatus.CANCELLED,
            declared_data={"year": 2022},
            canteen=canteen,
            applicant=user,
        )

        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), False)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_has_sat_canteen_with_cc_diag(self, batch_update_mock, create_contact_mock):
        user = UserFactory()
        central_kitchen = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, siret="65815950319874", managers=[user]
        )
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen.siret,
            managers=[user],
        )

        DiagnosticFactory(
            year=2021,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        DiagnosticFactory(
            year=2022,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_has_sat_canteen_with_cc_td(self, batch_update_mock, create_contact_mock):
        user = UserFactory()
        central_kitchen = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, siret="65815950319874", managers=[user]
        )
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen.siret,
            managers=[user],
        )

        diag_2021 = DiagnosticFactory(
            year=2021,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        diag_2022 = DiagnosticFactory(
            year=2022,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        TeledeclarationFactory(
            diagnostic=diag_2021,
            year=2021,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"year": 2021},
            canteen=central_kitchen,
            applicant=user,
        )
        TeledeclarationFactory(
            diagnostic=diag_2022,
            year=2022,
            status=Teledeclaration.TeledeclarationStatus.CANCELLED,
            declared_data={"year": 2022},
            canteen=central_kitchen,
            applicant=user,
        )

        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), False)
