from freezegun import freeze_time

from django.test import TestCase
from data.models import Canteen, Diagnostic, Sector
from data.factories import CanteenFactory, DiagnosticFactory, PurchaseFactory


class CanteenActionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe_1_with_satellites = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_2_without_satellites = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_11 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_1_with_satellites,
        )
        cls.canteen_satellite_12 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_1_with_satellites,
        )
        cls.canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )
        cls.canteen_site = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
        )

    @freeze_time("2025-08-30")  # after the 2024 campaign
    def test_canteen_missing_data_actions(self):
        # has diagnostic, but missing data (yearly_meal_count)
        DiagnosticFactory(canteen=self.canteen_site, year=2024, valeur_totale=100)
        self.canteen_site.yearly_meal_count = None
        self.canteen_site.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_site.id).action,
            Canteen.Actions.FILL_CANTEEN_DATA,
        )

        # has diagnostic, but still missing data (line_ministry)
        self.canteen_site.yearly_meal_count = 1000
        self.canteen_site.economic_model = Canteen.EconomicModel.PUBLIC
        self.canteen_site.sector_list = [Sector.ADMINISTRATION_ARMEE]
        self.canteen_site.line_ministry = None
        self.canteen_site.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_site.id).action,
            Canteen.Actions.FILL_CANTEEN_DATA,
        )

        # has diagnostic, but still missing data (sector)
        self.canteen_site.economic_model = Canteen.EconomicModel.PRIVATE
        self.canteen_site.sector_list = []
        self.canteen_site.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_site.id).action,
            Canteen.Actions.FILL_CANTEEN_DATA,
        )

        # has diagnostic, but still missing data (too many sectors)
        self.canteen_site.sector_list = [
            Sector.SANTE_HOPITAL,
            Sector.EDUCATION_PRIMAIRE,
            Sector.ENTERPRISE_ENTREPRISE,
            Sector.ADMINISTRATION_ARMEE,
        ]
        self.canteen_site.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_site.id).action,
            Canteen.Actions.FILL_CANTEEN_DATA,
        )

        # has diagnostic, but still missing data (line_ministry)
        self.canteen_site.sector_list = [Sector.ADMINISTRATION_PRISON]
        self.canteen_site.economic_model = Canteen.EconomicModel.PUBLIC
        self.canteen_site.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_site.id).action,
            Canteen.Actions.FILL_CANTEEN_DATA,
        )

        # has diagnostic and data filled
        self.canteen_site.sector_list = [Sector.EDUCATION_PRIMAIRE]
        self.canteen_site.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_site.id).action,
            Canteen.Actions.DID_NOT_TELEDECLARE,
        )

    @freeze_time("2025-01-20")  # during the 2024 campaign
    def test_canteen_teledeclaration_actions(self):
        for canteen in [
            self.canteen_site,
            self.canteen_satellite,  # without groupe
        ]:
            # canteen without purchases nor diagnostic
            self.assertEqual(canteen.diagnostics.count(), 0)

            canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

            self.assertEqual(canteen_qs.get(id=canteen.id).action, Canteen.Actions.CREATE_DIAGNOSTIC)

            # canteen with purchases but without diagnostic
            PurchaseFactory(canteen=canteen, date="2024-01-01")

            canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

            self.assertEqual(canteen_qs.get(id=canteen.id).action, Canteen.Actions.PREFILL_DIAGNOSTIC)

            # canteen without purchases but with diagnostic (not filled)
            canteen.purchase_set.all().delete()
            canteen_diagnostic_2024 = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=None)

            canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

            self.assertEqual(canteen_qs.get(id=canteen.id).action, Canteen.Actions.FILL_DIAGNOSTIC)

            # canteen with diagnostic filled (2024)
            canteen_diagnostic_2024.valeur_totale = 100
            canteen_diagnostic_2024.save()

            canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

            self.assertEqual(canteen_qs.get(id=canteen.id).action, Canteen.Actions.TELEDECLARE)

            # canteen with diagnostic teledeclared
            canteen_diagnostic_2024.teledeclare(applicant=canteen.managers.first())

            canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

            self.assertEqual(canteen_qs.get(id=canteen.id).action, Canteen.Actions.NOTHING)

    @freeze_time("2025-01-20")  # during the 2024 campaign
    def test_groupe_missing_data_actions(self):
        # missing satellites, no diagnostic, canteen missing data
        self.assertEqual(self.canteen_groupe_2_without_satellites.satellites.count(), 0)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_2_without_satellites.id).action,
            Canteen.Actions.ADD_SATELLITES,
        )

        # add satellite, no diagnostic, canteen missing data
        self.canteen_satellite.groupe = self.canteen_groupe_2_without_satellites
        self.canteen_satellite.save(skip_validations=True)
        self.canteen_groupe_2_without_satellites.yearly_meal_count = None
        self.canteen_groupe_2_without_satellites.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_2_without_satellites.id).action,
            Canteen.Actions.CREATE_DIAGNOSTIC,
        )

        # has satellite, diagnostic started, canteen missing data
        canteen_groupe_diagnostic_2024 = DiagnosticFactory(
            canteen=self.canteen_groupe_2_without_satellites,
            year=2024,
            valeur_totale=None,
        )

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_2_without_satellites.id).action,
            Canteen.Actions.FILL_DIAGNOSTIC,
        )

        # has satellite, diagnostic started, canteen missing data
        canteen_groupe_diagnostic_2024.central_kitchen_diagnostic_mode = Diagnostic.CentralKitchenDiagnosticMode.ALL
        canteen_groupe_diagnostic_2024.save()

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_2_without_satellites.id).action,
            Canteen.Actions.FILL_DIAGNOSTIC,
        )

        # has satellite, diagnostic filled (2024), canteen missing data
        canteen_groupe_diagnostic_2024.valeur_totale = 100
        canteen_groupe_diagnostic_2024.save()

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_2_without_satellites.id).action,
            Canteen.Actions.FILL_CANTEEN_DATA,
        )

        # has satellite, diagnostic filled (2024), canteen data filled, new satellite missing data
        self.canteen_groupe_2_without_satellites.yearly_meal_count = 1000
        self.canteen_groupe_2_without_satellites.save(skip_validations=True)
        new_canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=self.canteen_groupe_2_without_satellites,
        )
        new_canteen_satellite.yearly_meal_count = None
        new_canteen_satellite.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_2_without_satellites.id).action,
            Canteen.Actions.FILL_SATELLITE_CANTEEN_DATA,
        )

        # has satellites filled, diagnostic filled (2024), canteen data filled
        new_canteen_satellite.yearly_meal_count = 1000
        new_canteen_satellite.save(skip_validations=True)

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_2_without_satellites.id).action,
            Canteen.Actions.TELEDECLARE,
        )

    @freeze_time("2025-01-20")  # during the 2024 campaign
    def test_groupe_satellite_relationship_diagnostic_mode_all_teledeclaration_actions(self):
        # groupe with satellites and has diagnostic started
        canteen_groupe_diagnostic_2024 = DiagnosticFactory(
            canteen=self.canteen_groupe_1_with_satellites,
            year=2024,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=None,
        )

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.FILL_DIAGNOSTIC,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.NOTHING_SATELLITE,
        )

        # group with appro mode ALL and satellite with missing data
        canteen_groupe_with_satellites_incorrect = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        canteen_satellite_incorrect = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=canteen_groupe_with_satellites_incorrect,
            # daily_meal_count=None,  # missing data
        )
        canteen_satellite_incorrect.yearly_meal_count = None
        canteen_satellite_incorrect.save(skip_validations=True)
        DiagnosticFactory(
            canteen=canteen_groupe_with_satellites_incorrect,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            year=2024,
        )

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=canteen_satellite_incorrect.id).action,
            Canteen.Actions.FILL_CANTEEN_DATA,
        )

        # groupe with satellites and has diagnostic filled
        canteen_groupe_diagnostic_2024.valeur_totale = 100
        canteen_groupe_diagnostic_2024.save()

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.TELEDECLARE,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.NOTHING_SATELLITE,
        )

        # groupe with satellites and has diagnostic teledeclared
        canteen_groupe_diagnostic_2024.teledeclare(applicant=self.canteen_groupe_1_with_satellites.managers.first())

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.NOTHING,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.NOTHING_SATELLITE_TELEDECLARED,
        )

    @freeze_time("2025-01-20")  # during the 2024 campaign
    def test_groupe_satellite_relationship_diagnostic_mode_appro_teledeclaration_actions(self):
        # groupe with satellites and has diagnostic started
        canteen_groupe_diagnostic_2024 = DiagnosticFactory(
            canteen=self.canteen_groupe_1_with_satellites,
            year=2024,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            valeur_totale=None,
        )

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.FILL_DIAGNOSTIC,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.FILL_DIAGNOSTIC,
        )

        # groupe with satellites and has diagnostic filled
        canteen_groupe_diagnostic_2024.valeur_totale = 100
        canteen_groupe_diagnostic_2024.save()

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.TELEDECLARE,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.TELEDECLARE,  # TODO: should be FILL_DIAGNOSTIC
        )

        # groupe with satellites and has diagnostic teledeclared
        canteen_groupe_diagnostic_2024.teledeclare(applicant=self.canteen_groupe_1_with_satellites.managers.first())

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.NOTHING,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.NOTHING,  # TODO: should be FILL_DIAGNOSTIC
        )

    @freeze_time("2025-01-20")  # during the 2024 campaign
    def test_groupe_satellite_relationship_diagnostic_mode_empty_teledeclaration_actions(self):
        # groupe with satellites, but no diagnostic
        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.CREATE_DIAGNOSTIC,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.CREATE_DIAGNOSTIC,
        )

        # groupe with satellites and satellite has diagnostic started
        canteen_satellite_11_diagnostic_2024 = DiagnosticFactory(
            canteen=self.canteen_satellite_11, year=2024, valeur_totale=None
        )

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.CREATE_DIAGNOSTIC,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.FILL_DIAGNOSTIC,
        )

        # groupe with satellites and satellite has diagnostic filled
        canteen_satellite_11_diagnostic_2024.valeur_totale = 100
        canteen_satellite_11_diagnostic_2024.save()

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.CREATE_DIAGNOSTIC,
        )
        self.assertEqual(
            canteen_qs.get(id=self.canteen_satellite_11.id).action,
            Canteen.Actions.TELEDECLARE,
        )

        # groupe with satellites and satellite has diagnostic teledeclared
        canteen_satellite_11_diagnostic_2024.teledeclare(
            applicant=self.canteen_groupe_1_with_satellites.managers.first()
        )

        canteen_qs = Canteen.objects.annotate_with_action_for_year(2024)

        self.assertEqual(
            canteen_qs.get(id=self.canteen_groupe_1_with_satellites.id).action,
            Canteen.Actions.CREATE_DIAGNOSTIC,
        )
        self.assertEqual(canteen_qs.get(id=self.canteen_satellite_11.id).action, Canteen.Actions.NOTHING)

    # TODO: test before campaign
    # TODO: test during correction campaign
    # TODO: test after campaign
