from django.db import migrations, models

import data.fields

TABLES = ["data_diagnostic", "data_historicaldiagnostic"]

RENAMED_FIELDS = [
    ("has_diversification_plan", "plan_diversification_en_place"),
    ("diversification_plan_actions", "plan_diversification_actions"),
    ("vegetarian_weekly_recurrence", "menu_vegetarien_frequence"),
    ("vegetarian_menu_type", "menu_vegetarien_type"),
    ("vegetarian_menu_bases", "menu_vegetarien_bases"),
]

# {column: {old value: new value}}
RENAMED_VALUES = {
    "service_type": {
        "UNIQUE": "MENU_UNIQUE",
        "MULTIPLE_SELF": "CHOIX_MULTIPLE_LIBRE_SERVICE",
        "MULTIPLE_RESERVATION": "CHOIX_MULTIPLE_RESERVATION",
    },
    "menu_vegetarien_frequence": {
        "NEVER": "JAMAIS",
        "LOW": "MOINS_HEBDO",
        "MID": "HEBDO",
        "HIGH": "PLUS_HEBDO",
        "DAILY": "QUOTIDIEN",
    },
}
# {array column: {old value: new value}}
RENAMED_ARRAY_VALUES = {
    "plan_diversification_actions": {
        "PRODUCTS": "PLATS_PRODUITS",
        "TRAINING": "FORMATION",
    },
    "menu_vegetarien_bases": {
        "GRAIN": "CEREALES_LEGUMINEUSES",
        "SOY": "SOJA",
        "CHEESE": "FROMAGE",
        "EGG": "OEUFS",
        "READYMADE": "PLATS_PRETS_A_L_EMPLOI",
    },
}


def rename_values(schema_editor, reverse=False):
    for table in TABLES:
        for column, values in RENAMED_VALUES.items():
            for old_value, new_value in values.items():
                if reverse:
                    old_value, new_value = new_value, old_value
                schema_editor.execute(
                    f'UPDATE {table} SET "{column}" = %s WHERE "{column}" = %s', [new_value, old_value]
                )
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
            name="menu_vegetarien_bases",
            field=data.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("CEREALES_LEGUMINEUSES", "De céréales et/ou les légumes secs (hors soja)"),
                        ("SOJA", "De soja"),
                        ("FROMAGE", "De fromage"),
                        ("OEUFS", "D’œufs"),
                        ("PLATS_PRETS_A_L_EMPLOI", "Plats prêts à l'emploi"),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="bases de menu végétarien",
            ),
        ),
        migrations.AlterField(
            model_name=model_name,
            name="menu_vegetarien_frequence",
            field=models.CharField(
                blank=True,
                choices=[
                    ("JAMAIS", "Jamais"),
                    ("MOINS_HEBDO", "Moins d'une fois par semaine"),
                    ("HEBDO", "Une fois par semaine"),
                    ("PLUS_HEBDO", "Plus d'une fois par semaine"),
                    ("QUOTIDIEN", "De façon quotidienne"),
                ],
                max_length=255,
                null=True,
                verbose_name="Menus végétariens par semaine",
            ),
        ),
        migrations.AlterField(
            model_name=model_name,
            name="plan_diversification_actions",
            field=data.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        (
                            "PLATS_PRODUITS",
                            "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
                        ),
                        (
                            "PRESENTATION",
                            "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
                        ),
                        (
                            "MENU",
                            "Agir sur la manière dont les menus sont conçus ces plats en soulignant leurs attributs positifs",
                        ),
                        (
                            "PROMOTION",
                            "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
                        ),
                        (
                            "FORMATION",
                            "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
                        ),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="actions inclus dans le plan de diversification des protéines",
            ),
        ),
        migrations.AlterField(
            model_name=model_name,
            name="service_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("MENU_UNIQUE", "Menu unique"),
                    ("CHOIX_MULTIPLE_LIBRE_SERVICE", "Choix multiple en libre-service"),
                    ("CHOIX_MULTIPLE_RESERVATION", "Choix multiple avec réservation à l’avance au jour le jour"),
                ],
                max_length=255,
                null=True,
                verbose_name="type de service",
            ),
        ),
    ]


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0294_eventlog_from_commandlog"),
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
