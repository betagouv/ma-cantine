# Generated by Django 4.2.6 on 2023-11-17 12:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0129_diagnostic_tunnel_appro_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="diagnostic",
            name="creation_source",
            field=models.CharField(
                blank=True,
                choices=[("TUNNEL", "Tunnel")],
                max_length=255,
                null=True,
                verbose_name="comment est-ce que ce diagnostic à été créé ?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldiagnostic",
            name="creation_source",
            field=models.CharField(
                blank=True,
                choices=[("TUNNEL", "Tunnel")],
                max_length=255,
                null=True,
                verbose_name="comment est-ce que ce diagnostic à été créé ?",
            ),
        ),
    ]
