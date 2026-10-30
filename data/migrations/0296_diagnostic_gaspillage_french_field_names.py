from django.db import migrations, models

import data.fields

TABLES = ["data_diagnostic", "data_historicaldiagnostic"]

RENAMED_FIELDS = [
    ("has_waste_diagnostic", "diagnostic_gaspillage_realise"),
    ("has_waste_plan", "plan_gaspillage_en_place"),
    ("has_waste_measures", "mesures_gaspillage_realisees"),
    ("waste_actions", "actions_gaspillage_realisees"),
    ("other_waste_action", "actions_gaspillage_autre"),
    ("has_donation_agreement", "dons_convention"),
    ("donation_frequency", "dons_frequence"),
    ("donation_quantity", "dons_quantite"),
    ("donation_food_type", "dons_type_denrees"),
    ("other_waste_comments", "commentaires_gaspillage_autre"),
    ("total_leftovers", "dechets_total"),
    ("duration_leftovers_measurement", "dechets_mesure_duree"),
    ("bread_leftovers", "dechets_pain"),
    ("served_leftovers", "dechets_plateau"),
    ("unserved_leftovers", "dechets_non_servis"),
    ("side_leftovers", "dechets_composantes"),
]

# {array column: {old value: new value}}
RENAMED_ARRAY_VALUES = {
    "actions_gaspillage_realisees": {
        "AWARENESS": "SENSIBILISATION",
        "TRAINING": "FORMATION",
        "REUSE": "REUTILISATION",
    },
}


def rename_values(schema_editor, reverse=False):
    for table in TABLES:
        for column, values in RENAMED_ARRAY_VALUES.items():
            for old_value, new_value in values.items():
                if reverse:
                    old_value, new_value = new_value, old_value
                schema_editor.execute(
                    f'UPDATE {table} SET "{column}" = array_replace("{column}", %s, %s) WHERE %s = ANY("{column}")',
                    [old_value, new_value, old_value],
                )


def rename_values_forward(apps, schema_editor):
    rename_values(schema_editor)


def rename_values_backward(apps, schema_editor):
    rename_values(schema_editor, reverse=True)


def altered_fields(model_name):
    return [
        migrations.AlterField(
            model_name=model_name,
            name="actions_gaspillage_realisees",
            field=data.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("INSCRIPTION", "Pré-inscription des convives obligatoire"),
                        ("SENSIBILISATION", "Sensibilisation par affichage ou autre média"),
                        ("FORMATION", "Formation / information du personnel de restauration"),
                        ("DISTRIBUTION", "Réorganisation de la distribution des composantes du repas"),
                        ("PORTIONS", "Choix des portions (grande faim, petite faim)"),
                        ("REUTILISATION", "Réutilisation des restes de préparation / surplus"),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="actions contre le gaspillage en place",
            ),
        ),
    ]


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0295_diagnostic_diversification_french_field_names"),
    ]

    operations = [
        # 1. rename the fields
        *[
            migrations.RenameField(model_name=model_name, old_name=old_name, new_name=new_name)
            for model_name in ["diagnostic", "historicaldiagnostic"]
            for old_name, new_name in RENAMED_FIELDS
        ],
        # 2. new choices
        *altered_fields("diagnostic"),
        *altered_fields("historicaldiagnostic"),
        # 3. rename the stored values
        migrations.RunPython(rename_values_forward, rename_values_backward),
    ]
