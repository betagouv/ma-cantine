from unittest import mock

# import sib_api_v3_sdk
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic
from macantine import tasks


class BrevoUserDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def _find_payload_for_user(contacts, user_email):
        return next(filter(lambda x: x.email == user_email, contacts))

    @freeze_time("2026-01-30")  # during the 2025 campaign
    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_without_canteen(self, batch_update_mock, create_contact_mock):
        user_without_canteen = UserFactory()

        # run task to fill the User.data field
        tasks.update_user_data()
        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_DATE_INSCRIPTION"), "2026-01-30")
        self.assertEqual(attributes.get("MA_CANTINE_COMPTE_DEV"), user_without_canteen.is_dev)
        self.assertEqual(attributes.get("MA_CANTINE_COMPTE_ELU_E"), user_without_canteen.is_elected_official)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_site(self, batch_update_mock, create_contact_mock):
        user_with_canteen = UserFactory()
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user_with_canteen])

        # run task to fill the User.data field
        tasks.update_user_data()
        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_site_diagnostic(self, batch_update_mock, create_contact_mock):
        user_with_canteen = UserFactory()
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user_with_canteen])
        DiagnosticFactory(year=2022, canteen=canteen_site)
        DiagnosticFactory(year=2025, canteen=canteen_site)

        # run task to fill the User.data field
        tasks.update_user_data()
        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes

        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_site_diagnostic_td(self, batch_update_mock, create_contact_mock):
        user_with_canteen = UserFactory()
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[user_with_canteen])
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            DiagnosticFactory(year=2021, canteen=canteen_site)  # not teledeclared
        with freeze_time("2026-01-30"):  # during the 2025 campaign
            DiagnosticFactory(year=2025, canteen=canteen_site).teledeclare(applicant=user_with_canteen)

        # run tasks to fill the Canteen.declaration_donnees_year & User.data fields
        tasks.canteen_fill_declaration_donnees_year_field()
        tasks.update_user_data()
        tasks.update_brevo_contacts()
        batch_update_mock.assert_not_called()
        create_contact_mock.assert_called_once()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 1)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_sat_groupe_diagnostic(self, batch_update_mock, create_contact_mock):
        user_with_canteen_sat = UserFactory()
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[])
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=canteen_groupe,
            managers=[user_with_canteen_sat],
        )
        DiagnosticFactory(
            year=2022,
            canteen=canteen_groupe,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        DiagnosticFactory(
            year=2025,
            canteen=canteen_groupe,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        # run tasks to fill the Canteen.declaration_donnees_year & User.data fields
        tasks.canteen_fill_declaration_donnees_year_field()
        tasks.update_user_data()
        tasks.update_brevo_contacts()
        create_contact_mock.assert_called_once()
        batch_update_mock.assert_not_called()

        payload = create_contact_mock.call_args[0][0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 0)

    @mock.patch("macantine.brevo.contacts_api_instance.create_contact")
    @mock.patch("macantine.brevo.contacts_api_instance.update_batch_contacts")
    def test_user_with_canteen_sat_groupe_diagnostic_td(self, batch_update_mock, create_contact_mock):
        user_with_canteen_groupe = UserFactory()
        user_with_canteen_sat = UserFactory()
        canteen_groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE, managers=[user_with_canteen_groupe]
        )
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=canteen_groupe,
            managers=[user_with_canteen_sat],
        )
        with freeze_time("2023-03-30"):  # during the 2022 campaign
            DiagnosticFactory(
                year=2022,
                canteen=canteen_groupe,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            )  # not teledeclared
        with freeze_time("2026-01-30"):  # during the 2025 campaign
            DiagnosticFactory(
                year=2025,
                canteen=canteen_groupe,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            ).teledeclare(applicant=user_with_canteen_groupe)

        # run tasks to fill the Canteen.declaration_donnees_year & User.data fields
        tasks.canteen_fill_declaration_donnees_year_field()
        tasks.update_user_data()
        tasks.update_brevo_contacts()
        self.assertEqual(create_contact_mock.call_count, 2)
        batch_update_mock.assert_not_called()

        # user_with_canteen_groupe
        payload = create_contact_mock.call_args_list[0].args[0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("NOM_COMPLET"), user_with_canteen_groupe.get_full_name())
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 1)
        # user_with_canteen_sat
        payload = create_contact_mock.call_args_list[1].args[0]
        attributes = payload.attributes
        self.assertEqual(attributes.get("NOM_COMPLET"), user_with_canteen_sat.get_full_name())
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_GROUPE"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_SATELLITE"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_2025"), 0)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_BILAN_TODO_2025"), 1)
        self.assertEqual(attributes.get("MA_CANTINE_NB_CANTINES_TD_2025"), 1)  # groupe has td
