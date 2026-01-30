from django.utils import timezone
from freezegun import freeze_time

from data.models import Canteen, Sector
from data.factories import CanteenFactory, UserFactory, DiagnosticFactory
from data.models.diagnostic import Diagnostic


def setUpTestData(cls, with_diagnostics=False):
    """
    Common test data for CanteenETLAnalysisTest & CanteenETLOpenDataTest
    """
    cls.canteen_site_manager_1 = UserFactory(email="gestionnaire1@example.com")
    cls.canteen_site_manager_2 = UserFactory(email="gestionnaire2@example.com")
    cls.canteen_groupe_manager = UserFactory()
    cls.canteen_site = CanteenFactory(
        name="Cantine",
        siret="21380185500015",
        city_insee_code="38185",
        epci="200040715",
        epci_lib="Grenoble-Alpes-Métropole",
        pat_list=["1294", "1295"],
        pat_lib_list=[
            "PAT du Département de l'Isère",
            "Projet Alimentaire inter Territorial de la Grande région grenobloise",
        ],
        department="38",
        department_lib="Isère",
        region="84",
        region_lib="Auvergne-Rhône-Alpes",
        management_type=Canteen.ManagementType.DIRECT,
        production_type=Canteen.ProductionType.ON_SITE,
        economic_model=Canteen.EconomicModel.PUBLIC,
        sector_list=[Sector.SANTE_HOPITAL, Sector.SOCIAL_CRECHE],
        declaration_donnees_2022=True,
        declaration_donnees_2023=False,
        declaration_donnees_2024=True,
        declaration_donnees_2025=False,
        managers=[cls.canteen_site_manager_1, cls.canteen_site_manager_2],
    )
    cls.canteen_site_without_manager = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[])
    cls.canteen_site_earlier = CanteenFactory(
        production_type=Canteen.ProductionType.ON_SITE,
        managers=[cls.canteen_site_manager_2],
        # creation_date=timezone.now() - timezone.timedelta(days=10),
    )
    Canteen.objects.filter(id=cls.canteen_site_earlier.id).update(
        creation_date=timezone.now() - timezone.timedelta(days=10)
    )
    cls.canteen_site_deleted = CanteenFactory(
        production_type=Canteen.ProductionType.ON_SITE,
        deletion_date=timezone.now(),
    )
    cls.canteen_site_armee = CanteenFactory(
        management_type=Canteen.ManagementType.DIRECT,
        production_type=Canteen.ProductionType.ON_SITE,
        economic_model=Canteen.EconomicModel.PUBLIC,
        sector_list=[Sector.ADMINISTRATION_PRISON],
        line_ministry=Canteen.Ministries.ARMEE,
        managers=[cls.canteen_site_manager_2],
    )
    cls.canteen_groupe = CanteenFactory(
        production_type=Canteen.ProductionType.GROUPE,
        managers=[cls.canteen_groupe_manager],
    )
    cls.canteen_satellite = CanteenFactory(
        production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        groupe=cls.canteen_groupe,
        central_producer_siret="22730656663081",
        city_insee_code="38185",
        epci="200040715",
        epci_lib="Grenoble-Alpes-Métropole",
        pat_list=["1294", "1295"],
        pat_lib_list=[
            "PAT du Département de l'Isère",
            "Projet Alimentaire inter Territorial de la Grande région grenobloise",
        ],
        department="38",
        department_lib="Isère",
        region="84",
        region_lib="Auvergne-Rhône-Alpes",
        sector_list=[Sector.EDUCATION_PRIMAIRE],
    )

    if with_diagnostics:
        with freeze_time("2023-05-14"):  # during the 2022 campaign
            cls.canteen_site_diagnostic_2022 = DiagnosticFactory(
                canteen=cls.canteen_site, year=2022, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
            )
        with freeze_time("2023-05-15"):  # during the 2022 campaign (1 day later)
            cls.canteen_site_earlier_diagnostic_2022 = DiagnosticFactory(
                canteen=cls.canteen_site_earlier, year=2022, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
            )
            cls.canteen_site_earlier_diagnostic_2022.teledeclare(cls.canteen_site_manager_2)
        with freeze_time("2023-05-16"):  # during the 2022 campaign (1 day later)
            cls.canteen_site_diagnostic_2022.teledeclare(cls.canteen_site_manager_1)
        with freeze_time("2023-05-17"):  # during the 2022 campaign (1 day later)
            cls.canteen_groupe_diagnostic_2022 = DiagnosticFactory(
                canteen=cls.canteen_groupe, year=2022, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
            )
            cls.canteen_groupe_diagnostic_2022.teledeclare(cls.canteen_groupe_manager)
        with freeze_time("2024-04-01"):  # during the 2023 campaign
            cls.canteen_site_diagnostic_2023 = DiagnosticFactory(
                canteen=cls.canteen_site, year=2023, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
            )
            cls.canteen_site_diagnostic_2023.teledeclare(cls.canteen_site_manager_1)
            cls.canteen_site_diagnostic_2023.cancel()  # will not appear in the exports
            cls.canteen_site_armee_diagnostic_2023 = DiagnosticFactory(
                canteen=cls.canteen_site_armee, year=2023, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
            )
            cls.canteen_site_armee_diagnostic_2023.teledeclare(cls.canteen_site_manager_2)
        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            cls.canteen_site_diagnostic_2024 = DiagnosticFactory(
                canteen=cls.canteen_site, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
            )
            cls.canteen_site_diagnostic_2024.teledeclare(cls.canteen_site_manager_1)
        with freeze_time("2026-01-30"):  # during the 2025 campaign
            cls.canteen_groupe_diagnostic_2025 = DiagnosticFactory(
                canteen=cls.canteen_groupe, year=2025, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
            )
            cls.canteen_groupe_diagnostic_2025.teledeclare(cls.canteen_groupe_manager)
