from django.test import TestCase

from api.serializers import CanteenTeledeclarationSerializer
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic, Sector
from data.models import diagnostic_teledeclaration_badges
from data.models.diagnostic_teledeclaration_badges import get_teledeclaration_badges_config
from data.models.diagnostic_teledeclaration_fields import TELEDECLARATION_YEARS, get_teledeclaration_fields_all

TELEDECLARED = {"status": Diagnostic.DiagnosticStatus.SUBMITTED}


def empty_volet(year, volet):
    return {field: None for field in get_teledeclaration_fields_all(year, volet)}


class DiagnosticBadgesTest(TestCase):
    def assertBadge(self, badge, year, cases):
        """
        cases: list of (description, canteen kwargs, diagnostic kwargs, expected badge value)
        """
        for description, canteen_kwargs, diagnostic_kwargs, expected in cases:
            with self.subTest(year=year, case=description):
                canteen = CanteenFactory(**canteen_kwargs)
                if diagnostic_kwargs.get("status") == Diagnostic.DiagnosticStatus.SUBMITTED:
                    # same snapshot as Diagnostic.teledeclare()
                    diagnostic_kwargs = {
                        **diagnostic_kwargs,
                        "canteen_snapshot": CanteenTeledeclarationSerializer(canteen).data,
                    }
                diagnostic = DiagnosticFactory(canteen=canteen, year=year, **diagnostic_kwargs)
                self.assertIs(getattr(diagnostic, badge), expected)

    def test_badges_config_functions_exist(self):
        for year in TELEDECLARATION_YEARS:
            for volet, function_name in get_teledeclaration_badges_config(year).items():
                with self.subTest(year=year, volet=volet):
                    self.assertTrue(callable(getattr(diagnostic_teledeclaration_badges, function_name, None)))

    def test_badges_2021_not_available(self):
        diagnostic = DiagnosticFactory(year=2021, **TELEDECLARED)
        for badge in ["waste_badge", "diversification_badge", "plastic_badge", "info_badge"]:
            with self.subTest(badge=badge):
                self.assertIsNone(getattr(diagnostic, badge))

    def test_waste_badge_2022(self):
        reached = {
            "diagnostic_gaspillage_realise": True,
            "actions_gaspillage_realisees": [Diagnostic.ActionsGaspillage.INSCRIPTION],
            "dons_convention": True,
            "tunnel_waste": "complet",
            **TELEDECLARED,
        }
        cases = [
            ("all the objectives", {}, reached, True),
            (
                "no donation, < 3000 meals",
                {"daily_meal_count": 2999, "yearly_meal_count": 1000000},
                {**reached, "dons_convention": False},
                True,
            ),
            (
                "no donation, 3000 meals",
                {"daily_meal_count": 3000, "yearly_meal_count": 1000000},
                {**reached, "dons_convention": False},
                False,
            ),
            ("no diagnostic", {}, {**reached, "diagnostic_gaspillage_realise": False}, False),
            ("no action", {}, {**reached, "actions_gaspillage_realisees": []}, False),
            (
                "not reached, tunnel not visited",
                {},
                {**reached, "diagnostic_gaspillage_realise": False, "tunnel_waste": None},
                None,
            ),
        ]
        self.assertBadge("waste_badge", 2022, cases)
        self.assertBadge("waste_badge", 2023, cases)
        self.assertBadge("waste_badge", 2024, cases)
        self.assertBadge("waste_badge", 2025, cases)

    def test_waste_badge_2026(self):
        reached = {
            "diagnostic_gaspillage_realise": True,
            "actions_gaspillage_realisees": [Diagnostic.ActionsGaspillage.INSCRIPTION],
            "dons_convention": True,
            **TELEDECLARED,
        }
        cases = [
            ("all the objectives", {}, reached, True),
            (
                "no donation, < 3000 meals",
                {"daily_meal_count": 2999, "yearly_meal_count": 1000000},
                {**reached, "dons_convention": False},
                True,
            ),
            (
                "no donation, 3000 meals",
                {"daily_meal_count": 3000, "yearly_meal_count": 1000000},
                {**reached, "dons_convention": False},
                False,
            ),
            ("no diagnostic", {}, {**reached, "diagnostic_gaspillage_realise": False}, False),
            ("no action", {}, {**reached, "actions_gaspillage_realisees": []}, False),
        ]
        self.assertBadge("waste_badge", 2026, cases)

    def test_diversification_badge_2022(self):
        not_administration = {"sector_list": [Sector.SANTE_HOPITAL], "daily_meal_count": 12}
        administration = {
            "sector_list": [Sector.ADMINISTRATION_ADMINISTRATIF],
            "economic_model": Canteen.EconomicModel.PUBLIC,
            "line_ministry": Canteen.Ministries.ECONOMIE,
            "daily_meal_count": 12,
        }
        visited = {"plan_diversification_en_place": False, "tunnel_diversification": "complet", **TELEDECLARED}
        frequence = Diagnostic.MenuVegetarienFrequence
        cases = [
            (
                "not administration, weekly",
                not_administration,
                {**visited, "menu_vegetarien_frequence": frequence.HEBDO},
                True,
            ),
            (
                "not administration, less than weekly",
                not_administration,
                {**visited, "menu_vegetarien_frequence": frequence.MOINS_HEBDO},
                False,
            ),
            (
                "administration, daily",
                administration,
                {**visited, "menu_vegetarien_frequence": frequence.QUOTIDIEN},
                True,
            ),
            (
                "administration, weekly",
                administration,
                {**visited, "menu_vegetarien_frequence": frequence.HEBDO},
                False,
            ),
            (
                "administration sector but private, weekly",
                {**administration, "economic_model": Canteen.EconomicModel.PRIVATE, "line_ministry": None},
                {**visited, "menu_vegetarien_frequence": frequence.HEBDO},
                True,
            ),
            (
                "administration sector but no line ministry, weekly",
                {**administration, "line_ministry": None, "skip_validations": True},  # invalid canteen (old data)
                {**visited, "menu_vegetarien_frequence": frequence.HEBDO},
                True,
            ),
            (
                "200 meals with a plan",
                {**not_administration, "daily_meal_count": 200},
                {**visited, "plan_diversification_en_place": True, "menu_vegetarien_frequence": frequence.JAMAIS},
                True,
            ),
            (
                "199 meals with a plan",
                {**not_administration, "daily_meal_count": 199},
                {**visited, "plan_diversification_en_place": True, "menu_vegetarien_frequence": frequence.JAMAIS},
                False,
            ),
            (
                "not reached, tunnel not visited",
                not_administration,
                {**visited, "menu_vegetarien_frequence": frequence.JAMAIS, "tunnel_diversification": None},
                None,
            ),
        ]
        self.assertBadge("diversification_badge", 2022, cases)
        self.assertBadge("diversification_badge", 2023, cases)
        self.assertBadge("diversification_badge", 2024, cases)
        self.assertBadge("diversification_badge", 2025, cases)

    def test_diversification_badge_2026(self):
        hospital = {"sector_list": [Sector.SANTE_HOPITAL], "daily_meal_count": 12}
        primaire = {"sector_list": [Sector.EDUCATION_PRIMAIRE], "daily_meal_count": 12}
        college = {"sector_list": [Sector.EDUCATION_SECONDAIRE_COLLEGE], "daily_meal_count": 12}
        lycee = {"sector_list": [Sector.EDUCATION_SECONDAIRE_LYCEE], "daily_meal_count": 12}
        agricole = {"sector_list": [Sector.EDUCATION_ENSEIGNEMENT_AGRICOLE], "daily_meal_count": 12}
        universite = {"sector_list": [Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE], "daily_meal_count": 12}
        administration = {
            "sector_list": [Sector.ADMINISTRATION_ADMINISTRATIF],
            "economic_model": Canteen.EconomicModel.PUBLIC,
            "line_ministry": Canteen.Ministries.ECONOMIE,
            "daily_meal_count": 12,
        }
        actions = [Diagnostic.PlanDiversificationActions.PLATS_PRODUITS]
        default_fields = {
            "plan_diversification_en_place": False,
            "plan_diversification_actions": [],
            "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.JAMAIS,
            "service_type": Diagnostic.ServiceType.MENU_UNIQUE,
            **TELEDECLARED,
        }
        cases = [
            # no obligation
            ("no obligation, nothing", hospital, default_fields, False),
            (
                "no obligation, plan with actions",
                hospital,
                {**default_fields, "plan_diversification_en_place": True, "plan_diversification_actions": actions},
                True,
            ),
            (
                "no obligation, plan without action",
                hospital,
                {**default_fields, "plan_diversification_en_place": True},
                False,
            ),
            (
                "no obligation, less than weekly",
                hospital,
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.MOINS_HEBDO},
                True,
            ),
            ("not a school sector, nothing", universite, default_fields, False),
            ("199 meals, nothing", {**hospital, "daily_meal_count": 199}, default_fields, False),
            # diversification plan
            (
                "200 meals with a plan",
                {**hospital, "daily_meal_count": 200},
                {**default_fields, "plan_diversification_en_place": True},
                True,
            ),
            ("200 meals without a plan", {**hospital, "daily_meal_count": 200}, default_fields, False),
            # weekly vegetarian menu
            (
                "primaire, weekly",
                primaire,
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO},
                True,
            ),
            (
                "collège, more than weekly",
                college,
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.PLUS_HEBDO},
                True,
            ),
            (
                "lycée, daily",
                lycee,
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.QUOTIDIEN},
                True,
            ),
            (
                "primaire, less than weekly",
                primaire,
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.MOINS_HEBDO},
                False,
            ),
            ("lycée, never", lycee, default_fields, False),
            (
                "enseignement agricole, weekly",
                agricole,
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO},
                True,
            ),
            ("enseignement agricole, never", agricole, default_fields, False),
            # daily vegetarian option
            (
                "administration, libre-service, daily",
                administration,
                {
                    **default_fields,
                    "service_type": Diagnostic.ServiceType.CHOIX_MULTIPLE_LIBRE_SERVICE,
                    "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.QUOTIDIEN,
                },
                True,
            ),
            (
                "administration, réservation, weekly",
                administration,
                {
                    **default_fields,
                    "service_type": Diagnostic.ServiceType.CHOIX_MULTIPLE_RESERVATION,
                    "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO,
                },
                False,
            ),
            (
                "administration sector but private, réservation, weekly",
                {**administration, "economic_model": Canteen.EconomicModel.PRIVATE, "line_ministry": None},
                {
                    **default_fields,
                    "service_type": Diagnostic.ServiceType.CHOIX_MULTIPLE_RESERVATION,
                    "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO,
                },
                True,
            ),
            (
                "administration sector but no line ministry, réservation, weekly",
                {**administration, "line_ministry": None, "skip_validations": True},  # invalid canteen (old data)
                {
                    **default_fields,
                    "service_type": Diagnostic.ServiceType.CHOIX_MULTIPLE_RESERVATION,
                    "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO,
                },
                True,
            ),
            (
                "administration, menu unique, weekly",
                administration,
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO},
                True,
            ),
            # several obligations
            (
                "lycée 250 meals, plan and weekly",
                {**lycee, "daily_meal_count": 250},
                {
                    **default_fields,
                    "plan_diversification_en_place": True,
                    "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO,
                },
                True,
            ),
            (
                "lycée 250 meals, plan but less than weekly",
                {**lycee, "daily_meal_count": 250},
                {
                    **default_fields,
                    "plan_diversification_en_place": True,
                    "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.MOINS_HEBDO,
                },
                False,
            ),
            (
                "lycée 250 meals, weekly but no plan",
                {**lycee, "daily_meal_count": 250},
                {**default_fields, "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO},
                False,
            ),
        ]
        self.assertBadge("diversification_badge", 2026, cases)

    def test_plastic_badge_2022(self):
        reached = {
            "plastique_contenant_cuisson_remplace": True,
            "plastique_contenant_service_remplace": True,
            "plastique_bouteille_remplace": True,
            "plastique_ustensile_remplace": True,
            "tunnel_plastic": "complet",
        }
        cases = [
            ("all the plastics replaced", {}, reached, True),
            ("cuisson not replaced", {}, {**reached, "plastique_contenant_cuisson_remplace": False}, False),
            ("service not replaced", {}, {**reached, "plastique_contenant_service_remplace": False}, False),
            ("bouteille not replaced", {}, {**reached, "plastique_bouteille_remplace": False}, False),
            ("ustensile not replaced", {}, {**reached, "plastique_ustensile_remplace": False}, False),
            (
                "not reached, tunnel not visited",
                {},
                {**reached, "plastique_bouteille_remplace": False, "tunnel_plastic": None},
                None,
            ),
        ]
        self.assertBadge("plastic_badge", 2022, cases)
        self.assertBadge("plastic_badge", 2023, cases)
        self.assertBadge("plastic_badge", 2024, cases)
        self.assertBadge("plastic_badge", 2025, cases)

    def test_plastic_badge_2026(self):
        entreprise = {"sector_list": [Sector.ENTERPRISE_ENTREPRISE], "daily_meal_count": 12}
        primaire = {"sector_list": [Sector.EDUCATION_PRIMAIRE], "daily_meal_count": 12}
        creche = {"sector_list": [Sector.SOCIAL_CRECHE], "daily_meal_count": 12}
        ehpad = {"sector_list": [Sector.SOCIAL_EHPAD], "daily_meal_count": 12}
        hospital = {"sector_list": [Sector.SANTE_HOPITAL], "daily_meal_count": 12}
        default_fields = {
            "plastique_bouteille_boisson_remplace": True,
            "plastique_bouteille_remplace": False,
            "plastique_vaisselle_jetable_remplace": False,
            "plastique_contenant_remplace": False,
            "plastique_ustensile_remplace": True,
            "plastique_contenant_emporter_remplace": True,
            **TELEDECLARED,
        }
        all_remplace = {
            **default_fields,
            "plastique_bouteille_remplace": True,
            "plastique_vaisselle_jetable_remplace": True,
            "plastique_contenant_remplace": True,
        }
        cases = [
            # for all the canteens
            ("all, bouteille boisson replaced", entreprise, default_fields, True),
            (
                "all, bouteille boisson not replaced",
                entreprise,
                {**default_fields, "plastique_bouteille_boisson_remplace": False},
                False,
            ),
            ("social (not crèche), nothing else needed", ehpad, default_fields, True),
            # vaisselle jetable: 20 daily meals or more
            (
                "19 meals, vaisselle not replaced",
                {**entreprise, "daily_meal_count": 19},
                default_fields,
                True,
            ),
            (
                "20 meals, vaisselle not replaced",
                {**entreprise, "daily_meal_count": 20},
                default_fields,
                False,
            ),
            (
                "20 meals, vaisselle replaced",
                {**entreprise, "daily_meal_count": 20},
                {**default_fields, "plastique_vaisselle_jetable_remplace": True},
                True,
            ),
            # education: bouteille & contenant
            ("education, all replaced", primaire, all_remplace, True),
            (
                "education, bouteille not replaced",
                primaire,
                {**all_remplace, "plastique_bouteille_remplace": False},
                False,
            ),
            (
                "education, contenant not replaced",
                primaire,
                {**all_remplace, "plastique_contenant_remplace": False},
                False,
            ),
            # crèche & health: contenant
            ("crèche, contenant replaced", creche, {**default_fields, "plastique_contenant_remplace": True}, True),
            ("crèche, contenant not replaced", creche, default_fields, False),
            ("health, contenant replaced", hospital, {**default_fields, "plastique_contenant_remplace": True}, True),
            ("health, contenant not replaced", hospital, default_fields, False),
        ]
        self.assertBadge("plastic_badge", 2026, cases)

    def test_info_badge_2022(self):
        cases = [
            ("informs on quality", {}, {"information_qualite_durable": True, "tunnel_info": "complet"}, True),
            ("does not inform", {}, {"information_qualite_durable": False, "tunnel_info": "complet"}, False),
            (
                "not reached, tunnel not visited",
                {},
                {"information_qualite_durable": False, "tunnel_info": None},
                None,
            ),
        ]
        self.assertBadge("info_badge", 2022, cases)
        self.assertBadge("info_badge", 2023, cases)
        self.assertBadge("info_badge", 2024, cases)
        self.assertBadge("info_badge", 2025, cases)

    def test_info_badge_2026(self):
        hospital = {"sector_list": [Sector.SANTE_HOPITAL]}
        primaire = {"sector_list": [Sector.EDUCATION_PRIMAIRE]}
        creche = {"sector_list": [Sector.SOCIAL_CRECHE]}
        prison = {"sector_list": [Sector.ADMINISTRATION_PRISON]}
        administratif = {"sector_list": [Sector.ADMINISTRATION_ADMINISTRATIF]}
        entreprise = {"sector_list": [Sector.ENTERPRISE_ENTREPRISE]}
        default_fields = {
            "information_part_egalim": True,
            "information_affichage_permanent": True,
            "information_electronique_annuelle": True,
            "information_consultation_qualite": False,
            "information_part_pat": True,
            **TELEDECLARED,
        }
        cases = [
            # for all the canteens
            ("all, everything", entreprise, default_fields, True),
            ("all, no part EGalim", entreprise, {**default_fields, "information_part_egalim": False}, False),
            ("all, no affichage", entreprise, {**default_fields, "information_affichage_permanent": False}, False),
            (
                "all, no communication électronique",
                entreprise,
                {**default_fields, "information_electronique_annuelle": False},
                False,
            ),
            ("administratif, no consultation needed", administratif, default_fields, True),
            # consultation on the food quality
            ("education, consultation", primaire, {**default_fields, "information_consultation_qualite": True}, True),
            ("education, no consultation", primaire, default_fields, False),
            ("health, consultation", hospital, {**default_fields, "information_consultation_qualite": True}, True),
            ("health, no consultation", hospital, default_fields, False),
            ("social, consultation", creche, {**default_fields, "information_consultation_qualite": True}, True),
            ("social, no consultation", creche, default_fields, False),
            ("prison, consultation", prison, {**default_fields, "information_consultation_qualite": True}, True),
            ("prison, no consultation", prison, default_fields, False),
            (
                "education, consultation but no part EGalim",
                primaire,
                {**default_fields, "information_consultation_qualite": True, "information_part_egalim": False},
                False,
            ),
        ]
        self.assertBadge("info_badge", 2026, cases)

    def test_badges_2022_need_a_teledeclared_diagnostic(self):
        """
        The 2022 badges using the canteen_snapshot (waste & diversification) are None if not teledeclared
        """
        waste_reached = {
            "diagnostic_gaspillage_realise": True,
            "actions_gaspillage_realisees": [Diagnostic.ActionsGaspillage.INSCRIPTION],
            "dons_convention": True,
            "tunnel_waste": "complet",
        }
        diversification_reached = {
            "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.HEBDO,
            "tunnel_diversification": "complet",
        }
        not_administration = {"sector_list": [Sector.SANTE_HOPITAL], "daily_meal_count": 12}
        for year in [2022, 2023, 2024, 2025]:
            self.assertBadge(
                "waste_badge",
                year,
                [
                    ("teledeclared", {}, {**waste_reached, **TELEDECLARED}, True),
                    ("not teledeclared", {}, waste_reached, None),
                ],
            )
            self.assertBadge(
                "diversification_badge",
                year,
                [
                    ("teledeclared", not_administration, {**diversification_reached, **TELEDECLARED}, True),
                    ("not teledeclared", not_administration, diversification_reached, None),
                ],
            )

    def test_badges_2026_use_the_canteen_snapshot(self):
        """
        The 2026 badges use the canteen data at the time of the teledeclaration (canteen_snapshot),
        not the current canteen data
        """
        # sector_list: education requires the plastic water bottles to be replaced
        canteen = CanteenFactory(sector_list=[Sector.EDUCATION_PRIMAIRE], daily_meal_count=12)
        diagnostic = DiagnosticFactory(
            canteen=canteen,
            year=2026,
            canteen_snapshot=CanteenTeledeclarationSerializer(canteen).data,
            plastique_bouteille_boisson_remplace=True,
            plastique_bouteille_remplace=False,
            plastique_vaisselle_jetable_remplace=False,
            plastique_contenant_remplace=False,
            plastique_ustensile_remplace=True,
            plastique_contenant_emporter_remplace=True,
            **TELEDECLARED,
        )
        self.assertIs(diagnostic.plastic_badge, False)
        Canteen.objects.filter(pk=canteen.pk).update(sector_list=[Sector.ENTERPRISE_ENTREPRISE])
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.canteen.sector_list, [Sector.ENTERPRISE_ENTREPRISE])
        self.assertIs(diagnostic.plastic_badge, False)

        # daily_meal_count: 3000 or more requires a donation agreement
        canteen = CanteenFactory(daily_meal_count=3000, yearly_meal_count=1000000)
        diagnostic = DiagnosticFactory(
            canteen=canteen,
            year=2026,
            canteen_snapshot=CanteenTeledeclarationSerializer(canteen).data,
            diagnostic_gaspillage_realise=True,
            plan_gaspillage_en_place=True,
            actions_gaspillage_realisees=[Diagnostic.ActionsGaspillage.INSCRIPTION],
            dons_convention=False,
            **TELEDECLARED,
        )
        self.assertIs(diagnostic.waste_badge, False)
        Canteen.objects.filter(pk=canteen.pk).update(daily_meal_count=100)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.canteen.daily_meal_count, 100)
        self.assertIs(diagnostic.waste_badge, False)

    def test_badges_2026_need_a_teledeclared_filled_and_clean_volet(self):
        """
        The 2026 badges are None if the diagnostic is not teledeclared, or if the volet is empty or not clean
        (see is_volet_completed: same for all the volets, tested here with the gaspillage volet)
        """
        reached = {
            "diagnostic_gaspillage_realise": True,
            "plan_gaspillage_en_place": True,
            "actions_gaspillage_realisees": [Diagnostic.ActionsGaspillage.INSCRIPTION],
            "dons_convention": True,
        }
        cases = [
            ("teledeclared, filled and clean volet", {}, {**reached, **TELEDECLARED}, True),
            ("not teledeclared, filled and clean volet", {}, reached, None),
            ("not teledeclared, empty volet", {}, empty_volet(2026, "GASPILLAGE"), None),
            ("teledeclared, empty volet", {}, {**empty_volet(2026, "GASPILLAGE"), **TELEDECLARED}, None),
            (
                "teledeclared, volet not clean",
                {},
                {**reached, **TELEDECLARED, "dons_quantite": -1},  # must be positive
                None,
            ),
        ]
        self.assertBadge("waste_badge", 2026, cases)
