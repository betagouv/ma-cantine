from unittest import mock

# import sib_api_v3_sdk
from django.test import TestCase
from freezegun import freeze_time

from data.factories import (
    CanteenFactory,
    DiagnosticFactory,
    TeledeclarationFactory,
    UserFactory,
)
from data.models import Canteen, Diagnostic, Teledeclaration
from macantine import tasks


class TestBrevoUserData(TestCase):
    def _find_payload_for_user(contacts, user_email):
        return next(filter(lambda x: x.email == user_email, contacts))

    @freeze_time("2021-01-20")
    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_batch_user_updates(self, batch_update_mock, create_contact_mock):
        """
        A new user without canteens will have all paramteres related to the diagnostic,
        TD and publication to `False` because they can't be missing them without even having
        a canteen.
        """
        new_user = UserFactory.create()
        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_not_called()

        payload = TestBrevoUserData._find_payload_for_user(batch_update_mock.call_args[0][0].contacts, new_user.email)
        self.assertEqual(payload.email, new_user.email)

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
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_PUBLICATION"), False)

    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_create_user(self, batch_update_mock, create_contact_mock):
        """
        If the batch update fails then the user will be created/updated individually
        """
        new_user = UserFactory.create()
        batch_update_mock.side_effect = Exception("Error !")

        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        self.assertEqual(payload.email, new_user.email)

    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_user_has_empty_canteen(self, batch_update_mock, create_contact_mock):
        """
        As soon as a user has a canteen, pending actions will follow and all paramteres
        related to the diagnostic, TD and publication will be active
        """
        user = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(user)

        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_not_called()

        payload = TestBrevoUserData._find_payload_for_user(batch_update_mock.call_args[0][0].contacts, user.email)
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_PUBLICATION"), True)

    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_user_has_published_canteen(self, batch_update_mock, create_contact_mock):
        user = UserFactory.create()
        canteen = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED)
        canteen.managers.add(user)

        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_not_called()

        payload = TestBrevoUserData._find_payload_for_user(batch_update_mock.call_args[0][0].contacts, user.email)
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_PUBLICATION"), False)

    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_user_has_canteen_with_diag(self, batch_update_mock, create_contact_mock):
        user = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(user)

        DiagnosticFactory.create(year=2021, canteen=canteen)
        DiagnosticFactory.create(year=2022, canteen=canteen)

        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_not_called()

        payload = TestBrevoUserData._find_payload_for_user(batch_update_mock.call_args[0][0].contacts, user.email)
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_PUBLICATION"), True)

    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_user_has_canteen_with_td(self, batch_update_mock, create_contact_mock):
        user = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(user)

        diag_2021 = DiagnosticFactory.create(year=2021, canteen=canteen)
        diag_2022 = DiagnosticFactory.create(year=2022, canteen=canteen)

        TeledeclarationFactory.create(
            diagnostic=diag_2021,
            year=2021,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"year": 2021},
            canteen=canteen,
        )
        TeledeclarationFactory.create(
            diagnostic=diag_2022,
            year=2022,
            status=Teledeclaration.TeledeclarationStatus.CANCELLED,
            declared_data={"year": 2022},
            canteen=canteen,
        )

        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_not_called()

        payload = TestBrevoUserData._find_payload_for_user(batch_update_mock.call_args[0][0].contacts, user.email)
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_PUBLICATION"), True)

    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_user_has_sat_canteen_with_cc_diag(self, batch_update_mock, create_contact_mock):
        user = UserFactory.create()
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="65815950319874")
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
        )
        canteen.managers.add(user)

        DiagnosticFactory.create(
            year=2021,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        DiagnosticFactory.create(
            year=2022,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_not_called()

        payload = TestBrevoUserData._find_payload_for_user(batch_update_mock.call_args[0][0].contacts, user.email)
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_PUBLICATION"), True)

    @mock.patch("macantine.tasks.contacts_api_instance.create_contact")
    @mock.patch("macantine.tasks.contacts_api_instance.update_batch_contacts")
    def test_user_has_sat_canteen_with_cc_td(self, batch_update_mock, create_contact_mock):
        user = UserFactory.create()
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="65815950319874")
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
        )
        canteen.managers.add(user)

        diag_2021 = DiagnosticFactory.create(
            year=2021,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        diag_2022 = DiagnosticFactory.create(
            year=2022,
            canteen=central_kitchen,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        TeledeclarationFactory.create(
            diagnostic=diag_2021,
            year=2021,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"year": 2021},
            canteen=central_kitchen,
        )
        TeledeclarationFactory.create(
            diagnostic=diag_2022,
            year=2022,
            status=Teledeclaration.TeledeclarationStatus.CANCELLED,
            declared_data={"year": 2022},
            canteen=central_kitchen,
        )

        tasks.update_brevo_contacts()
        batch_update_mock.assert_called_once()
        create_contact_mock.assert_not_called()

        payload = TestBrevoUserData._find_payload_for_user(batch_update_mock.call_args[0][0].contacts, user.email)
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_GERE_UN_ETABLISSEMENT"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_PUBLICATION"), True)
