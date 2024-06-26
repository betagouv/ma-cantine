# Generated by Django 4.2.4 on 2023-08-17 22:16

import data.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0123_partner_contact_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partner",
            name="categories",
            field=data.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("appro", "Améliorer ma part de bio / durable"),
                        ("plastic", "Substituer mes plastiques"),
                        ("asso", "Donner à une association"),
                        ("waste", "Diagnostiquer mon gaspillage"),
                        ("training", "Me former ou former mon personnel"),
                        ("suivi", "Assurer mon suivi d'approvisionnement"),
                        ("vege", "Diversifier mes sources de protéines"),
                        ("network", "Mise en réseau d’acteurs de terrain"),
                        ("financial", "Aide financière / matérielle"),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="Besoin(s) comblé(s) par ce partenaire",
            ),
        ),
    ]
