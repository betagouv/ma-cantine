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

    def test_diversification_badge_v2(self):
        hospital = {"sector_list": [Sector.SANTE_HOPITAL], "daily_meal_count": 12}
        primaire = {"sector_list": [Sector.EDUCATION_PRIMAIRE], "daily_meal_count": 12}
        college = {"sector_list": [Sector.EDUCATION_SECONDAIRE_COLLEGE], "daily_meal_count": 12}
        lycee = {"sector_list": [Sector.EDUCATION_SECONDAIRE_LYCEE], "daily_meal_count": 12}
        agricole = {"sector_list": [Sector.EDUCATION_ENSEIGNEMENT_AGRICOLE], "daily_meal_count": 12}
        universite = {"sector_list": [Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE], "daily_meal_count": 12}
        administration = {"sector_list": [Sector.ADMINISTRATION_ADMINISTRATIF], "daily_meal_count": 12}
        actions = [Diagnostic.PlanDiversificationActions.PLATS_PRODUITS]
        default_fields = {
            "plan_diversification_en_place": False,
            "plan_diversification_actions": [],
            "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.JAMAIS,
            "service_type": Diagnostic.ServiceType.MENU_UNIQUE,
            "tunnel_diversification": "complet",
        }
        cases = [
            # no obligation
            ("no obligation, nothing", hospital, default_fields, False),
            (
                "no obligation, nothing, tunnel not visited",
                hospital,
                {**default_fields, "tunnel_diversification": None},
                None,
            ),
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

    def test_plastic_badge_v2(self):
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
            "tunnel_plastic": "complet",
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
            (
                "not reached, tunnel not visited",
                entreprise,
                {**default_fields, "plastique_bouteille_boisson_remplace": False, "tunnel_plastic": None},
                None,
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

    def test_info_badge_v2(self):
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
            "tunnel_info": "complet",
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
            (
                "not reached, tunnel not visited",
                entreprise,
                {**default_fields, "information_part_egalim": False, "tunnel_info": None},
                None,
            ),
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
