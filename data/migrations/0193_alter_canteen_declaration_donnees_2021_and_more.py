# Generated by Django 5.0.7 on 2025-07-10 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0192_remove_canteen_publication_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="canteen",
            name="declaration_donnees_2021",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2021"
            ),
        ),
        migrations.AlterField(
            model_name="canteen",
            name="declaration_donnees_2022",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2022"
            ),
        ),
        migrations.AlterField(
            model_name="canteen",
            name="declaration_donnees_2023",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2023"
            ),
        ),
        migrations.AlterField(
            model_name="canteen",
            name="declaration_donnees_2024",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2024"
            ),
        ),
        migrations.AlterField(
            model_name="historicalcanteen",
            name="declaration_donnees_2021",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2021"
            ),
        ),
        migrations.AlterField(
            model_name="historicalcanteen",
            name="declaration_donnees_2022",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2022"
            ),
        ),
        migrations.AlterField(
            model_name="historicalcanteen",
            name="declaration_donnees_2023",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2023"
            ),
        ),
        migrations.AlterField(
            model_name="historicalcanteen",
            name="declaration_donnees_2024",
            field=models.BooleanField(
                default=False, verbose_name="a télédéclaré ses données de 2024"
            ),
        ),
    ]
