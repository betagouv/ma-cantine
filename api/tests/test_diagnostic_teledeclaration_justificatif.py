from datetime import timedelta
from decimal import Decimal
from html import unescape

from django.core.management import call_command
from django.template.loader import get_template
from django.urls import reverse
from django.utils.html import escape, strip_tags
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from api.views.diagnostic_teledeclaration import DiagnosticTeledeclarationPdfView
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic
from data.models.diagnostic_teledeclaration_dates import CAMPAIGN_DATES
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_verbose_name,
)


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
            2026: "justificatif_2026",
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

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_does_not_display_the_fields_created_in_2026(self):
        fields_created_in_2026 = [
            ("PLASTIQUE", "plastique_bouteille_boisson_remplace"),
            ("PLASTIQUE", "plastique_vaisselle_jetable_remplace"),
            ("PLASTIQUE", "plastique_contenant_remplace"),
            ("PLASTIQUE", "vente_emporter"),
            ("PLASTIQUE", "plastique_contenant_emporter_remplace"),
            ("INFORMATION", "information_affichage_permanent"),
            ("INFORMATION", "information_electronique_annuelle"),
            ("INFORMATION", "information_part_egalim"),
            ("INFORMATION", "information_part_pat"),
            ("INFORMATION", "information_consultation_qualite"),
        ]
        user = UserFactory()
        canteen = CanteenFactory(managers=[user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024)
        diagnostic.teledeclare(user)
        # filled after teledeclare: these fields didn't exist in 2024
        for _, field_name in fields_created_in_2026:
            setattr(diagnostic, field_name, True)

        html = get_template(self.template_name).render(DiagnosticTeledeclarationPdfView.get_context(diagnostic))

        text = " ".join(unescape(strip_tags(html)).split())
        for volet, field_name in fields_created_in_2026:
            with self.subTest(field=field_name):
                self.assertNotIn(get_teledeclaration_verbose_name(2026, volet, field_name), text)


# 2026 volets with all their fields filled
VOLET_ANSWERS_2026 = {
    # gaspillage
    "diagnostic_gaspillage_realise": True,
    "plan_gaspillage_en_place": False,
    "actions_gaspillage_realisees": [Diagnostic.ActionsGaspillage.SENSIBILISATION],
    "actions_gaspillage_autre": "Compost des restes",
    "dons_convention": True,
    "dons_frequence": 4,
    "dons_quantite": Decimal("120"),
    "dons_type_denrees": "Fruits",
    # diversification
    "plan_diversification_en_place": True,
    "plan_diversification_actions": [Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
    "service_type": Diagnostic.ServiceType.MENU_UNIQUE,
    "menu_vegetarien_frequence": Diagnostic.MenuVegetarienFrequence.QUOTIDIEN,
    "menu_vegetarien_bases": [Diagnostic.MenuVegetarienBase.SOJA],
    # plastique
    "plastique_bouteille_boisson_remplace": True,
    "plastique_bouteille_remplace": False,
    "plastique_ustensile_remplace": True,
    "plastique_vaisselle_jetable_remplace": False,
    "plastique_contenant_remplace": True,
    "vente_emporter": True,
    "plastique_contenant_emporter_remplace": False,
    # information
    "information_affichage_permanent": True,
    "information_electronique_annuelle": False,
    "information_part_egalim": True,
    "information_part_pat": False,
    "information_consultation_qualite": True,
}


@freeze_time("2027-01-30")  # during the 2026 campaign
class DiagnosticTeledeclarationJustificatif2026Test(APITestCase):
    template_name = "teledeclaration_pdf/justificatif_2026/index.html"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(email="gestionnaire@example.com")
        cls.canteen = CanteenFactory(managers=[cls.user])

    def _render(self, diagnostic):
        return get_template(self.template_name).render(DiagnosticTeledeclarationPdfView.get_context(diagnostic))

    def _teledeclared_diagnostic(self, **kwargs):
        diagnostic = DiagnosticFactory(
            canteen=self.canteen, year=2026, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE, **kwargs
        )
        diagnostic.teledeclare(self.user)
        return diagnostic

    def assertDisplaysValueAfterLabel(self, html, volet, field_name, displayed_value):
        """
        The label of the field, directly followed by its value, in the text of the page
        """
        text = " ".join(unescape(strip_tags(html)).split())
        label = get_teledeclaration_verbose_name(2026, volet, field_name)
        self.assertIn(f"{label} {displayed_value}", text)

    def test_display_the_label_of_all_the_volet_fields(self):
        diagnostic = self._teledeclared_diagnostic(**VOLET_ANSWERS_2026)

        html = self._render(diagnostic)

        for volet in ["APPROVISIONNEMENT", "GASPILLAGE", "DIVERSIFICATION", "PLASTIQUE", "INFORMATION"]:
            for field_name in get_teledeclaration_fields_all(2026, volet, diagnostic.diagnostic_type):
                with self.subTest(volet=volet, field=field_name):
                    label = escape(get_teledeclaration_verbose_name(2026, volet, field_name))
                    if field_name == "nombre_repas_an":
                        # only in the meal count block, not repeated in the approvisionnement volet
                        self.assertEqual(html.count(label), 1)
                    else:
                        self.assertIn(label, html)

    def test_display_the_diagnostic_type(self):
        diagnostic = self._teledeclared_diagnostic()

        html = self._render(diagnostic)

        text = " ".join(unescape(strip_tags(html)).split())
        self.assertIn(f"Vous avez choisi {Diagnostic.DiagnosticType.SIMPLE.label}", text)

    def test_display_if_generated_from_purchases(self):
        for generated_from_purchases, displayed_value in [(True, "Oui"), (False, "Non")]:
            with self.subTest(generated_from_purchases=generated_from_purchases):
                # one diagnostic per canteen and year
                canteen = CanteenFactory(managers=[self.user])
                diagnostic = DiagnosticFactory(
                    canteen=canteen,
                    year=2026,
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                    generated_from_purchases=generated_from_purchases,
                )
                diagnostic.teledeclare(self.user)

                html = self._render(diagnostic)

                text = " ".join(unescape(strip_tags(html)).split())
                self.assertIn(f"A été automatiquement généré depuis les achats {displayed_value}", text)

    def test_display_the_value_of_the_volet_fields(self):
        diagnostic = self._teledeclared_diagnostic(**VOLET_ANSWERS_2026)

        html = self._render(diagnostic)

        # one field per volet
        self.assertDisplaysValueAfterLabel(html, "GASPILLAGE", "dons_type_denrees", "Fruits")
        self.assertDisplaysValueAfterLabel(
            html, "DIVERSIFICATION", "service_type", Diagnostic.ServiceType.MENU_UNIQUE.label
        )
        self.assertDisplaysValueAfterLabel(html, "PLASTIQUE", "vente_emporter", "Oui")
        self.assertDisplaysValueAfterLabel(html, "INFORMATION", "information_part_pat", "Non")

    def test_does_not_display_the_fields_deleted_in_2026(self):
        fields_deleted_in_2026 = {
            ("GASPILLAGE", "mesures_gaspillage_realisees"): True,
            ("GASPILLAGE", "commentaires_gaspillage_autre"): "Un commentaire",
            ("PLASTIQUE", "plastique_contenant_cuisson_remplace"): True,
            ("PLASTIQUE", "plastique_contenant_service_remplace"): True,
            ("INFORMATION", "information_qualite_nutritionnelle"): True,
            ("INFORMATION", "information_qualite_durable"): True,
            ("INFORMATION", "information_frequence"): Diagnostic.InformationFrequence.ANNUELLE,
            ("INFORMATION", "information_supports"): [Diagnostic.InformationSupport.AFFICHAGE],
            ("INFORMATION", "information_supports_autre"): "Journal de l'école",
            ("INFORMATION", "information_support_url"): "https://example.com/menus",
        }
        diagnostic = self._teledeclared_diagnostic(**VOLET_ANSWERS_2026)
        # filled after teledeclare: these fields don't exist anymore in 2026
        for (_, field_name), value in fields_deleted_in_2026.items():
            setattr(diagnostic, field_name, value)

        html = self._render(diagnostic)

        text = " ".join(unescape(strip_tags(html)).split())
        for volet, field_name in fields_deleted_in_2026:
            with self.subTest(field=field_name):
                self.assertNotIn(get_teledeclaration_verbose_name(2025, volet, field_name), text)

    def test_display_the_description_only_if_not_groupe(self):
        user = UserFactory()
        canteen_site = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_comments="Description du site",
            managers=[user],
        )
        canteen_groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE,
            publication_comments="Description du groupe",
            managers=[user],
        )
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=canteen_groupe)
        diagnostic_site = DiagnosticFactory(
            canteen=canteen_site, year=2026, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic_groupe = DiagnosticFactory(
            canteen=canteen_groupe, year=2026, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic_site.teledeclare(user)
        # skip_validations: the meal count of each satellite isn't needed for this test
        diagnostic_groupe.teledeclare(user, skip_validations=True)

        # site: the description is displayed
        canteen_fields = DiagnosticTeledeclarationPdfView.get_context(diagnostic_site)["volets"]["CANTEEN"]
        self.assertIn({"label": "Description", "value": "Description du site"}, canteen_fields)

        # groupe: the description is never displayed
        canteen_fields = DiagnosticTeledeclarationPdfView.get_context(diagnostic_groupe)["volets"]["CANTEEN"]
        self.assertNotIn("Description", [field["label"] for field in canteen_fields])

    def test_display_the_cost_per_meal(self):
        diagnostic = self._teledeclared_diagnostic(valeur_totale=10000, nombre_repas_an=1000)

        html = self._render(diagnostic)

        self.assertIn("Estimation du coût moyen par repas servi", html)
        self.assertIn("10,00 € HT", html)  # 10 000 € / 1 000 couverts

    def test_display_the_provisional_alert_only_during_the_campaign(self):
        diagnostic = self._teledeclared_diagnostic()

        html = self._render(diagnostic)
        self.assertIn("Justificatif provisoire", html)

        with freeze_time("2027-06-30"):  # after the 2026 campaign
            html = self._render(diagnostic)
            self.assertNotIn("Justificatif provisoire", html)

    def test_display_the_campaign_end_date(self):
        diagnostic = self._teledeclared_diagnostic()

        html = self._render(diagnostic)

        self.assertIn("jusqu'à la clôture de la télédéclaration, 31 mars 2027", html)

    def test_display_a_sentence_if_volet_is_empty(self):
        volets = ["GASPILLAGE", "DIVERSIFICATION", "PLASTIQUE", "INFORMATION"]
        empty_fields = {
            field: None
            for volet in volets
            for field in get_teledeclaration_fields_all(2026, volet, Diagnostic.DiagnosticType.SIMPLE)
        }
        diagnostic = self._teledeclared_diagnostic(**empty_fields)

        html = self._render(diagnostic)

        self.assertEqual(html.count("Volet non renseigné"), len(volets))
        for volet in volets:
            for field_name in get_teledeclaration_fields_all(2026, volet, Diagnostic.DiagnosticType.SIMPLE):
                with self.subTest(volet=volet, field=field_name):
                    self.assertNotIn(escape(get_teledeclaration_verbose_name(2026, volet, field_name)), html)

    def test_display_the_applicant_email(self):
        diagnostic = self._teledeclared_diagnostic()

        html = self._render(diagnostic)

        self.assertIn("gestionnaire@example.com", html)

    def test_display_the_teledeclaration_and_canteen_ids(self):
        # large ids, so they can't be found in the html by chance
        canteen = CanteenFactory(id=9999999, managers=[self.user])
        diagnostic = DiagnosticFactory(
            id=8888888, canteen=canteen, year=2026, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        # skip_validations: a canteen created with an id has its geo fields reset, so it isn't "filled"
        diagnostic.teledeclare(self.user, skip_validations=True)

        html = self._render(diagnostic)

        self.assertEqual(diagnostic.teledeclaration_id, 8888888)
        self.assertIn("8888888", html)
        self.assertIn("9999999", html)

    def test_display_the_teledeclaration_date(self):
        diagnostic = self._teledeclared_diagnostic()

        html = self._render(diagnostic)

        self.assertIn("30 janvier 2027", html)
