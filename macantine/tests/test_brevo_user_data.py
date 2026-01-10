from unittest import mock

# import sib_api_v3_sdk
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic
from macantine import tasks


class TestBrevoUserData(TestCase):
    def _find_payload_for_user(contacts, user_email):
        return next(filter(lambda x: x.email == user_email, contacts))

    @freeze_time("2021-01-20")
    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_create_new_user(self, batch_update_mock, create_contact_mock):
        """
        A new user without canteens will have all parameters related to the diagnostic,
        TD and publication to `False` because they can't be missing them without even having
        a canteen.
        """
        new_user = UserFactory()

        tasks.update_user_data()  # needed to fill the User.data field
        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_DATE_INSCRIPTION"), "2021-01-20")
        self.assertEqual(attributes.get("MA_CANTINE_COMPTE_DEV"), new_user.is_dev)
        self.assertEqual(attributes.get("MA_CANTINE_COMPTE_ELU_E"), new_user.is_elected_official)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 0)
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
        As soon as a user has a canteen, pending actions will follow and all parameters
        related to the diagnostic, TD and publication will be active
        """
        user = UserFactory()
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user])

        tasks.update_user_data()  # needed to fill the User.data field
        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
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
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user])
        DiagnosticFactory(year=2021, canteen=canteen_site)
        DiagnosticFactory(year=2022, canteen=canteen_site)

        tasks.update_user_data()  # needed to fill the User.data field
        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
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
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user])
        with freeze_time("2022-08-30"):  # during the 2021 campaign
            DiagnosticFactory(year=2021, canteen=canteen_site)  # not teledeclared
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            DiagnosticFactory(year=2022, canteen=canteen_site).teledeclare(applicant=user)

        tasks.update_user_data()  # needed to fill the User.data field
        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_has_sat_canteen_with_cc_diag(self, batch_update_mock, create_contact_mock):
        user = UserFactory()
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[])
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=canteen_groupe, managers=[user])
        DiagnosticFactory(
            year=2021,
            canteen=canteen_groupe,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        DiagnosticFactory(
            year=2022,
            canteen=canteen_groupe,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        tasks.update_user_data()  # needed to fill the User.data field
        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_has_groupe_canteen_with_td(self, batch_update_mock, create_contact_mock):
        user = UserFactory()
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[user])
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=canteen_groupe, managers=[])
        with freeze_time("2022-08-30"):  # during the 2021 campaign
            DiagnosticFactory(
                year=2021,
                canteen=canteen_groupe,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            )  # not teledeclared
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            DiagnosticFactory(
                year=2022,
                canteen=canteen_groupe,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            ).teledeclare(applicant=user)

        tasks.update_user_data()  # needed to fill the User.data field
        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_BILAN_DONNEES_2021"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2023"), True)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2022"), False)
        self.assertEqual(attributes.get("MA_CANTINE_MANQUE_TD_DONNEES_2021"), True)
