from django.utils import timezone

from data.models import Canteen, Sector
from data.factories import CanteenFactory, UserFactory


def setUpTestData(cls):
    # same test data for CanteenETLAnalysisTest & CanteenETLOpenDataTest
    cls.canteen_site_manager_1 = UserFactory(email="gestionnaire1@example.com")
    cls.canteen_site_manager_2 = UserFactory(email="gestionnaire2@example.com")
    cls.canteen_site = CanteenFactory(
        name="Cantine",
        siret="19382111300027",
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
    cls.canteen_site_created_earlier = CanteenFactory(
        production_type=Canteen.ProductionType.ON_SITE,
        # creation_date=timezone.now() - timezone.timedelta(days=10),
    )
    Canteen.objects.filter(id=cls.canteen_site_created_earlier.id).update(
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
    )
    cls.canteen_groupe = CanteenFactory(
        production_type=Canteen.ProductionType.GROUPE,
    )
    cls.canteen_satellite = CanteenFactory(
        production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        groupe=cls.canteen_groupe,
        central_producer_siret="22730656663081",
    )
