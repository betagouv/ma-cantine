from django.core.exceptions import ValidationError
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector


year_data = 2024
date_in_teledeclaration_campaign = "2025-03-30"
date_in_correction_campaign = "2025-04-20"
date_in_last_teledeclaration_campaign = "2024-02-01"


class DiagnosticTeledeclaredQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_not_filled_draft = DiagnosticFactory(canteen=CanteenFactory(), valeur_totale=None)
        cls.diagnostic_filled_draft = DiagnosticFactory(canteen=CanteenFactory(), valeur_totale=1000)
        cls.diagnostic_filled_submitted = DiagnosticFactory(
            canteen=CanteenFactory(), valeur_totale=1000, status=Diagnostic.DiagnosticStatus.SUBMITTED
        )

    def test_teledeclared_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 3)
        self.assertEqual(Diagnostic.objects.teledeclared().count(), 1)

    def test_is_teledeclared_property(self):
        self.assertFalse(self.diagnostic_not_filled_draft.is_teledeclared)
        self.assertFalse(self.diagnostic_filled_draft.is_teledeclared)
        self.assertTrue(self.diagnostic_filled_submitted.is_teledeclared)


class DiagnosticModelTeledeclareMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe,
            sector_list=[Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL],
        )
        cls.diagnostic_groupe = DiagnosticFactory(
            canteen=cls.canteen_groupe,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=0,
        )
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        cls.diagnostic_site = DiagnosticFactory(
            canteen=cls.canteen_site,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            valeur_totale=1000,
        )

    @freeze_time(date_in_last_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_outside_of_campaign(self):
        self.assertRaises(ValidationError, self.diagnostic_groupe.teledeclare, applicant=self.user)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_already_teledeclared(self):
        # teledeclare once
        self.diagnostic_site.teledeclare(applicant=self.user)
        # try to teledeclare again
        self.assertRaises(ValidationError, self.diagnostic_site.teledeclare, applicant=UserFactory())

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_not_filled(self):
        self.assertEqual(self.diagnostic_groupe.valeur_totale, 0)
        self.assertRaises(ValidationError, self.diagnostic_groupe.teledeclare, applicant=self.user)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_if_canteen_missing_data(self):
        self.canteen_site.yearly_meal_count = None  # missing data
        self.canteen_site.save(skip_validations=True)
        self.canteen_site.refresh_from_db()
        self.assertRaises(ValidationError, self.diagnostic_site.teledeclare, applicant=self.user)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_if_canteen_groupe_without_satellites(self):
        self.canteen_satellite.groupe = None  # remove from groupe
        self.canteen_satellite.save()
        self.canteen_groupe.refresh_from_db()
        self.assertEqual(self.canteen_groupe.satellites.count(), 0)
        self.assertRaises(ValidationError, self.diagnostic_groupe.teledeclare, applicant=self.user)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_if_canteen_groupe_has_satellite_missing_data(self):
        self.canteen_satellite.yearly_meal_count = None  # missing data
        self.canteen_satellite.save(skip_validations=True)
        self.canteen_satellite.refresh_from_db()
        # fill the diagnostic
        self.diagnostic_groupe.valeur_totale = 1000
        self.diagnostic_groupe.valeur_bio = 200
        self.diagnostic_groupe.valeur_siqo = 100
        self.diagnostic_groupe.valeur_externalites_performance = 100
        self.diagnostic_groupe.valeur_egalim_autres = 100
        self.diagnostic_groupe.save()
        self.assertRaises(ValidationError, self.diagnostic_groupe.teledeclare, applicant=self.user)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_groupe_can_teledeclare(self):
        self.assertIsNone(self.diagnostic_groupe.applicant)
        self.assertIsNone(self.diagnostic_groupe.canteen_snapshot)
        self.assertIsNone(self.diagnostic_groupe.satellites_snapshot)
        self.assertIsNone(self.diagnostic_groupe.applicant_snapshot)
        self.assertEqual(self.diagnostic_groupe.status, Diagnostic.DiagnosticStatus.DRAFT)
        self.assertIsNone(self.diagnostic_groupe.teledeclaration_date)
        self.assertIsNone(self.diagnostic_groupe.teledeclaration_mode)
        self.assertIsNone(self.diagnostic_groupe.teledeclaration_version)
        self.assertIsNone(self.diagnostic_groupe.teledeclaration_id)
        # fill the diagnostic
        self.diagnostic_groupe.valeur_totale = 1000
        self.diagnostic_groupe.valeur_bio = 200
        self.diagnostic_groupe.valeur_siqo = 100
        self.diagnostic_groupe.valeur_externalites_performance = 100
        self.diagnostic_groupe.valeur_egalim_autres = 100
        self.diagnostic_groupe.save()
        # teledeclare
        self.diagnostic_groupe.teledeclare(applicant=self.user)
        self.assertEqual(self.diagnostic_groupe.applicant, self.user)
        self.assertIsNotNone(self.diagnostic_groupe.canteen_snapshot)
        self.assertEqual(self.diagnostic_groupe.valeur_bio_agg, 200)
        self.assertEqual(self.diagnostic_groupe.valeur_siqo_agg, 100)
        self.assertEqual(self.diagnostic_groupe.valeur_externalites_performance_agg, 100)
        self.assertEqual(self.diagnostic_groupe.valeur_egalim_autres_agg, 100)
        self.assertEqual(self.diagnostic_groupe.valeur_egalim_hors_bio_agg, 300)
        self.assertEqual(self.diagnostic_groupe.valeur_egalim_agg, 500)
        self.assertEqual(self.diagnostic_groupe.status, Diagnostic.DiagnosticStatus.SUBMITTED)
        self.assertIsNotNone(self.diagnostic_groupe.teledeclaration_date)
        self.assertEqual(self.diagnostic_groupe.teledeclaration_mode, Diagnostic.TeledeclarationMode.CENTRAL_ALL)
        self.assertEqual(self.diagnostic_groupe.teledeclaration_version, 16)
        self.assertEqual(self.diagnostic_groupe.teledeclaration_id, self.diagnostic_groupe.id)
        # for snapshots, see tests below
        # try to teledeclare again
        self.assertRaises(ValidationError, self.diagnostic_groupe.teledeclare, applicant=UserFactory())

    @freeze_time(date_in_teledeclaration_campaign)
    def test_satellite_in_group_can_teledeclare_non_appro_fields_if_groupe_mode_appro(self):
        # change diagnostic_groupe mode to APPRO
        self.diagnostic_groupe.central_kitchen_diagnostic_mode = Diagnostic.CentralKitchenDiagnosticMode.APPRO
        self.diagnostic_groupe.save()
        diagnostic_satellite = DiagnosticFactory(
            canteen=self.canteen_satellite,
            year=year_data,
            diagnostic_type=None,  # Groupe appro teledeclaration
            has_waste_diagnostic=True,
            has_waste_plan=False,
        )
        # teledeclare
        diagnostic_satellite.teledeclare(applicant=self.user)


class DiagnosticModelCancelMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe,
        )
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen_groupe,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
        )

    @freeze_time(date_in_last_teledeclaration_campaign)
    def test_cannot_cancel_a_diagnostic_outside_of_campaign(self):
        self.assertRaises(ValidationError, self.diagnostic.cancel)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_cancel_a_diagnostic_not_teledeclared(self):
        self.assertRaises(ValidationError, self.diagnostic.cancel)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cancel(self):
        # teledeclare the diagnostic
        self.diagnostic.teledeclare(applicant=UserFactory())
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.SUBMITTED)
        self.assertIsNotNone(self.diagnostic.applicant)
        self.assertIsNotNone(self.diagnostic.teledeclaration_date)
        self.assertIsNotNone(self.diagnostic.teledeclaration_mode)
        self.assertIsNotNone(self.diagnostic.teledeclaration_version)
        self.assertIsNotNone(self.diagnostic.teledeclaration_id)

        # cancel
        self.diagnostic.cancel()

        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.DRAFT)
        self.assertIsNone(self.diagnostic.applicant)
        self.assertIsNone(self.diagnostic.teledeclaration_date)
        self.assertIsNone(self.diagnostic.teledeclaration_mode)
        self.assertIsNone(self.diagnostic.teledeclaration_version)
        self.assertIsNone(self.diagnostic.teledeclaration_id)


class DiagnosticTeledeclaredSnapshotsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        # groupe + satellite
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe,
        )
        cls.diagnostic_groupe = DiagnosticFactory(
            canteen=cls.canteen_groupe,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
        )
        # site
        cls.canteen_site = CanteenFactory(
            siret="21640122400011",
            production_type=Canteen.ProductionType.ON_SITE,
            sector_list=[Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL],
        )
        cls.diagnostic_site = DiagnosticFactory(
            canteen=cls.canteen_site,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
            valeur_bio=200,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_groupe.teledeclare(applicant=cls.user)
            cls.diagnostic_site.teledeclare(applicant=cls.user)

    def test_diagnostic_canteen_snapshot(self):
        # groupe
        self.assertIsNotNone(self.diagnostic_groupe.canteen_snapshot)
        self.assertEqual(self.diagnostic_groupe.canteen_snapshot["id"], self.canteen_groupe.id)
        self.assertEqual(self.diagnostic_groupe.canteen_snapshot["production_type"], Canteen.ProductionType.GROUPE)
        self.assertEqual(self.diagnostic_groupe.canteen_snapshot["sector_list"], [])
        self.assertEqual(self.diagnostic_groupe.canteen_snapshot_sector_lib_list, None)
        # site
        self.assertIsNotNone(self.diagnostic_site.canteen_snapshot)
        self.assertEqual(self.diagnostic_site.canteen_snapshot["id"], self.canteen_site.id)
        self.assertEqual(self.diagnostic_site.canteen_snapshot["production_type"], Canteen.ProductionType.ON_SITE)
        self.assertEqual(len(self.diagnostic_site.canteen_snapshot["sector_list"]), 2)
        self.assertEqual(self.diagnostic_site.canteen_snapshot["sector_list"][0], "education_primaire")
        self.assertEqual(
            self.diagnostic_site.canteen_snapshot_sector_lib_list,
            ["Ecole primaire (maternelle et élémentaire)", "Hôpitaux"],
        )

    def test_diagnostic_satellites_snapshot(self):
        # groupe
        self.assertIsNotNone(self.diagnostic_groupe.satellites_snapshot)
        self.assertEqual(len(self.diagnostic_groupe.satellites_snapshot), 1)
        self.assertEqual(self.diagnostic_groupe.satellites_snapshot[0]["id"], self.canteen_satellite.id)
        # site
        self.assertIsNone(self.diagnostic_site.satellites_snapshot)

    def test_diagnostic_applicant_snapshot(self):
        # groupe
        self.assertIsNotNone(self.diagnostic_groupe.applicant_snapshot)
        self.assertEqual(self.diagnostic_groupe.applicant_snapshot["id"], self.user.id)
        self.assertEqual(self.diagnostic_groupe.applicant_snapshot["email"], self.user.email)
        # site
        self.assertIsNotNone(self.diagnostic_site.applicant_snapshot)
        self.assertEqual(self.diagnostic_site.applicant_snapshot["id"], self.user.id)
        self.assertEqual(self.diagnostic_site.applicant_snapshot["email"], self.user.email)
