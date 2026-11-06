from django.test import TestCase
from django.urls import reverse


class ApiDocsTest(TestCase):
    def test_diagnostic_fields_description_from_teledeclaration_config(self):
        response = self.client.get(reverse("schema"), {"format": "json"})
        self.assertEqual(response.status_code, 200)
        properties = response.json()["components"]["schemas"]["ManagerDiagnostic"]["properties"]

        # most recent year (2026)
        self.assertEqual(
            properties["valeurBio"]["description"],
            "Total des achats bio ou avec mention « En conversion vers l'agriculture biologique »",
        )
        # empty verbose_name in 2026: 2025's (v1 field exposed under its English name)
        self.assertEqual(properties["hasWastePlan"]["description"], "Plan d'action contre le gaspillage en place")
        # not in the teledeclaration config: the model field's verbose_name
        self.assertEqual(properties["year"]["description"], "année")
