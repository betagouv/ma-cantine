# Generated by Django 5.0.8 on 2024-09-06 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0149_historicalwastemeasurement_wastemeasurement"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalwastemeasurement",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical évaluation du gaspillage alimentaire",
                "verbose_name_plural": "historical évaluations du gaspillage alimentaire",
            },
        ),
        migrations.AlterModelOptions(
            name="wastemeasurement",
            options={
                "verbose_name": "évaluation du gaspillage alimentaire",
                "verbose_name_plural": "évaluations du gaspillage alimentaire",
            },
        ),
    ]