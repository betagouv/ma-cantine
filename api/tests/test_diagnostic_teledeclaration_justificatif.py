from datetime import timedelta

from django.core.management import call_command
from django.template.loader import get_template
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from api.views.diagnostic_teledeclaration import DiagnosticTeledeclarationPdfView
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic
from data.models.diagnostic_teledeclaration_dates import CAMPAIGN_DATES


class DiagnosticTeledeclarationJustificatifTest(APITestCase):
    """
    Tests that don't depend on the version of the template
    """

    @authenticate
    def test_uses_the_template_of_the_year(self):
        expected_templates = {
            2021: "justificatif_2021",
            2022: "justificatif_2021",
            2023: "justificatif_2023",
            2024: "justificatif_2023",
            2025: "justificatif_2023",
            2026: "justificatif_2023",
        }
        # a new campaign year must choose its template
        self.assertEqual(set(expected_templates), set(CAMPAIGN_DATES))
        all_templates = {f"teledeclaration_pdf/{name}/index.html" for name in expected_templates.values()}

        for year, template_name in expected_templates.items():
            with self.subTest(year=year):
                with freeze_time(CAMPAIGN_DATES[year]["teledeclaration_start_date"] + timedelta(days=1)):
                    canteen = CanteenFactory(managers=[authenticate.user])
                    diagnostic = DiagnosticFactory(
                        canteen=canteen, year=year, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
                    )
                    diagnostic.teledeclare(applicant=authenticate.user)

                    response = self.client.get(
                        reverse(
                            "diagnostic_teledeclaration_pdf",
                            kwargs={"canteen_pk": canteen.id, "pk": diagnostic.id},
                        )
                    )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                expected_template = f"teledeclaration_pdf/{template_name}/index.html"
                self.assertTemplateUsed(response, expected_template)
                for other_template in all_templates - {expected_template}:
                    self.assertTemplateNotUsed(response, other_template)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_generate_pdf_if_unauthenticated(self):
        user = UserFactory()
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(user)
        diagnostic.teledeclare(user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_cannot_generate_pdf_if_canteen_does_not_exist(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

        url = reverse("diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": 9999, "pk": diagnostic.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_cannot_generate_pdf_if_diagnostic_does_not_exist(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

        url = reverse("diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_cannot_generate_pdf_if_not_canteen_manager(self):
        user = UserFactory()
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(user)
        diagnostic.teledeclare(user)

        # teledeclared by user, but authenticate.user is not a manager
        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_can_generate_pdf(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        diagnostic.teledeclare(applicant=authenticate.user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_can_generate_pdf_central(self):
        canteen_central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user], skip_validations=True
        )
        diagnostic = DiagnosticFactory(
            canteen=canteen_central, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic.teledeclare(applicant=authenticate.user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2026-03-30")  # during the 2025 campaign
    @authenticate
    def test_can_generate_pdf_groupe_satellite(self):
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[authenticate.user])
        canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=canteen_groupe, managers=[authenticate.user]
        )
        diagnostic_satellite = DiagnosticFactory(
            canteen=canteen_satellite, year=2025, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic_satellite.teledeclare(applicant=authenticate.user)
        diagnostic_groupe = DiagnosticFactory(
            canteen=canteen_groupe, year=2025, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic_groupe.teledeclare(applicant=authenticate.user)

        call_command("diagnostic_fill_invalid_warning_reason_list", year=2025, apply=True)
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # groupe should be able to generate pdf
        url = reverse(
            "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": canteen_groupe.id, "pk": diagnostic_groupe.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # satellite should be able to generate pdf of initial diagnostic
        # (even if the diagnostic is not valid: DOUBLON_1TD1SITE)
        url = reverse(
            "diagnostic_teledeclaration_pdf",
            kwargs={"canteen_pk": canteen_satellite.id, "pk": diagnostic_satellite.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # satellite should be able to generate pdf of generated diagnostic
        diagnostic_satellite_generated = Diagnostic.all_objects.get(
            canteen=canteen_satellite, year=2025, generated_from_groupe_diagnostic=True
        )

        url = reverse(
            "diagnostic_teledeclaration_pdf",
            kwargs={"canteen_pk": canteen_satellite.id, "pk": diagnostic_satellite_generated.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DiagnosticTeledeclarationJustificatif2021Test(APITestCase):
    """
    Template used for the 2021 & 2022 campaigns
    """

    template_name = "teledeclaration_pdf/justificatif_2021/index.html"

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_can_generate_pdf_legacy_teledeclaration(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        diagnostic.teledeclare(applicant=authenticate.user)
        # simulate legacy diagnostic without type
        Diagnostic.objects.filter(id=diagnostic.id).update(
            diagnostic_type=None, canteen_snapshot={"name": ""}, applicant_snapshot={"name": ""}
        )

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2023-03-30")  # during the 2022 campaign
    def test_display_the_volet_answers(self):
        """
        The PDF templates read the diagnostic fields by name (diagnostic.__dict__ + overrides):
        a renamed field must be renamed in the templates (& overrides) too
        """
        user = UserFactory()
        canteen = CanteenFactory(daily_meal_count=200, managers=[user])
        diagnostic = DiagnosticFactory(
            canteen=canteen,
            year=2022,
            diagnostic_gaspillage_realise=True,
            actions_gaspillage_realisees=[Diagnostic.ActionsGaspillage.SENSIBILISATION],
            plan_diversification_en_place=True,
            plan_diversification_actions=[Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
            menu_vegetarien_frequence=Diagnostic.MenuVegetarienFrequence.QUOTIDIEN,
            menu_vegetarien_bases=[Diagnostic.MenuVegetarienBase.SOJA],
            information_qualite_nutritionnelle=True,
            information_qualite_durable=True,
            information_supports=[Diagnostic.InformationSupport.AFFICHAGE],
            information_supports_autre="Journal de l'école",
            information_frequence=Diagnostic.InformationFrequence.ANNUELLE,
            information_support_url="https://example.com/menus",
            plastique_contenant_cuisson_remplace=True,
            plastique_contenant_service_remplace=True,
            plastique_bouteille_remplace=False,
            plastique_ustensile_remplace=False,
        )
        diagnostic.teledeclare(user)

        html = get_template(self.template_name).render(DiagnosticTeledeclarationPdfView.get_context(diagnostic))

        # gaspillage
        self.assertIn("Diagnostic sur le gaspillage réalisé", html)
        # diversification (only displayed if plan_diversification_en_place)
        self.assertIn(Diagnostic.PlanDiversificationActions.PLATS_PRODUITS.label, html)
        self.assertIn(Diagnostic.MenuVegetarienFrequence.QUOTIDIEN.label, html)
        self.assertIn(Diagnostic.MenuVegetarienBase.SOJA.label, html)
        # information
        self.assertIn("Communique sur le plan alimentaire", html)
        self.assertIn("Communique sur les démarches qualité/durables/équitables", html)
        self.assertNotIn("Ne communique pas", html)
        self.assertIn(Diagnostic.InformationSupport.AFFICHAGE.label, html)
        self.assertIn("Journal de l&#x27;école", html)
        self.assertIn(Diagnostic.InformationFrequence.ANNUELLE.label, html)
        self.assertIn("https://example.com/menus", html)
        # plastique
        self.assertIn("Contenants de cuisson en plastique remplacés", html)
        self.assertIn("Contenants de service en plastique remplacés", html)
        self.assertIn("Bouteilles en plastique non remplacées", html)


class DiagnosticTeledeclarationJustificatif2023Test(APITestCase):
    """
    Template used for the 2023, 2024 & 2025 campaigns
    """

    template_name = "teledeclaration_pdf/justificatif_2023/index.html"

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_display_the_volet_answers(self):
        """
        The PDF templates read the diagnostic fields by name (diagnostic.__dict__ + overrides):
        a renamed field must be renamed in the templates (& overrides) too
        """
        user = UserFactory()
        canteen = CanteenFactory(daily_meal_count=200, managers=[user])
        diagnostic = DiagnosticFactory(
            canteen=canteen,
            year=2024,
            diagnostic_gaspillage_realise=True,
            actions_gaspillage_realisees=[Diagnostic.ActionsGaspillage.SENSIBILISATION],
            plan_diversification_en_place=True,
            plan_diversification_actions=[Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
            menu_vegetarien_frequence=Diagnostic.MenuVegetarienFrequence.QUOTIDIEN,
            menu_vegetarien_bases=[Diagnostic.MenuVegetarienBase.SOJA],
            information_qualite_nutritionnelle=True,
            information_qualite_durable=True,
            information_supports=[Diagnostic.InformationSupport.AFFICHAGE],
            information_supports_autre="Journal de l'école",
            information_frequence=Diagnostic.InformationFrequence.ANNUELLE,
            information_support_url="https://example.com/menus",
            plastique_contenant_cuisson_remplace=True,
            plastique_contenant_service_remplace=True,
            plastique_bouteille_remplace=False,
            plastique_ustensile_remplace=False,
        )
        diagnostic.teledeclare(user)

        html = get_template(self.template_name).render(DiagnosticTeledeclarationPdfView.get_context(diagnostic))

        # gaspillage
        self.assertIn("Diagnostic sur le gaspillage réalisé", html)
        # diversification (only displayed if plan_diversification_en_place)
        self.assertIn(Diagnostic.PlanDiversificationActions.PLATS_PRODUITS.label, html)
        self.assertIn(Diagnostic.MenuVegetarienFrequence.QUOTIDIEN.label, html)
        self.assertIn(Diagnostic.MenuVegetarienBase.SOJA.label, html)
        # information
        self.assertIn("Communique sur le plan alimentaire", html)
        self.assertIn("Communique sur les démarches qualité/durables/équitables", html)
        self.assertNotIn("Ne communique pas", html)
        self.assertIn(Diagnostic.InformationSupport.AFFICHAGE.label, html)
        self.assertIn("Journal de l&#x27;école", html)
        self.assertIn(Diagnostic.InformationFrequence.ANNUELLE.label, html)
        self.assertIn("https://example.com/menus", html)
        # plastique
        self.assertIn("Contenants de cuisson en plastique remplacés", html)
        self.assertIn("Contenants de service en plastique remplacés", html)
        self.assertIn("Bouteilles en plastique non remplacées", html)
        # only in this version
        self.assertIn(Diagnostic.ActionsGaspillage.SENSIBILISATION.label, html)

    def test_measure_info_component_since_2026(self):
        template = get_template("teledeclaration_pdf/justificatif_2023/components/measure_info.html")
        context = {
            "information_affichage_permanent": True,
            "information_electronique_annuelle": False,
            "information_part_egalim": True,
            "information_part_pat": None,
            "information_consultation_qualite": True,
            # previous fields (ignored since 2026)
            "information_qualite_nutritionnelle": True,
        }

        html = template.render({"year": 2026, **context})
        for field_name in context:
            if field_name.startswith("information_qualite"):
                continue
            self.assertIn(Diagnostic._meta.get_field(field_name).verbose_name, html)
        self.assertNotIn("Communique sur le plan alimentaire", html)

        html = template.render({"year": 2025, **context})
        self.assertIn("Communique sur le plan alimentaire", html)
        self.assertNotIn("affichage permanent", html)

    def test_measure_plastic_component_since_2026(self):
        template = get_template("teledeclaration_pdf/justificatif_2023/components/measure_plastic.html")
        context = {
            "plastique_bouteille_boisson_remplace": True,
            "plastique_bouteille_remplace": None,
            "plastique_ustensile_remplace": True,
            "plastique_vaisselle_jetable_remplace": False,
            "plastique_contenant_remplace": True,
            "vente_emporter": True,
            "plastique_contenant_emporter_remplace": True,
            # removed in 2026
            "plastique_contenant_cuisson_remplace": True,
        }

        html = template.render({"year": 2026, **context})
        for field_name in [
            "plastique_bouteille_boisson_remplace",
            "plastique_vaisselle_jetable_remplace",
            "plastique_contenant_remplace",
            "plastique_contenant_emporter_remplace",
        ]:
            self.assertIn(Diagnostic._meta.get_field(field_name).verbose_name, html)
        self.assertIn("Aucune bouteilles d’eau plate en plastique", html)
        self.assertIn("Aucun ustensiles à usage unique en matière plastique", html)
        self.assertNotIn("Contenants de cuisson en plastique remplacés", html)

        html = template.render({"year": 2025, **context})
        self.assertIn("Contenants de cuisson en plastique remplacés", html)
        self.assertNotIn("fontaine d'eau potable", html)

    def test_measure_plastic_component_since_2026_without_vente_emporter(self):
        template = get_template("teledeclaration_pdf/justificatif_2023/components/measure_plastic.html")
        html = template.render({"year": 2026, "vente_emporter": False, "plastique_contenant_emporter_remplace": None})
        self.assertIn("L'établissement ne propose pas de repas à emporter", html)
        self.assertNotIn("repas à emporter : Inconnu", html)
