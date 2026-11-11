from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic, Sector


class DiagnosticBadgesTest(TestCase):
    def assertBadge(self, badge, year, cases):
        """
        cases: list of (description, canteen kwargs, diagnostic kwargs, expected badge value)
        """
        for description, canteen_kwargs, diagnostic_kwargs, expected in cases:
            with self.subTest(year=year, case=description):
                canteen = CanteenFactory(**canteen_kwargs)
                diagnostic = DiagnosticFactory(canteen=canteen, year=year, **diagnostic_kwargs)
                self.assertIs(getattr(diagnostic, badge), expected)

    def test_waste_badge_v1(self):
        reached = {
            "diagnostic_gaspillage_realise": True,
            "actions_gaspillage_realisees": [Diagnostic.ActionsGaspillage.INSCRIPTION],
            "dons_convention": True,
            "tunnel_waste": "complet",
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
        self.assertBadge("waste_badge", 2021, cases)
        self.assertBadge("waste_badge", 2022, cases)
        self.assertBadge("waste_badge", 2023, cases)
        self.assertBadge("waste_badge", 2024, cases)
        self.assertBadge("waste_badge", 2025, cases)
        self.assertBadge("waste_badge", 2026, cases)

    def test_diversification_badge_v1(self):
        not_administration = {"sector_list": [Sector.SANTE_HOPITAL], "daily_meal_count": 12}
        administration = {"sector_list": [Sector.ADMINISTRATION_ADMINISTRATIF], "daily_meal_count": 12}
        visited = {"plan_diversification_en_place": False, "tunnel_diversification": "complet"}
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
        self.assertBadge("diversification_badge", 2021, cases)
        self.assertBadge("diversification_badge", 2022, cases)
        self.assertBadge("diversification_badge", 2023, cases)
        self.assertBadge("diversification_badge", 2024, cases)
        self.assertBadge("diversification_badge", 2025, cases)

    def test_plastic_badge_v1(self):
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
        self.assertBadge("plastic_badge", 2021, cases)
        self.assertBadge("plastic_badge", 2022, cases)
        self.assertBadge("plastic_badge", 2023, cases)
        self.assertBadge("plastic_badge", 2024, cases)
        self.assertBadge("plastic_badge", 2025, cases)

    def test_info_badge_v1(self):
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
        self.assertBadge("info_badge", 2021, cases)
        self.assertBadge("info_badge", 2022, cases)
        self.assertBadge("info_badge", 2023, cases)
        self.assertBadge("info_badge", 2024, cases)
        self.assertBadge("info_badge", 2025, cases)
