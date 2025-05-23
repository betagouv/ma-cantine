# Generated by Django 5.0.7 on 2025-04-24 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0178_canteen_creation_source_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase",
            name="creation_source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("TUNNEL", "Tunnel"),
                    ("API", "API"),
                    ("IMPORT", "Import"),
                    ("ADMIN", "Admin"),
                ],
                max_length=255,
                null=True,
                verbose_name="Source de création de l'achat",
            ),
        ),
    ]
