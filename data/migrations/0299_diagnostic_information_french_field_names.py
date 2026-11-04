from django.db import migrations, models

import data.fields

TABLES = ["data_diagnostic", "data_historicaldiagnostic"]

RENAMED_FIELDS = [
    ("communication_supports", "information_supports"),
    ("other_communication_support", "information_supports_autre"),
    ("communication_support_url", "information_support_url"),
    ("communicates_on_food_plan", "information_qualite_nutritionnelle"),
    ("communicates_on_food_quality", "information_qualite_durable"),
    ("communication_frequency", "information_frequence"),
]

# {array column: {old value: new value}}
RENAMED_ARRAY_VALUES = {
    "information_supports": {
        "DISPLAY": "AFFICHAGE",
        "WEBSITE": "SITE_INTERNET",
        "OTHER": "AUTRE",
        "DIGITAL": "ELECTRONIQUE",
    },
}

# {column: {old value: new value}}
RENAMED_VALUES = {
    "information_frequence": {
        "REGULARLY": "REGULIEREMENT",
        "YEARLY": "ANNUELLE",
        "LESS_THAN_YEARLY": "MOINS_QUE_ANNUELLE",
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
        for column, values in RENAMED_VALUES.items():
            for old_value, new_value in values.items():
                if reverse:
                    old_value, new_value = new_value, old_value
                schema_editor.execute(
                    f'UPDATE {table} SET "{column}" = %s WHERE "{column}" = %s',
                    [new_value, old_value],
                )


def rename_values_forward(apps, schema_editor):
    rename_values(schema_editor)


def rename_values_backward(apps, schema_editor):
    rename_values(schema_editor, reverse=True)


def altered_fields(model_name):
    return [
        migrations.AlterField(
            model_name=model_name,
            name="information_supports",
            field=data.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("EMAIL", "Envoi d'e-mail aux convives ou à leurs représentants"),
                        ("AFFICHAGE", "Par affichage sur le lieu de restauration"),
                        ("SITE_INTERNET", "Sur site internet ou intranet (mairie, cantine)"),
                        ("AUTRE", "Autres moyens d'affichage et de communication électronique"),
                        ("ELECTRONIQUE", "Par voie électronique"),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="Communication utilisée",
            ),
        ),
        migrations.AlterField(
            model_name=model_name,
            name="information_frequence",
            field=models.CharField(
                blank=True,
                choices=[
                    ("REGULIEREMENT", "Régulièrement au cours de l’année"),
                    ("ANNUELLE", "Une fois par an"),
                    ("MOINS_QUE_ANNUELLE", "Moins d'une fois par an"),
                ],
                max_length=255,
                null=True,
                verbose_name="fréquence de communication",
            ),
        ),
    ]


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0298_diagnostic_gaspillage_french_field_names"),
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
