from django.db import migrations

RENAMED_FIELDS = [
    ("cooking_plastic_substituted", "plastique_contenant_cuisson_remplace"),
    ("serving_plastic_substituted", "plastique_contenant_service_remplace"),
    ("plastic_bottles_substituted", "plastique_bouteille_remplace"),
    ("plastic_tableware_substituted", "plastique_ustensile_remplace"),
]


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0299_diagnostic_information_french_field_names"),
    ]

    operations = [
        migrations.RenameField(model_name=model_name, old_name=old_name, new_name=new_name)
        for model_name in ["diagnostic", "historicaldiagnostic"]
        for old_name, new_name in RENAMED_FIELDS
    ]
